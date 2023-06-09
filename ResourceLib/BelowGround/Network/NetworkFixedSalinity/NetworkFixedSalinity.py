#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

from ResourceLib.BelowGround.Network.SimpleNetwork import SimpleNetwork
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity


# MRO: NetworkFixedSalinity, SimpleNetwork, FixedSalinity, ResourceModel, object
class NetworkFixedSalinity(SimpleNetwork, FixedSalinity):
    ## Fixed salinityin belowground competition concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.getInputParameters(args=args)

    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only plant height and leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini=t_ini, t_end=t_end)

    ## Before being able to calculate the resources, all plant entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: plant
    def addPlant(self, plant):
        super().addPlant(plant=plant)

    ## This function returns a list of the growth modification factors of
    # all plants. Calculated in the subsequent timestep.\n
    #  The factor is > 1, if plants receive water from their adjacent plants;
    #  < 1 if the lose water to the adjacent plant; or = 1 if no exchange
    #  happens
    #  @return: np.array with $N_plant$ scalars
    def calculateBelowgroundResources(self):
        # FixedSalinity start
        self.calculatePsiOsmo()
        # FixedSalinity end

        super().calculateBelowgroundResources()

    ## This function returns a list of the growth reduction factors of all plants.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_plant$ scalars
    def calculatePsiOsmo(self):
        salinity_plant = super().getPlantSalinity()
        self._psi_osmo = -85000000 * salinity_plant

    ## This function reads input parameters, e.g. salinity from the control
    # file.
    def getInputParameters(self, args):
        super().getInputParameters(args=args)
        super().GetSalinity(args=args)
