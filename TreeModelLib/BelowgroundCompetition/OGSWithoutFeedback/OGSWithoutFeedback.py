#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition.OGSLargeScale3D import OGSLargeScale3D
from lxml import etree
from os import path
import os


## OGS integration for belowground competition concept. This case is
#  using the OGS software to calculate changes in pore water salinity using
#  a detailed groundwater model. Here, no Feedback is considered.
#  @param args: Please see input file tag documentation for details
#  @date: 2019 - Today
class OGSWithoutFeedback(OGSLargeScale3D):
    def __init__(self, args):
        super().__init__(args)
        if args.find("use_old_ogs_results"):
            use_old_ogs_results = bool(args.find("use_old_ogs_results").text)
            if use_old_ogs_results:
                print("pyMANGA is using old results from previously saved" +
                      " numpy arrays.")
        else:
            self.runOGSOnce()

    ## This function calculates the mean salinity by given abiotic drivers.
    #  The resulting salinities are used for each MANGA timestep since there is
    #  no feedback considered here..
    def runOGSOnce(self):
        try:
            print("Trying to remove previous results...")
            os.remove(
                path.join(path.dirname(path.dirname(path.abspath(__file__))),
                          "OGSWithoutFeedback/cumsum_salinity.npy"))
            os.remove(
                path.join(path.dirname(path.dirname(path.abspath(__file__))),
                          "OGSWithoutFeedback/calls_in_last_timestep.npy"))
            print("Previous results removed.")
        except FileNotFoundError:
            print("No files found.")

        self._t_end = float(self._xml_t_end.text)
        self.copyPythonScript()

        self._constant_contributions = np.zeros_like(self._volumes)
        self._salinity_prefactors = np.zeros_like(self._volumes)

        current_project_file = path.join(self._ogs_project_folder,
                                         "pymanga_" + self._ogs_project_file)
        self._tree.write(current_project_file)
        print("Calculating belowground resources distribution using ogs...")
        bc_path = (path.dirname(path.dirname(path.abspath(__file__))))
        os.system(bc_path + "/OGS/bin/ogs " + current_project_file + " -o " +
                  self._ogs_project_folder + " -l error")
        print("OGS-calculation done.")

    ## This function updates and returns BelowgroundResources in the current
    #  timestep. For each tree a reduction factor is calculated which is defined
    #  as: resource uptake at zero salinity/ real resource uptake.
    def calculateBelowgroundResources(self):

        cumsum_salinity = np.load(
            path.join(path.dirname(path.dirname(path.abspath(__file__))),
                      "OGSWithoutFeedback/cumsum_salinity.npy"))
        calls_per_cell = np.load(
            path.join(path.dirname(path.dirname(path.abspath(__file__))),
                      "OGSWithoutFeedback/calls_in_last_timestep.npy"))
        salinity = cumsum_salinity / calls_per_cell
        for tree_id in range(len(self._tree_constant_contribution)):
            ids = self._tree_cell_ids[tree_id]
            mean_salinity_for_tree = np.mean(salinity[ids])
            belowground_resource = (
                (self._tree_constant_contribution[tree_id] +
                 mean_salinity_for_tree *
                 self._tree_salinity_prefactor[tree_id]) /
                self._tree_constant_contribution[tree_id])
            self.belowground_resources.append(belowground_resource)

    ## This functions prepares the next timestep for the competition
    #  concept. In the OGS concept, information on t_ini and t_end is stored.
    #  Additionally, arrays are prepared to store information on water uptake
    #  of the participating trees. Moreover, the ogs-prj-file for the next
    #  timestep is updated and saved in the ogs-project folder.
    #  @param t_ini: initial time of next timestep
    #  @param t_end: end time of next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self._t_ini = t_ini
        self._t_end = t_end
        self._xml_t_initial.text = str(self._t_ini)
        self._xml_t_end.text = str(self._t_end)
        self._tree_cell_ids = []
        self._tree_constant_contribution = []
        self._tree_salinity_prefactor = []
        self._constant_contributions = np.zeros_like(self._volumes)
        self._salinity_prefactors = np.zeros_like(self._volumes)
        self._t_end_list.append(self._t_end)
        try:
            self._t_ini_zero
        except AttributeError:
            self._t_ini_zero = self._t_ini
        ## List containing reduction factor for each tree
        self.belowground_resources = []

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
        constants_filename = path.join(self._ogs_project_folder,
                                       "constant_contributions.npy")
        prefactors_filename = path.join(self._ogs_project_folder,
                                        "salinity_prefactors.npy")
        for line in source.readlines():
            if self._abiotic_drivers:
                for abiotic_factor in self._abiotic_drivers.iterchildren():
                    if (abiotic_factor.tag + " = ") in line:
                        line = (abiotic_factor.tag + " = " +
                                abiotic_factor.text + "\n")
            if "constant_contributions.npy" in line:
                line = line.replace("constant_contributions.npy",
                                    constants_filename)
            if "mangapath = " in line:
                line = line.replace(
                    "dummy", '"' + path.dirname(path.abspath(__file__)) + '"')
            if "salinity_prefactors.npy" in line:
                line = line.replace("salinity_prefactors.npy",
                                    prefactors_filename)
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
