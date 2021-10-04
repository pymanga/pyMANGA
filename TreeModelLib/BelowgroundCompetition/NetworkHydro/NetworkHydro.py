#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork
from TreeModelLib.BelowgroundCompetition.SimpleHydro import SimpleHydro
from ProjectLib.Logger import method_logger


# MRO: NetworkHydro, SimpleNetwork, SimpleHydro, TreeModel, object
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
    @method_logger
    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini, t_end)
        # Hydro parameters
        self._resistance = []
        self._potential_nosal = []

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next
    #  timestep.
    #  @param: tree
    @method_logger
    def addTree(self, tree):
        super().addTree(tree)
        # Hydro parameters
        geometry = tree.getGeometry()
        parameter = tree.getParameter()

        root_surface_resistance = SimpleHydro.rootSurfaceResistance(
            self, parameter["lp"], parameter["k_geom"], geometry["r_root"],
            geometry["h_root"])
        xylem_resistance = SimpleHydro.xylemResistance(
            self, geometry["r_crown"], geometry["h_stem"], geometry["r_root"],
            parameter["kf_sap"], geometry["r_stem"])
        self._resistance.append(root_surface_resistance + xylem_resistance)
        self._potential_nosal.append(
            (parameter["leaf_water_potential"] +
             (2 * geometry["r_crown"] + geometry["h_stem"]) * 9810))

    ## This function returns a list of the growth reduction factors of all
    # trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    @method_logger
    def calculateBelowgroundResources(self):
        self.calculatePsiOsmo()
        super().calculateBelowgroundResources()

    ## This function calculates the water balance and salinity of each grid
    # cell as defined in SimpleHydro, and calculates the osmotic water
    # potential.
    @method_logger
    def calculatePsiOsmo(self):
        super().transpire()
        self._psi_osmo = np.array(self._salinity) * -85000000

    ## This function reads the input parameters and initialises the mesh.\n
    @method_logger
    def getInputParameters(self, args):
        super().makeGrid(args)
        super().getInputParameters(args)
