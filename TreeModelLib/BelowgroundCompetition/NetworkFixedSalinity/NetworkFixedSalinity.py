#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork


class NetworkFixedSalinity(SimpleNetwork):
    ## Fixed salinityin belowground competition concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.GetSalinity(args)

    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only tree height and leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self.trees = []
        self._xe = []
        self._ye = []
        self._tree_names = np.empty(0)
        self._partner_names = []
        self._partner_indices = []
        self._potential_partner = []
        self._rgf_counter = []

        self.graph_dict = {}
        self._gIDs = []

        self._above_graft_resistance = np.empty(0)
        self._below_graft_resistance = np.empty(0)
        self._psi_height = []
        self._psi_leaf = []
        self._psi_osmo = []
        self._psi_top = []
        self._r_root = []
        self._r_stem = []
        self._kf_sap = []

        self.belowground_resources = []

        self._t_ini = t_ini
        self._t_end = t_end
        self.time = t_end - t_ini

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        self.network = tree.getNetwork()

        self.trees.append(tree)

        self._rgf_counter.append(self.network['rgf'])
        self._partner_names.append(self.network['partner'])
        self._potential_partner.append(self.network['potential_partner'])

        self._xe.append(x)
        self._ye.append(y)
        self.n_trees = len(self._xe)
        self._tree_names = np.concatenate((self._tree_names,
                                           [str(tree.group_name) +
                                            str(tree.tree_id)]))

        self._below_graft_resistance = np.concatenate(
            (self._below_graft_resistance,
             [self.belowGraftResistance(parameter["lp"],
                                        parameter["k_geom"],
                                        parameter["kf_sap"],
                                        geometry["r_root"],
                                        geometry["h_root"],
                                        geometry["r_stem"])]
             ))
        self._above_graft_resistance = np.concatenate(
            (self._above_graft_resistance,
             [self.aboveGraftResistance(
                 parameter["kf_sap"], geometry["r_crown"],
                 geometry["h_stem"], geometry["r_stem"])]
             ))

        self._r_root.append(geometry["r_root"])
        self._r_stem.append(geometry["r_stem"])

        self._kf_sap.append(parameter["kf_sap"])
        self._psi_leaf.append(parameter["leaf_water_potential"])
        self._psi_height.append(
            (2 * geometry["r_crown"] + geometry["h_stem"]) * 9810)
        self._psi_top = np.array(self._psi_leaf) - np.array(self._psi_height)

    def calculateBelowgroundResources(self):
        # FixedSalinity start
        self.calculatePsiOsmo()
        # FixedSalinity end

        self.groupFormation()
        self.rootGraftFormation()
        self.calculateBGresourcesTree()
        res_b = self.getBGresourcesIndividual(self._psi_top, self._psi_osmo,
                                              self._above_graft_resistance,
                                              self._below_graft_resistance)
        self.belowground_resources = self._water_avail / res_b

        for i, tree in zip(range(0, self.n_trees), self.trees):
            network = {}
            network['partner'] = self._partner_names[i]
            network['rgf'] = self._rgf_counter[i]
            network['potential_partner'] = self._potential_partner[i]
            network['water_available'] = self._water_avail[i]
            network['water_absorbed'] = self._water_absorb[i]
            network['water_exchanged'] = self._water_exchanged_trees[i]
            network['psi_osmo'] = self._psi_osmo[i]

            tree.setNetwork(network)

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculatePsiOsmo(self):
        self._xe = np.array(self._xe)
        salinity_tree = ((self._xe - self._min_x) /
                         (self._max_x - self._min_x) *
                         (self._salinity[1] - self._salinity[0]) +
                         self._salinity[0])
        self._psi_osmo = -85000000 * salinity_tree

    ## This function reads salinity from the control file.\n
    def GetSalinity(self, args):
        missing_tags = ["salinity", "type", "max_x", "min_x"]

        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "salinity":
                self._salinity = arg.text.split()
                if len(self._salinity) != 2:
                    raise (
                        KeyError("Two salinity values need to be specified"))
                self._salinity[0] = float(self._salinity[0])
                self._salinity[1] = float(self._salinity[1])
            if tag == "min_x":
                self._min_x = float(args.find("min_x").text)
            if tag == "max_x":
                self._max_x = float(args.find("max_x").text)

            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for below-ground initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground initialisation in project file."
            )
