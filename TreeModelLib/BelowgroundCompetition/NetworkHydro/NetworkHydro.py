#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork
from TreeModelLib.BelowgroundCompetition.SimpleHydro import SimpleHydro


class NetworkHydro(SimpleNetwork, SimpleHydro):
    ## Simple approach to reduce water availability due to osmotic potential.
    #  Processes are gradient flow, salinisation by plant transpiration,
    #  dilution by tides and horizontal mixing (diffusion).\n
    #  @param: Tags to define SimpleHydro, see tag documentation \n
    #  @date: 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.getInputParameters(args)

    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only tree height and leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        SimpleNetwork.prepareNextTimeStep(self, t_ini, t_end)
        # Hydro parameters
        self._resistance = []
        self._potential_nosal = []

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next
    #  timestep.
    #  @param: tree
    def addTree(self, tree):
        SimpleNetwork.addTree(self, tree)
        # Hydro parameters
        geometry = tree.getGeometry()
        parameter = tree.getParameter()

        root_surface_resistance = SimpleHydro.rootSurfaceResistance(self,
                                                                    parameter[
                                                                        "lp"],
                                                                    parameter[
                                                                        "k_geom"],
                                                                    geometry[
                                                                        "r_root"],
                                                                    geometry[
                                                                        "h_root"])
        xylem_resistance = SimpleHydro.xylemResistance(self,
                                                       geometry[
                                                           "r_crown"],
                                                       geometry["h_stem"],
                                                       geometry["r_root"],
                                                       parameter["kf_sap"],
                                                       geometry["r_stem"])
        self._resistance.append(root_surface_resistance + xylem_resistance)
        self._potential_nosal.append(
            (parameter["leaf_water_potential"] +
             (2 * geometry["r_crown"] + geometry["h_stem"]) * 9810))

    ## This function returns a list of the growth reduction factors of all
    # trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        self.calculatePsiOsmo()
        SimpleNetwork.calculateBelowgroundResources(self)

    def calculatePsiOsmo(self):
        SimpleHydro.transpire(self)
        self._psi_osmo = np.array(self._salinity) * -85000

    ## This function reads the input parameters and initialises the mesh.\n
    def getInputParameters(self, args):
        SimpleHydro.makeGrid(self, args)
        SimpleNetwork.getInputParameters(self, args)
