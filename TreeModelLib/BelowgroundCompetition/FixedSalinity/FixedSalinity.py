#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2020-Today
@author: ronny.peters@tu-dresden.de
"""
import numpy as np
from pyMANGA.TreeModelLib.BelowgroundCompetition.BelowgroundCompetition import BelowgroundCompetition


class FixedSalinity(BelowgroundCompetition):
    ## Fixed salinityin belowground competition concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.GetSalinity(args)

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        self._xe = np.array(self._xe)
        salinity_tree = ((self._xe - self._min_x) /
                         (self._max_x - self._min_x) *
                         (self._salinity[1] - self._salinity[0]) +
                         self._salinity[0])
        psi_zero = np.array(self._psi_leaf) + (2 * np.array(self._r_crown) +
                                               np.array(self._h_stem)) * 9810
        psi_sali = np.array(psi_zero) + 85000000 * salinity_tree
        self.belowground_resources = psi_sali / psi_zero

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
            except:
                print("WARNING: Tag " + tag +
                      " not specified for 'FixedSalinity' below-ground "
                      "initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground initialisation in project file."
            )

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        self._xe.append(x)
        self._h_stem.append(geometry["h_stem"])
        self._r_crown.append(geometry["r_crown"])
        self._psi_leaf.append(parameter["leaf_water_potential"])

    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only tree height aund leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self._h_stem = []
        self._r_crown = []
        self._psi_leaf = []
        self._xe = []
