#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2022-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
from ResourceLib.BelowGround.Individual.SymmetricZOI import SymmetricZOI
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity


# MRO: SZoiFixedSalinity, SymmetricZOI, FixedSalinity, TreeModel, object
class SZoiFixedSalinity(SymmetricZOI, FixedSalinity):
    ## Fixed salinity with symmetric zone of influence belowground competition
    # concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        super().makeGrid(args=args)
        self.GetSalinity(args=args)

    ## This functions prepares arrays for the competition
    #  concept. In the SymmetricZOI concept, trees geometric measures
    #  are saved in simple lists and the timestepping is updated. \n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini, t_end)
        FixedSalinity.prepareNextTimeStep(self, t_ini, t_end)

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their current implementation for the next timestep.
    #  @param tree
    def addTree(self, tree):
        super().addTree(tree)
        FixedSalinity.addTree(self, tree)

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent time step.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        super().calculateBelowgroundResources()
        bg_factor_symmetric_ZOI = self.getBelowgroundResources()

        FixedSalinity.calculateBelowgroundResources(self)
        bg_factor_fixed_salinity = FixedSalinity.getBelowgroundResources(self)

        self.belowground_resources = bg_factor_symmetric_ZOI * \
                                     bg_factor_fixed_salinity
