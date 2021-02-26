#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from TreeModelLib.BelowgroundCompetition.Network import Network


class NetworkHydro(Network):
    ## Simple approach to reduce water availability due to osmotic potential.
    #  Processes are gradient flow, salinisation by plant transpiration,
    #  dilution by tides and horizontal mixing (diffusion).\n
    #  @param: Tags to define SimpleHydro, see tag documentation \n
    #  @date: 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.makeGrid(args)


    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only tree height and leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self.trees = []
        self._xe = []
        self._ye = []
        self._tree_name = np.empty(0)
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
        self._tree_name = np.concatenate((self._tree_name,
                                         [str(tree.group_name) + str(tree.tree_id)]))

        self._below_graft_resistance = np.concatenate((self._below_graft_resistance,
                                                       [self.belowGraftResistance(parameter["lp"],
                                                                                  parameter["k_geom"],
                                                                                  parameter["kf_sap"],
                                                                                  geometry["r_root"],
                                                                                  geometry["h_root"],
                                                                                  geometry["r_stem"])]
                                                       ))
        self._above_graft_resistance = np.concatenate((self._above_graft_resistance,
                                                       [self.aboveGraftResistance(
                                                          parameter["kf_sap"], geometry["r_crown"],
                                                          geometry["h_stem"], geometry["r_stem"])]
                                                       ))

        self._r_root.append(geometry["r_root"])
        self._r_stem.append(geometry["r_stem"])

        self._psi_leaf.append(parameter["leaf_water_potential"])
        self._psi_height.append((2 * geometry["r_crown"] + geometry["h_stem"]) * 9810)
        self._psi_top = np.array(self._psi_leaf) - np.array(self._psi_height)

        self._kf_sap.append(parameter["kf_sap"])

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        self.calculatePsiOsmo()
        # Network start
        self.groupFormation()
        self.rootGraftFormation()
        self.calculateBGresourcesTree()
        # Network end
        self.calculateNewSalinity()

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

    def calculatePsiOsmo(self):
        # calculate water uptake from grid cells
        distance = (np.array(self._r_root)[np.newaxis, np.newaxis, :] -
                    ((self._my_grid[0][:, :, np.newaxis] -
                      np.array(self._xe)[np.newaxis, np.newaxis, :]) ** 2 +
                     (self._my_grid[1][:, :, np.newaxis] -
                      np.array(self._ye)[np.newaxis, np.newaxis, :]) ** 2) ** 0.5)
        presence = distance > 0
        maxe = np.amax(distance, axis=(0, 1))
        self._salinity = []
        self._psi_osmo = []
        for ii in range(distance.shape[2]):
            closest = distance[:, :, ii] == maxe[ii]
            presence[:, :, ii] = np.fmax(closest, presence[:, :, ii])
            self._salinity.append((np.sum(presence[:, :, ii] * self.salinity) /
                                   np.sum(presence[:, :, ii])))
            self._psi_osmo.append(-self._salinity[ii] * 85000)
        self._psi_osmo = np.array(self._psi_osmo)

    ## This function calculates the water balance of each grid cell.
    # Transpiration, dilution (tidal flooding), exchange between neighbouring
    # grid cells and gradient flow is regarded for.
    def calculateNewSalinity(self):
        tsl = (self._t_end - self._t_ini)       # time step length
        s_d = 3600 * 24                         # seconds per day
        distance = (np.array(self._r_root)[np.newaxis, np.newaxis, :] -
                    ((self._my_grid[0][:, :, np.newaxis] -
                      np.array(self._xe)[np.newaxis, np.newaxis, :]) ** 2 +
                     (self._my_grid[1][:, :, np.newaxis] -
                      np.array(self._ye)[np.newaxis, np.newaxis, :]) ** 2) ** 0.5)
        water_loss = np.zeros(np.shape(distance[:, :, 0]))
        presence = distance > 0
        maxe = np.amax(distance, axis=(0, 1))
        for ii in range(distance.shape[2]):
            closest = distance[:, :, ii] == maxe[ii]
            presence[:, :, ii] = np.fmax(closest, presence[:, :, ii])
            water_loss += (self._water_absorb[ii] / s_d /
                            np.sum(presence[:, :, ii])) * presence[:, :, ii]
        print('water loss ' + str(np.mean(water_loss)))
        print('sal old ' + str(np.mean(self.salinity)))

        # refill
        self.salinity += self._sea_salinity * water_loss / self.volume

        # dilution
        self.salinity += (-self.salinity * self.dilution_frac * tsl / s_d +
                          self._sea_salinity * self.dilution_frac * tsl / s_d)

        # diffusion
        salinity_new = self.salinity * (1 - self._diffusion_frac * tsl / s_d)
        # diff in x-dir
        for ii in range(self.x_resolution):
            if ii == self.x_resolution - 1:
                salinity_new[:, ii] += (self.salinity[:, ii] *
                                        self._diffusion_frac * tsl / s_d / 4)
                salinity_new[:, ii - 1] += (self.salinity[:, ii] *
                                    self._diffusion_frac * tsl / s_d / 4)
            elif ii == 0:
                salinity_new[:, ii +
                             1] += (self.salinity[:, ii] *
                                    self._diffusion_frac * tsl / s_d / 4)
                salinity_new[:, ii] += (self.salinity[:, ii] *
                                        self._diffusion_frac * tsl / s_d / 4)
            else:
                salinity_new[:, ii +
                             1] += (self.salinity[:, ii] *
                                    self._diffusion_frac * tsl / s_d / 4)
                salinity_new[:, ii -
                             1] += (self.salinity[:, ii] *
                                    self._diffusion_frac * tsl / s_d / 4)

        # diff in y-dir
        for ii in range(self.y_resolution):
            if ii == self.y_resolution - 1:
                salinity_new[ii, :] += (self.salinity[ii, :] *
                                        self._diffusion_frac * tsl / s_d / 4)
                salinity_new[ii -
                             1, :] += (self.salinity[ii, :] *
                                       self._diffusion_frac * tsl / s_d / 4)
            elif ii == 0:
                salinity_new[ii +
                             1, :] += (self.salinity[ii, :] *
                                       self._diffusion_frac * tsl / s_d / 4)
                salinity_new[ii, :] += (self.salinity[ii, :] *
                                        self._diffusion_frac * tsl / s_d / 4)
            else:
                salinity_new[ii +
                             1, :] += (self.salinity[ii, :] *
                                       self._diffusion_frac * tsl / s_d / 4)
                salinity_new[ii -
                             1, :] += (self.salinity[ii, :] *
                                       self._diffusion_frac * tsl / s_d / 4)
        self.salinity = salinity_new
        # gradient-flow
        multi_fac = self.q_fac * tsl
        salinity_new[0, :] = self.salinity[0, :] * (
            1 - multi_fac) + self._up_sal * multi_fac
        salinity_new[1:self.y_resolution, :] = (
            self.salinity[1:self.y_resolution, :] * (1 - multi_fac) +
            self.salinity[0:(self.y_resolution - 1), :] * multi_fac)
        self.salinity = salinity_new
        print('sal new ' + str(np.mean(self.salinity)))

    ## This function initialises the mesh.\n
    def makeGrid(self, args):
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution",
            "y_resolution", "depth", "porosity", "dilution_frac_upper",
            "dilution_frac_lower", "diffusion_frac", "sea_salinity", "ini_sal",
            "up_sal", "slope", "k_f", "flooding_duration"
        ]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "x_resolution":
                self.x_resolution = int(arg.text)
            elif tag == "y_resolution":
                self.y_resolution = int(arg.text)
            elif tag == "x_1":
                x_1 = float(arg.text)
            elif tag == "x_2":
                x_2 = float(arg.text)
            elif tag == "y_1":
                y_1 = float(arg.text)
            elif tag == "y_2":
                y_2 = float(arg.text)
            elif tag == "depth":
                self._depth = float(arg.text)
            elif tag == "porosity":
                self._porosity = float(arg.text)
            elif tag == "dilution_frac_upper":
                _dilution_frac_upper = float(arg.text)
            elif tag == "dilution_frac_lower":
                _dilution_frac_lower = float(arg.text)
            elif tag == "diffusion_frac":
                self._diffusion_frac = float(arg.text)
            elif tag == "sea_salinity":
                self._sea_salinity = float(arg.text)
            elif tag == "ini_sal":
                self._ini_sal = float(arg.text)
            elif tag == "up_sal":
                self._up_sal = float(arg.text)
            elif tag == "slope":
                self._slope = float(arg.text)
            elif tag == "k_f":
                self._k_f = float(arg.text)
            elif tag == "flooding_duration":
                from ast import literal_eval
                self._flooding_duration = np.array(literal_eval(arg.text))
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for below-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground grid initialisation in project file."
            )
        l_x = x_2 - x_1
        l_y = y_2 - y_1
        x_step = l_x / self.x_resolution
        y_step = l_y / self.y_resolution
        self._mesh_size = np.maximum(x_step, y_step)
        xe = np.linspace(x_1 + x_step / 2.,
                         x_2 - x_step / 2.,
                         self.x_resolution,
                         endpoint=True)
        ye = np.linspace(y_1 + y_step / 2.,
                         y_2 - y_step / 2.,
                         self.y_resolution,
                         endpoint=True)
        self._my_grid = np.meshgrid(xe, ye)
        self.salinity = np.ones(np.shape(self._my_grid[0])) * self._ini_sal
        self.volume = self._depth * x_step * y_step * self._porosity
        self.q_fac = self._k_f * self._slope / y_step
        inds = np.arange(
            (self._flooding_duration.shape[0] - 1) *
            (self.y_resolution - 1), 0,
            -(self._flooding_duration.shape[0] - 1)) / (self.y_resolution - 1)
        inds = np.append(inds, 0)
        inds_int = np.trunc(inds).astype(int)
        inds_frac = inds - inds_int
        raw_flodur = np.append(self._flooding_duration, 0)
        flodur = (raw_flodur[inds_int] + inds_frac *
                  (raw_flodur[inds_int + 1] - raw_flodur[inds_int])) / 24
        dilu_vec = (_dilution_frac_upper +
                    (-_dilution_frac_upper + _dilution_frac_lower) * flodur)
        self.dilution_frac = (np.repeat(np.array([dilu_vec]), self.x_resolution,
                                        axis=0)).transpose()
