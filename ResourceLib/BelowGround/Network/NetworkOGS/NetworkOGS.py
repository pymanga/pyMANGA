#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from os import path

from ResourceLib.BelowGround.Network.Network import Network
from ResourceLib.BelowGround.Individual.OGS import OGS


class NetworkOGS(Network, OGS):
    """
    NetworkOGS below-ground resource concept.
    """
    def __init__(self, args):
        """
        MRO: NetworkOGS, Network, OGS, ResourceModel, object.
        Args:
            args: NetworkOGS module specifications from project file tags
        """
        OGS.__init__(self, args)
        super().getInputParameters(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        ## Load both prepartNextTimeStep methods
        # The only parameters occurring in both are t_ini and t_end and as
        # the ones from OGS are needed, OGS needs to be loaded after network
        self.prepareNetworkParameters(t_ini, t_end)
        OGS.prepareNextTimeStep(self, t_ini, t_end)

    def prepareNetworkParameters(self, t_ini, t_end):
        """
        Call Network method to prepare next time step.
        """
        super().prepareNextTimeStep(t_ini, t_end)

    def addPlant(self, plant):
        # Network stuff
        super().addPlant(plant)

        # OGS stuff
        x, y = plant.getPosition()
        # add cell IDs and cell volume to plant
        geometry = plant.getGeometry()
        root_radius = geometry["r_root"]
        super().addCellCharateristics(x, y, root_radius)

    def addPsiOsmo(self):
        """
        Create an array of osmotic potential values based on the values stored in the network attributes (this is the
        osmotic potential calculated at the end of the last time step). When a new plant is recruited with osmotic
        potential = 0, the initial value is approximated by averaging the osmotic potentials of the other plants.
        Note: This may lead to inaccurate initial values if (i) the time step length of MANGA is very large and
        (ii) when plants are recruited and there are no or few other plants.
        Sets:
            array of shape(no_of_plants)
        """
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

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each tree based on water exchange between grafted trees
        and on the pore-water salinity below the center of each tree.
        Sets:
            numpy array of shape(number_of_plants)
        """
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
