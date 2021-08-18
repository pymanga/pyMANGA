#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

from TreeModelLib.BelowgroundCompetition.OGSLargeScale3D import OGSLargeScale3D
import numpy as np


# Child class of  OGSLargeScale3DExternal to test external time stepping
class OGSLargeScale3DExternal(OGSLargeScale3D):
    def __init__(self, args):
        OGSLargeScale3D.__init__(self, args)

    # allow external communication
    def getOGSAccessible(self):
        return True

    def prepareNextTimeStep(self, t_ini, t_end):
        self.no_trees = 0

        # Arrays with length no. of trees
        self._x = []
        self._y = []
        self._R_total = []

        self._psi_leaf = np.empty(0)
        self._psi_height = np.empty(0)
        self._rcrown = []
        self._hstem = []

        self._tree_cell_ids = []
        self._tree_salinity = np.empty(0)
        self.tree_water_uptake = []
        self.belowground_resources = []

        # arrays with length no. of cells
        self.tree_contributions = []

    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()

        affected_cells = self._cell_information.getCellIDsAtXY(x, y)
        self._tree_cell_ids.append(affected_cells)

        root_surface_resistance = self.rootSurfaceResistance(
            parameter["lp"], parameter["k_geom"], geometry["r_root"],
            geometry["h_root"])
        xylem_resistance = self.xylemResistance(geometry["r_crown"],
                                                geometry["h_stem"],
                                                geometry["r_root"],
                                                parameter["kf_sap"],
                                                geometry["r_stem"])
        R = root_surface_resistance + xylem_resistance
        self._R_total.append(R)
        self._psi_leaf = np.concatenate((self._psi_leaf,
                                         [(
                                          parameter["leaf_water_potential"])]))
        self._psi_height = np.concatenate((self._psi_height,
                                           [-(2 * geometry["r_crown"] +
                                              geometry["h_stem"]) *
                                            9810]))

        self.no_trees = len(self._R_total)
        self._tree_salinity = np.empty(self.no_trees)

    def calculateBelowgroundResources(self):
        if self.no_trees <= 0:
            print("WARNING: All trees are dead.")
        # Calculate salinity below tree
        self.calculateTreeSalinity()
        self._psi_osmo = -self._tree_salinity * 1000 * 85000

        self.tree_water_uptake = -(self._psi_leaf - self._psi_height -
                                   self._psi_osmo) / \
                                 self._R_total / np.pi * 1000  # kg/s
        self.belowground_resources = 1 - (self._psi_osmo /
                                          (self._psi_leaf - self._psi_height))

        # Calculate contribution per cell
        self.calculateTreeContribution()

    ## Setter for external information - specify and document argument for each
    #  concept application
    #  (See XMLtoProject.py as example)
    def setExternalInformation(self, **args):
        # information about cell salinity from OGS
        self.cumsum_salinity = args["cumsum_salinity"]
        self.calls_per_cell = args["calls_per_cell"]

    ## Getter for external information
    def getExternalInformation(self):
        return self.tree_contributions

    def calculateTreeSalinity(self):
        salinity = self.cumsum_salinity / self.calls_per_cell
        for tree_id in range(self.no_trees):
            ids = self._tree_cell_ids[tree_id]
            mean_salinity_for_tree = np.mean(salinity[ids])
            self._tree_salinity[tree_id] = mean_salinity_for_tree

    def calculateTreeContribution(self):
        self.tree_contributions = np.zeros(len(self.cumsum_salinity))
        for tree_id in range(self.no_trees):
            ids = self._tree_cell_ids[tree_id]
            v = 0
            for cell_id in ids:
                v_i = self._volumes.GetTuple(cell_id)[0]
                v += v_i
            per_volume = 1. / v
            tree_contribution = self.tree_water_uptake[tree_id]
            self.tree_contributions[ids] = tree_contribution * per_volume
