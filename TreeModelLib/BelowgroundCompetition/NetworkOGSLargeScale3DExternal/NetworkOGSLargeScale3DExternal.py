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
from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork


class NetworkOGSLargeScale3DExternal(OGSLargeScale3DExternal,
                                     NetworkOGSLargeScale3D,
                                     SimpleNetwork):
    def __init__(self, args):
        # Load init method from NetworkOGSLargeScale3D, which includes init
        # method of OGSLargeScale3D and reading of import parameters
        NetworkOGSLargeScale3D.__init__(self, args)

    def prepareNextTimeStep(self, t_ini, t_end):
        # Load init method of SimpleNetwork and OGSLargeScale3DExternal
        SimpleNetwork.prepareNextTimeStep(self, t_ini, t_end)
        OGSLargeScale3DExternal.prepareNextTimeStep(self, t_ini, t_end)

    def addTree(self, tree):
        NetworkOGSLargeScale3D.addTree(tree)

    def calculateBelowgroundResources(self):
        # Get salinity information from OGS
        OGSLargeScale3DExternal.calculateTreeSalinity()
        self._psi_osmo = -self._tree_salinity * 1000 * 85000

        ## SimpleNetwork stuff
        # Calculate amount of water absorbed from soil column
        # Convert psi_osmo to np array in order to use in
        # calculateBGresourcesTree()
        self._psi_osmo = np.array(self._psi_osmo)
        SimpleNetwork.groupFormation()
        SimpleNetwork.rootGraftFormation()
        SimpleNetwork.calculateBGresourcesTree()

        # Calculate bg resource factor
        self.belowground_resources = NetworkOGSLargeScale3D.getBGfactor()

        # Update network parameters
        self.updateNetworkParametersForGrowthAndDeath()

        # Calculate contribution per cell
        # Map water absorbed as contribution to respective cells
        # Convert water_abs from m³/time step to kg/s
        self.tree_water_uptake = self._water_absorb * 1000 / self.time
        OGSLargeScale3DExternal.calculateTreeContribution()

    def setExternalInformation(self, **args):
        # define self.cumsum_salinity and self.calls_per_cell to get
        # salinity of each cell
        OGSLargeScale3DExternal.setExternalInformation()

    ## Getter for external information
    def getExternalInformation(self):
        return self.tree_contributions
