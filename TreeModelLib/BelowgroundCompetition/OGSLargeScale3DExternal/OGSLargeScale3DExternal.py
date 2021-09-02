#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

from TreeModelLib.BelowgroundCompetition.OGSLargeScale3D import OGSLargeScale3D
import numpy as np


# Child class of  OGSLargeScale3DExternal to use external time stepping
# E.g. to run MANGA as OGS boundary condition
# To function, the concept needs an array with cumulated cell salinity and
# the number of calls for each cell. It returns an array describing water
# withdrawal in each cell.
class OGSLargeScale3DExternal(OGSLargeScale3D):
    def __init__(self, args):
        super().__init__(args)

    # allow external communication
    def getOGSAccessible(self):
        return True

    ## This functions prepares the next timestep for the competition
    #  concept. In the OGS concept, information on t_ini and t_end is stored.
    #  Additionally, arrays are prepared to store information on water uptake
    #  of the participating trees. Moreover, the ogs-prj-file for the next
    #  time step is updated and saved in the ogs-project folder.
    #  @param t_ini: initial time of next time step
    #  @param t_end: end time of next time step
    def prepareNextTimeStep(self, t_ini, t_end):
        self.no_trees = 0

        # Arrays with length 'no. of trees'
        self._x = []
        self._y = []
        self._total_resistance = []

        self._psi_leaf = np.empty(0)
        self._psi_height = np.empty(0)
        self._rcrown = []
        self._hstem = []

        self._tree_cell_ids = []
        self._tree_salinity = np.empty(0)
        self.tree_water_uptake = []
        self.belowground_resources = []

        # arrays with length 'no. of cells'
        self.tree_contributions = []

    ## Before being able to calculate the resources, all tree enteties need
    #  to be added with their current implementation for the next time step.
    #  Here, in the OGS case, each tree is represented by a contribution to
    #  python source terms in OGS. To this end, their constant and salinity
    #  dependent resource uptake is saved in numpy arrays.
    #  @param tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()

        # Cells affected by tree water uptake
        affected_cells = self._cell_information.getCellIDsAtXY(x, y)
        self._tree_cell_ids.append(affected_cells)

        # Resistances against water flow in tree
        root_surface_resistance = super().rootSurfaceResistance(
            parameter, geometry)
        xylem_resistance = super().xylemResistance(
            parameter, geometry)
        total_resistance = root_surface_resistance + xylem_resistance
        self._total_resistance.append(total_resistance)

        # Water potentials
        self._psi_leaf = np.concatenate((self._psi_leaf,
                                         [(
                                          parameter["leaf_water_potential"])]))
        self._psi_height = np.concatenate((self._psi_height,
                                           [-(2 * geometry["r_crown"] +
                                              geometry["h_stem"]) *
                                            9810]))

    ## This function updates and returns BelowgroundResources in the current
    #  time step. For each tree a reduction factor is calculated which is
    #  defined as: resource uptake at zero salinity/ real resource uptake.
    def calculateBelowgroundResources(self):
        # Number of trees
        self.no_trees = len(self._total_resistance)
        # Salinity below each tree
        self._tree_salinity = np.empty(self.no_trees)
        if self.no_trees <= 0:
            print("WARNING: All trees are dead.")

        # Calculate salinity (and psi_osmo) below tree
        super().calculateTreeSalinity()

        self.tree_water_uptake = -(self._psi_leaf - self._psi_height -
                                   self._psi_osmo) / \
                                 self._total_resistance / np.pi * 1000  # kg/s
        self.belowground_resources = 1 - (self._psi_osmo /
                                          (self._psi_leaf - self._psi_height))

        # Calculate contribution per cell
        super().calculateTreeContribution()

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
        return self.tree_contributions
