#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork
from TreeModelLib.BelowgroundCompetition.FixedSalinity import FixedSalinity
from ProjectLib.Logger import method_logger


# MRO: NetworkFixedSalinity, SimpleNetwork, FixedSalinity, TreeModel, object
class NetworkFixedSalinity(SimpleNetwork, FixedSalinity):
    ## Fixed salinityin belowground competition concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.getInputParameters(args=args)

    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only tree height and leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    @method_logger
    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini=t_ini, t_end=t_end)

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: tree
    @method_logger
    def addTree(self, tree):
        super().addTree(tree=tree)

    ## This function returns a list of the growth modification factors of
    # all trees. Calculated in the subsequent timestep.\n
    #  The factor is > 1, if trees receive water from their adjacent trees;
    #  < 1 if the lose water to the adjacent tree; or = 1 if no exchange
    #  happens
    #  @return: np.array with $N_tree$ scalars
    @method_logger
    def calculateBelowgroundResources(self):
        # FixedSalinity start
        self.calculatePsiOsmo()
        # FixedSalinity end

        super().calculateBelowgroundResources()

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculatePsiOsmo(self):
        salinity_tree = super().getTreeSalinity()
        self._psi_osmo = -85000000 * salinity_tree

    ## This function reads input parameters, e.g. salinity from the control
    # file.
    @method_logger
    def getInputParameters(self, args):
        super().getInputParameters(args=args)
        super().GetSalinity(args=args)
