#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition.OGSLargeScale3DExternal import \
     OGSLargeScale3DExternal
from TreeModelLib.BelowgroundCompetition.NetworkOGSLargeScale3D import \
    NetworkOGSLargeScale3D


# Child class of OGSLargeScale3DExternal and NetworkOGSLargeScale3D to use
# external time stepping, e.g. to run MANGA as OGS boundary condition
# The concept needs an array with cumulated cell salinity and
# the number of calls for each cell. It returns an array describing water
# withdrawal in each cell as rate in kg per sec per cell volume.
# The withdrawal is the amount of water absorbed from the soil column,
# and can be different from the amount of water available to the tree du to
# root graft mediated water exchange (see SimpleNetwork).
# MRO: NetworkOGSLargeScale3DExternal, NetworkOGSLargeScale3D,
# SimpleNetwork, OGSLargeScale3DExternal, OGSLargeScale3D, TreeModel, object
class NetworkOGSLargeScale3DExternal(NetworkOGSLargeScale3D,
                                     OGSLargeScale3DExternal):

    def __init__(self, args):
        # Load init method from NetworkOGSLargeScale3D, which includes init
        # method of OGSLargeScale3D and reading of network import parameters
        super().__init__(args)

    # This function allows external communication
    def getOGSAccessible(self):
        return True

    ## This functions prepares the tree variables for the
    # NetworkOGSLargeScale3D concept.\n
    #  @param t_ini - initial time for next time step \n
    #  @param t_end - end time for next time step
    def prepareNextTimeStep(self, t_ini, t_end):
        # Parameters required for NetworkOGSLargeScale3D
        self._tree_cell_volume = []

        # Load init and parameters that are required to get/ process
        # information from OGS and SimpleNetwork
        super().prepareNextTimeStep(t_ini, t_end)

    ## Before being able to calculate the resources, all tree enteties need
    #  to be added with their current implementation for the next time step.
    #  Here, in the OGS case, each tree is represented by a contribution to
    #  python source terms in OGS.
    #  @param tree
    def addPlant(self, tree):
        # Use addPlant of NetworkOGSLargeScale3D
        super().addPlant(tree)

    ## This function updates and returns BelowgroundResources in the current
    #  time step. For each tree a reduction factor is calculated which is
    #  defined as: resource uptake at zero salinity and without resource
    #  sharing (root grafting)/ actual resource uptake.
    #  Before resource uptake is calculated, this function calls
    #  SimpleNetwork functions to develop the root graft network
    def calculateBelowgroundResources(self):
        # Salinity below each tree
        self._tree_salinity = np.empty(self.no_trees)
        if self.no_trees <= 0:
            print("WARNING: All trees are dead.")

        # Get salinity information from OGS in kg/kg (defined in
        # OGSLargeScale3D.py)
        super().calculateTreeSalinity()

        ## NetworkOGSLargeScale3D stuff (defined in SimpleNetwork.py)
        # Convert psi_osmo to np array in order to use in
        self._psi_osmo = np.array(self._psi_osmo)
        # Calculate amount of water absorbed from soil column
        super().groupFormation()
        super().rootGraftFormation()
        super().calculateBGresourcesTree()

        # Calculate bg resource factor (defined in SimpleNetwork)
        self.belowground_resources = super().getBGfactor()

        # Update network parameters (defined in SimpleNetwork)
        super().updateNetworkParametersForGrowthAndDeath()

        # Calculate contribution per cell
        # Map water absorbed as contribution to respective cells
        # Convert water_abs from m³/time step to kg/s
        self._tree_water_uptake = self._water_absorb * 1000 / self.time
        super().calculateCompleteTreeContribution()

    ## Setter for external information
    # This function sets the parameters 'cumsum_salinity' and 'calls_per_cell',
    # which contain information about the cumulated salinity in each cell and
    # the number of calls, calculated by OGS
    def setExternalInformation(self, **args):
        # set external information as defined in OGSLargeScale3DExternal.py
        super().setExternalInformation(**args)

    ## Getter for external information
    # This function returns the estimated water withdrawal in each cell
    # as rate (kg per sec per cell volume)
    def getExternalInformation(self):
        return self._tree_contribution_per_cell
