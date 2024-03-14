#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ResourceLib.BelowGround.Network.Network import Network
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity


class NetworkFixedSalinity(Network, FixedSalinity):
    """
    NetworkFixedSalinity below-ground resource concept.
    """
    def __init__(self, args):
        """
        Blow-ground resource concept.
        MRO: NetworkFixedSalinity, Network, FixedSalinity, ResourceModel, object
        Args:
            args: NetworkFixedSalinity module specifications from project file tags
        """
        case = args.find("type").text
        super().__init__(args)
        self.getInputParameters(args=args)

    def prepareNextTimeStep(self, t_ini, t_end):
        # Use Network method
        super().prepareNextTimeStep(t_ini=t_ini, t_end=t_end)

    def addPlant(self, plant):
        # Use Network method
        super().addPlant(plant=plant)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on pore-water salinity below the
        center of each plant and the exchange between grafted trees.
        Sets:
            numpy array of shape(number_of_trees)
        """
        # FixedSalinity start
        self.calculatePsiOsmo()
        # FixedSalinity end

        super().calculateBelowgroundResources()

    def calculatePsiOsmo(self):
        """
        Calculate osmotic water potential (Pa) in the soil based on pore water salinity.
        Sets:
            numpy array of shape(number_of_plants)
        """
        salinity_plant = super().getPlantSalinity()
        self._psi_osmo = -85000000 * salinity_plant

    def getInputParameters(self, args):
        # Get FixedSalinity inputs
        super(Network, self).getInputParameters(args)
        # Get Network inputs
        tags = {
            "prj_file": args,
            "required": ["f_radius"],
            "optional": ["exchange"]

        }
        super(FixedSalinity, self).getInputParameters(**tags)
