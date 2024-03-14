#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ResourceLib.BelowGround.Individual.OGS import OGS
import numpy as np


class OGSExternal(OGS):
    """
    OGSExternal below-ground resource concept.
    """
    def __init__(self, args):
        """
        OpenGeoSys below-ground module adapted for external use.
        MRO: OGSExternal, OGS, TreeModel, object
        Args:
            args:
        """
        super().__init__(args)

    def getOGSAccessible(self):
        """
        Allow external communication
        Returns:
            bool
        """
        return True

    def prepareNextTimeStep(self, t_ini, t_end):
        self.n_plants = 0

        # Arrays with length 'no. of plants'
        self._total_resistance = []

        self._psi_leaf = np.empty(0)
        self._psi_height = np.empty(0)
        self._psi_osmo = np.empty(0)
        self._rcrown = []
        self._hstem = []

        super().prepareOGSparameters()

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()

        # Cells affected by plant water uptake
        root_radius = geometry["r_root"]
        super().addCellCharateristics(x, y, root_radius)

        # Resistances against water flow in plant
        # Calculate total plant resistance
        total_resistance = super().totalTreeResistance(parameter, geometry)
        self._total_resistance.append(total_resistance)

        # Water potentials
        self._psi_leaf = np.concatenate(
            (self._psi_leaf, [(parameter["leaf_water_potential"])]))
        self._psi_height = np.concatenate(
            (self._psi_height,
             [-(2 * geometry["r_crown"] + geometry["h_stem"]) * 9810]))

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on pore-water salinity below the
        center of each plant.
        Sets:
            numpy array of shape(number_of_trees)
        """
        # Number of plants
        self.no_plants = len(self._total_resistance)
        # Salinity below each plant
        self._plant_salinity = np.empty(self.no_plants)
        if self.no_plants <= 0:
            print("WARNING: All plants are dead.")

        # Calculate salinity (and psi_osmo) below plant
        super().calculatePlantSalinity()

        self._plant_water_uptake = -(self._psi_leaf - self._psi_height -
                                   self._psi_osmo) / \
                                 self._total_resistance / np.pi * 1000  # kg/s
        self.belowground_resources = 1 - (self._psi_osmo /
                                          (self._psi_leaf - self._psi_height))

        # Calculate contribution per cell
        super().calculateCompletePlantContribution()

    def setExternalInformation(self, **args):
        """
        Set parameters 'cumsum_salinity' and 'calls_per_cell', which contain information about the
        cumulated salinity in each cell and the number of calls, calculated by OGS
        Args:
            **args:
        """
        # information about cell salinity from OGS
        self.cumsum_salinity = args["cumsum_salinity"]
        self.calls_per_cell = args["calls_per_cell"]
        self._salinity = self.cumsum_salinity / self.calls_per_cell

    def getExternalInformation(self):
        """
        Returns estimated water withdrawal in each cell as rate (kg per sec per cell volume)
        Returns:

        """
        return self._plant_contribution_per_cell
