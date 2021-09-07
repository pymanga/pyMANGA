#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
import os
from os import path

from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork
from TreeModelLib.BelowgroundCompetition.OGSLargeScale3D import OGSLargeScale3D


class NetworkOGSLargeScale3D(SimpleNetwork, OGSLargeScale3D):

    ## OGS integration and network approach (root grafting) for below-ground
    # competition concept. This case is using OGSLargeScale3D and
    # SimpleNetwork as parent classes.
    # @param args: Please see input file tag documentation for details
    # @date: 2021 - Today
    def __init__(self, args):
        OGSLargeScale3D.__init__(self, args)
        case = args.find("type").text
        print("Initiate below-ground competition of type " + case + ".")
        self.getInputParameters(args)

    ## This functions prepares the tree variables for the
    # NetworkOGSLargeScale3D concept.\n
    #  @param t_ini - initial time for next time step \n
    #  @param t_end - end time for next time step
    def prepareNextTimeStep(self, t_ini, t_end):
        ## Load both prepartNextTimeStep methods
        # The only parameters occurring in both are t_ini and t_end and as
        # the ones from OGS are needed, OGS needs to be loaded after network
        SimpleNetwork.prepareNextTimeStep(self, t_ini, t_end)
        OGSLargeScale3D.prepareNextTimeStep(self, t_ini, t_end)

        # Initialize new variables for this concept
        self._tree_contribution = []
        self._contributions = np.zeros_like(self._volumes)
        self._tree_cell_volume = []

        self._psi_osmo = []

    ## Before being able to calculate the resources, all tree enteties need
    #  to be added with their current implementation for the next time step.
    #  Here, in the OGS case, each tree is represented by a contribution to
    #  python source terms in OGS. To this end, their resource uptake is
    #  saved in numpy arrays.
    #  @param tree
    def addTree(self, tree):
        # SimpleNetwork stuff
        SimpleNetwork.addTree(self, tree)

        # OGS stuff
        x, y = tree.getPosition()
        affected_cells = self._cell_information.getCellIDsAtXY(x, y)
        self._tree_cell_ids.append(affected_cells)
        v = 0
        for cell_id in affected_cells:
            v_i = self._volumes.GetTuple(cell_id)[0]
            v += v_i
        self._tree_cell_volume.append(v)

    ## This function creates a (dummy) array to be filled with values of
    # osmotic potential
    def addPsiOsmo(self):
        psi_osmo = self.network['psi_osmo']
        if psi_osmo:
            self._psi_osmo.append(np.array(psi_osmo))
        else:
            self._psi_osmo.append(0)

    ## This function updates and returns BelowgroundResources in the current
    #  time step. For each tree a reduction factor is calculated which is
    #  defined as: resource uptake at zero salinity and without resource
    #  sharing (root grafting)/ actual resource uptake.
    def calculateBelowgroundResources(self):
        ## SimpleNetwork stuff - calculate amount of water absorbed from
        # soil column
        # Convert psi_osmo to np array in order to use in
        # calculateBGresourcesTree()
        self._psi_osmo = np.array(self._psi_osmo)
        self.groupFormation()
        self.rootGraftFormation()
        self.calculateBGresourcesTree()

        # Map water absorbed as contribution to respective cells
        # Convert water_abs from m³/time step to kg/s
        self._tree_contribution = self._water_absorb * 1000 / self.time

        for cell_ids, volume, contribution in zip(self._tree_cell_ids,
                                                  self._tree_cell_volume,
                                                  self._tree_contribution):
            for cell_id in cell_ids:
                # a trees contribution to each cell in the grid is added a
                # source rate (kg per volume per s)
                self._contributions[cell_id] += contribution * (1 / volume)

        # OGS stuff
        self.copyPythonScript()

        np.save(path.join(self._ogs_project_folder, "contributions.npy"),
                self._contributions)

        current_project_file = path.join(
            self._ogs_project_folder,
            str(self._t_ini).replace(".", "_") + "_" + self._ogs_project_file)
        print("Running ogs...")
        bc_path = (path.dirname(path.dirname(path.abspath(__file__))))
        if not (os.system(bc_path + "/OGS/bin/ogs " + current_project_file +
                          " -o " + self._ogs_project_folder + " -l error")
                == 0):
            raise ValueError("Ogs calculation failed!")
        print("OGS-calculation done.")

        self.writePVDCollection()
        files = os.listdir(self._ogs_project_folder)
        for file in files:
            if (self._ogs_prefix.text in file
                    and ("_" + str(self._t_end)) in file):
                self._ogs_bulk_mesh.text = str(file)

        cumsum_salinity = np.load(
            path.join(self._ogs_project_folder, "cumsum_salinity.npy"))
        calls_per_cell = np.load(
            path.join(self._ogs_project_folder, "calls_in_last_timestep.npy"))

        salinity = cumsum_salinity / calls_per_cell

        ## SimpleNetwork stuff
        # Calculate bg resource factor
        res_b_noSal = self.getBGresourcesIndividual(
            self._psi_top, np.array([0] * self.no_trees),
            self._above_graft_resistance, self._below_graft_resistance)
        self.belowground_resources = self._water_avail / res_b_noSal

        # Calculate osmotic potential below tree for next time step
        for tree_id in range(len(self._tree_contribution)):
            ids = self._tree_cell_ids[tree_id]
            mean_salinity_for_tree = np.mean(salinity[ids])
            self._psi_osmo[tree_id] = -85 * 10 ** 6 * mean_salinity_for_tree

        # Update network parameters
        self.updateNetworkParametersForGrowthAndDeath()

        # OGS stuff - update ogs parameters
        parameters = self._tree.find("parameters")
        for parameter in parameters.iterchildren():
            name = parameter.find("name")
            if name.text.strip() == "c_ini":
                parameter.find("field_name").text = "concentration"

            if name.text.strip() == "p_ini":
                parameter.find("field_name").text = "pressure"

    ## This function copies the python script which defines BC and source terms
    #  to the ogs project folder.
    def copyPythonScript(self):
        if self._use_external_python_script:
            source = open(
                path.join(self._ogs_project_folder,
                          self._external_python_script), "r")
        else:
            source = open(
                path.join(path.dirname(path.abspath(__file__)),
                          "python_source.py"), "r")
        target = open(path.join(self._ogs_project_folder, "python_source.py"),
                      "w")
        contributions_filename = path.join(self._ogs_project_folder,
                                           "contributions.npy")
        cumsum_filename = path.join(self._ogs_project_folder,
                                    "cumsum_salinity.npy")
        calls_filename = path.join(self._ogs_project_folder,
                                   "calls_in_last_timestep.npy")

        for line in source.readlines():
            if self._abiotic_drivers:
                for abiotic_factor in self._abiotic_drivers.iterchildren():
                    if (abiotic_factor.tag + " = ") in line:
                        line = (abiotic_factor.tag + " = " +
                                abiotic_factor.text + "\n")
            if "contributions.npy" in line:
                line = line.replace("contributions.npy",
                                    contributions_filename)
            if "cumsum_salinity.npy" in line:
                line = line.replace("cumsum_salinity.npy", cumsum_filename)
            if "calls_in_last_timestep.npy" in line:
                line = line.replace("calls_in_last_timestep.npy",
                                    calls_filename)
            if "CellInformation(source_mesh)" in line:
                line = line.replace(
                    "source_mesh",
                    "'" + path.join(self._ogs_project_folder,
                                    self._source_mesh_name) + "'")
            if "t_write = t_end" in line:
                line = line.replace("t_end", str(self._t_end))
            target.write(line)
        source.close()
        target.close()
