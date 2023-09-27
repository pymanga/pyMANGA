#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

from ResourceLib.BelowGround.Individual.OGS import OGS
import numpy as np


# Child class of OGSExternal to use external time stepping
# E.g. to run MANGA as OGS boundary condition
# The concept needs an array with cumulated cell salinity and
# the number of calls for each cell. It returns an array describing water
# withdrawal in each cell as rate in kg per sec per cell volume.
# MRO: OGSExternal, OGS, TreeModel, object
class OGSExternal(OGS):

    def __init__(self, args):
        """
        OpenGeoSys below-ground module adapted for external use.
        Args:
            args:
        """
        super().__init__(args)

    # allow external communication
    def getOGSAccessible(self):
        return True

    ## This functions prepares the next timestep for the competition
    #  concept. In the OGS concept, information on t_ini and t_end is stored.
    #  Additionally, arrays are prepared to store information on water uptake
    #  of the participating plants. Moreover, the ogs-prj-file for the next
    #  time step is updated and saved in the ogs-project folder.
    #  @param t_ini: initial time of next time step
    #  @param t_end: end time of next time step
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

    ## Before being able to calculate the resources, all plant enteties need
    #  to be added with their current implementation for the next time step.
    #  Here, in the OGS case, each plant is represented by a contribution to
    #  python source terms in OGS.
    #  @param plant
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

    ## This function updates and returns BelowgroundResources in the current
    #  time step. For each plant a reduction factor is calculated which is
    #  defined as: resource uptake at zero salinity/ real resource uptake.
    def calculateBelowgroundResources(self):
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

    ## Setter for external information
    # This function sets the parameters 'cumsum_salinity' and 'calls_per_cell',
    # which contain information about the cumulated salinity in each cell and
    # the number of calls, calculated by OGS
    def setExternalInformation(self, **args):
        # information about cell salinity from OGS
        self.cumsum_salinity = args["cumsum_salinity"]
        self.calls_per_cell = args["calls_per_cell"]
        self._salinity = self.cumsum_salinity / self.calls_per_cell

    ## Getter for external information
    # This function returns the estimated water withdrawal in each cell
    # as rate (kg per sec per cell volume)
    def getExternalInformation(self):
        return self._plant_contribution_per_cell
