#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib.BelowGround.Generic.OGSExternal import \
     OGSExternal
from ResourceLib.BelowGround.Network.NetworkOGS import \
    NetworkOGS


class NetworkOGSExternal(NetworkOGS, OGSExternal):
    """
    NetworkOGSExternal below-ground resource concept.
    """
    def __init__(self, args):
        """
        # MRO: NetworkOGSExternal, NetworkOGS,
        # Network, OGSExternal, OGS, ResourceModel, object
        Args:
            args: below-ground module specifications from project file tags
        """
        # Load init method from NetworkOGS, which includes init
        # method of OGS and reading of network import parameters
        super().__init__(args)

    def getOGSAccessible(self):
        """
        Allow external communication
        Returns:
            bool
        """
        return True

    def prepareNextTimeStep(self, t_ini, t_end):
        # Parameters required for NetworkOGS
        self._plant_cell_volume = []

        # Load init and parameters that are required to get/ process
        # information from OGS and Network
        super().prepareNetworkParameters(t_ini, t_end)
        super().prepareOGSparameters()

    def addPlant(self, plant):
        # Use addPlant of NetworkOGS
        super().addPlant(plant)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on pore-water salinity below the
        center of each plant and water exchange between grafted trees.
        Sets:
            numpy array of shape(number_of_trees)
        """
        # Salinity below each plant
        self._plant_salinity = np.empty(self.no_plants)
        if self.no_plants <= 0:
            print("WARNING: All plants are dead.")

        # Get salinity information from OGS in kg/kg (defined in
        # OGS.py)
        super().calculatePlantSalinity()

        ## NetworkOGS stuff (defined in Network.py)
        # Convert psi_osmo to np array in order to use in
        self._psi_osmo = np.array(self._psi_osmo)
        # Calculate amount of water absorbed from soil column
        super().groupFormation()
        super().rootGraftFormation()
        super().calculateBGresourcesPlant()

        # Calculate bg resource factor (defined in Network)
        self.belowground_resources = super().getBGfactor()

        # Update network parameters (defined in Network)
        super().updateNetworkParametersForGrowthAndDeath()

        # Calculate contribution per cell
        # Map water absorbed as contribution to respective cells
        # Convert water_abs from m³/time step to kg/s
        self._plant_water_uptake = self._water_absorb * 1000 / self.time
        super().calculateCompletePlantContribution()

    def setExternalInformation(self, **args):
        """
        Set parameters 'cumsum_salinity' and 'calls_per_cell', which contain information about the
        cumulated salinity in each cell and the number of calls, calculated by OGS
        Args:
            **args:
        """
        # set external information as defined in OGSExternal.py
        super().setExternalInformation(**args)

    def getExternalInformation(self):
        """
        Returns estimated water withdrawal in each cell as rate (kg per sec per cell volume)
        Returns:

        """
        return self._plant_contribution_per_cell
