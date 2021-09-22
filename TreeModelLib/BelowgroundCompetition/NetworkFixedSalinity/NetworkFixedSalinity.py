#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork
from TreeModelLib.BelowgroundCompetition.FixedSalinity import FixedSalinity


class NetworkFixedSalinity(SimpleNetwork):
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
    def prepareNextTimeStep(self, t_ini, t_end):
        SimpleNetwork.prepareNextTimeStep(self, t_ini=t_ini, t_end=t_end)

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: tree
    def addTree(self, tree):
        SimpleNetwork.addTree(self, tree=tree)

    def calculateBelowgroundResources(self):
        # FixedSalinity start
        self.calculatePsiOsmo()
        # FixedSalinity end

        SimpleNetwork.calculateBelowgroundResources(self)

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

    ## This function reads input parameters, e.g. salinity from the control
    # file.
    def getInputParameters(self, args):
        SimpleNetwork.getInputParameters(self, args=args)
        FixedSalinity.GetSalinity(self, args=args)
