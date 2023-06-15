#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
import os
from os import path

from ResourceLib.BelowGround.Network.Network import Network
from ResourceLib.BelowGround.Individual.OGSLargeScale3D import OGSLargeScale3D


# MRO: NetworkOGSLargeScale3D, Network, OGSLargeScale3D, ResourceModel,
# object
class NetworkOGSLargeScale3D(Network, OGSLargeScale3D):
    ## OGS integration and network approach (root grafting) for below-ground
    # competition concept. This case is using OGSLargeScale3D and
    # Network as parent classes.
    # @param args: Please see input file tag documentation for details
    # @date: 2021 - Today
    def __init__(self, args):
        OGSLargeScale3D.__init__(self, args)
        super().getInputParameters(args)

    ## This functions prepares the plant variables for the
    # NetworkOGSLargeScale3D concept.\n
    #  @param t_ini - initial time for next time step \n
    #  @param t_end - end time for next time step
    def prepareNextTimeStep(self, t_ini, t_end):
        ## Load both prepartNextTimeStep methods
        # The only parameters occurring in both are t_ini and t_end and as
        # the ones from OGS are needed, OGS needs to be loaded after network
        super().prepareNextTimeStep(t_ini, t_end)
        OGSLargeScale3D.prepareNextTimeStep(self, t_ini, t_end)

    ## Before being able to calculate the resources, all plant enteties need
    #  to be added with their current implementation for the next time step.
    #  Here, in the OGS case, each plant is represented by a contribution to
    #  python source terms in OGS. To this end, their resource uptake is
    #  saved in numpy arrays.
    #  @param plant
    def addPlant(self, plant):
        # Network stuff
        super().addPlant(plant)

        # OGS stuff
        x, y = plant.getPosition()
        # add cell IDs and cell volume to plant
        geometry = plant.getGeometry()
        root_radius = geometry["r_root"]
        super().addCellCharateristics(x, y, root_radius)

    ## This function creates an array with values of osmotic potential based
    # on values saved in network attributes (this is the osmotic potential
    # calculated at the end of the last time step). If a new plant with osmotic
    # potential = 0 is recruited, the initial value is approximated by
    # averaging the osmotic potential below the other plants. Note: this might
    # lead to inaccurate starting values if (i) the time step length of MANGA
    # is very large and (ii) if plants are recruited and no or not many plants
    # exist.
    def addPsiOsmo(self):
        psi_osmo = self.network['psi_osmo']
        # Case: self.network['psi_osmo'] is empty
        if psi_osmo:
            self._psi_osmo.append(np.array(psi_osmo))
        # Case: self.network['psi_osmo'] is not empty
        else:
            mean_of_others = np.mean(self._psi_osmo)
            # Case: there are no other plants with osmotic potential yet
            if np.isnan(mean_of_others):
                self._psi_osmo.append(0)
            # Case: starting value for this plant is the average osmotic
            # potential of existing plants
            else:
                self._psi_osmo.append(mean_of_others)

    ## This function updates and returns BelowgroundResources in the current
    #  time step. For each plant a reduction factor is calculated which is
    #  defined as: resource uptake at zero salinity and without resource
    #  sharing (root grafting)/ actual resource uptake.
    def calculateBelowgroundResources(self):
        ## Network stuff - calculate amount of water absorbed from
        # soil column
        # Convert psi_osmo to np array in order to use in
        # calculateBGresourcesPlant()
        self._psi_osmo = np.array(self._psi_osmo)
        super().groupFormation()
        super().rootGraftFormation()
        super().calculateBGresourcesPlant()

        # Map water absorbed as contribution to respective cells
        # Convert water_abs from m³/time step to kg/s
        self._plant_water_uptake = self._water_absorb * 1000 / self.time

        # Calculate water withdrawal per cell
        super().calculateCompletePlantContribution()

        ## OGS stuff
        # Copy scripts, write bc inputs, run OGS
        super().copyPythonScript()
        np.save(
            path.join(self._ogs_project_folder, "complete_contributions.npy"),
            self._plant_contribution_per_cell)
        self.runOGSandWriteFiles()

        ## Calculate bg factor
        # Get cell salinity array from external files
        super().getCellSalinity()
        # Calculate salinity below each plant
        super().calculatePlantSalinity()

        self.belowground_resources = Network.getBGfactor(self)

        # Update network parameters
        super().updateNetworkParametersForGrowthAndDeath()

        # OGS stuff - update ogs parameters
        self.renameParameters()
