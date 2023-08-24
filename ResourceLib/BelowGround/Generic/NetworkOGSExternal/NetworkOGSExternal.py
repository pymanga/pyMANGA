#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
import numpy as np
from ResourceLib.BelowGround.Generic.OGSExternal import \
     OGSExternal
from ResourceLib.BelowGround.Network.NetworkOGS import \
    NetworkOGS


# Child class of OGSExternal and NetworkOGS to use
# external time stepping, e.g. to run MANGA as OGS boundary condition
# The concept needs an array with cumulated cell salinity and
# the number of calls for each cell. It returns an array describing water
# withdrawal in each cell as rate in kg per sec per cell volume.
# The withdrawal is the amount of water absorbed from the soil column,
# and can be different from the amount of water available to the plant du to
# root graft mediated water exchange (see Network).
# MRO: NetworkOGSExternal, NetworkOGS,
# Network, OGSExternal, OGS, ResourceModel, object
class NetworkOGSExternal(NetworkOGS, OGSExternal):

    def __init__(self, args):
        # Load init method from NetworkOGS, which includes init
        # method of OGS and reading of network import parameters
        super().__init__(args)

    # This function allows external communication
    def getOGSAccessible(self):
        return True

    ## This functions prepares the plant variables for the
    # NetworkOGS concept.\n
    #  @param t_ini - initial time for next time step \n
    #  @param t_end - end time for next time step
    def prepareNextTimeStep(self, t_ini, t_end):
        # Parameters required for NetworkOGS
        self._plant_cell_volume = []

        # Load init and parameters that are required to get/ process
        # information from OGS and Network
        super().prepareNextTimeStep(t_ini, t_end)

    ## Before being able to calculate the resources, all plant enteties need
    #  to be added with their current implementation for the next time step.
    #  Here, in the OGS case, each plant is represented by a contribution to
    #  python source terms in OGS.
    #  @param plant
    def addPlant(self, plant):
        # Use addPlant of NetworkOGS
        super().addPlant(plant)

    ## This function updates and returns BelowgroundResources in the current
    #  time step. For each plant a reduction factor is calculated which is
    #  defined as: resource uptake at zero salinity and without resource
    #  sharing (root grafting)/ actual resource uptake.
    #  Before resource uptake is calculated, this function calls
    #  Network functions to develop the root graft network
    def calculateBelowgroundResources(self):
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

    ## Setter for external information
    # This function sets the parameters 'cumsum_salinity' and 'calls_per_cell',
    # which contain information about the cumulated salinity in each cell and
    # the number of calls, calculated by OGS
    def setExternalInformation(self, **args):
        # set external information as defined in OGSExternal.py
        super().setExternalInformation(**args)

    ## Getter for external information
    # This function returns the estimated water withdrawal in each cell
    # as rate (kg per sec per cell volume)
    def getExternalInformation(self):
        return self._plant_contribution_per_cell
