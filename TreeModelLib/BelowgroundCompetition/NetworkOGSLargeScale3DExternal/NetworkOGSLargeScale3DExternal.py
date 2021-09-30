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
class NetworkOGSLargeScale3DExternal(NetworkOGSLargeScale3D,
                                     OGSLargeScale3DExternal):
    def __init__(self, args):
        # Load init method from NetworkOGSLargeScale3D, which includes init
        # method of OGSLargeScale3D and reading of network import parameters
        NetworkOGSLargeScale3D.__init__(self, args)

    # This function allows external communication
    def getOGSAccessible(self):
        return True

    ## This functions prepares the tree variables for the
    # NetworkOGSLargeScale3D concept.\n
    #  @param t_ini - initial time for next time step \n
    #  @param t_end - end time for next time step
    def prepareNextTimeStep(self, t_ini, t_end):
        # Load init method of SimpleNetwork = super(NetworkOGSLargeScale3D)
        super(NetworkOGSLargeScale3D, self).prepareNextTimeStep(t_ini, t_end)

        # Parameters required for NetworkOGSLargeScale3D
        self._tree_cell_volume = []

        # Load parameters that are required to get/ process information from
        # OGS
        OGSLargeScale3DExternal.prepareOGSparameters(self)

    ## Before being able to calculate the resources, all tree enteties need
    #  to be added with their current implementation for the next time step.
    #  Here, in the OGS case, each tree is represented by a contribution to
    #  python source terms in OGS.
    #  @param tree
    def addTree(self, tree):
        NetworkOGSLargeScale3D.addTree(self, tree)

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

        # Get salinity information from OGS in kg/kg
        OGSLargeScale3DExternal.calculateTreeSalinity(self)

        ## NetworkOGSLargeScale3D stuff
        # Convert psi_osmo to np array in order to use in
        self._psi_osmo = np.array(self._psi_osmo)
        # Calculate amount of water absorbed from soil column
        NetworkOGSLargeScale3D.groupFormation(self)
        NetworkOGSLargeScale3D.rootGraftFormation(self)
        NetworkOGSLargeScale3D.calculateBGresourcesTree(self)

        # Calculate bg resource factor
        self.belowground_resources = NetworkOGSLargeScale3D.getBGfactor(self)

        # Update network parameters
        NetworkOGSLargeScale3D.updateNetworkParametersForGrowthAndDeath(self)

        # Calculate contribution per cell
        # Map water absorbed as contribution to respective cells
        # Convert water_abs from m³/time step to kg/s
        self._tree_water_uptake = self._water_absorb * 1000 / self.time
        OGSLargeScale3DExternal.calculateCompleteTreeContribution(self)

    ## Setter for external information
    # This function sets the parameters 'cumsum_salinity' and 'calls_per_cell',
    # which contain information about the cumulated salinity in each cell and
    # the number of calls, calculated by OGS
    def setExternalInformation(self, **args):
        OGSLargeScale3DExternal.setExternalInformation(self, **args)

    ## Getter for external information
    # This function returns the estimated water withdrawal in each cell
    # as rate (kg per sec per cell volume)
    def getExternalInformation(self):
        return self._tree_contribution_per_cell

