#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from ResourceLib.BelowGround.Individual.OGSLargeScale3D import OGSLargeScale3D
from os import path
import os


## OGS integration for belowground competition concept. This case is
#  using the OGS software to calculate changes in pore water salinity using
#  a detailed groundwater model. Here, no Feedback is considered.
#  @param args: Please see input file tag documentation for details
#  @date: 2019 - Today
# MRO: OGSWithoutFeedback, OGSLargeScale3D, ResourceModel, object
class OGSWithoutFeedback(OGSLargeScale3D):

    def __init__(self, args):
        super().__init__(args)
        if args.find("use_old_ogs_results") is not None:
            use_old_ogs_results = (
                args.find("use_old_ogs_results").text == "True")
            if use_old_ogs_results:
                print("pyMANGA is using old results from previously saved" +
                      " numpy arrays.")
            else:
                self.runOGSOnce()
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
        super().copyPythonScript()

        self._constant_contributions = np.zeros_like(self._volumes)
        self._salinity_prefactors = np.zeros_like(self._volumes)
        np.save(
            path.join(self._ogs_project_folder, "constant_contributions.npy"),
            self._constant_contributions)
        np.save(path.join(self._ogs_project_folder, "salinity_prefactors.npy"),
                self._salinity_prefactors)

        current_project_file = path.join(self._ogs_project_folder,
                                         "pymanga_" + self._ogs_project_file)
        self._xml_tree.write(current_project_file)
        print("Calculating belowground resources distribution using ogs...")
        bc_path = (path.dirname(path.dirname(path.abspath(__file__))))
        if not (os.system(bc_path + "/OGS/bin/ogs " + current_project_file +
                          " -o " + self._ogs_project_folder + " -l error")
                == 0):
            raise ValueError("Ogs calculation failed!")
        print("OGS-calculation done.")

    ## This function updates and returns BelowgroundResources in the current
    #  timestep. For each plant a reduction factor is calculated which is defined
    #  as: resource uptake at zero salinity/ real resource uptake.
    def calculateBelowgroundResources(self):
        super().getCellSalinity()
        for plant_id in range(len(self._plant_constant_contribution)):
            ids = self._plant_cell_ids[plant_id]
            mean_salinity_for_plant = np.mean(self._salinity[ids])
            belowground_resource = (
                (self._plant_constant_contribution[plant_id] +
                 mean_salinity_for_plant *
                 self._plant_salinity_prefactor[plant_id]) /
                self._plant_constant_contribution[plant_id])
            self.belowground_resources.append(belowground_resource)

    ## This functions prepares the next timestep for the competition
    #  concept. In the OGS concept, information on t_ini and t_end is stored.
    #  Additionally, arrays are prepared to store information on water uptake
    #  of the participating plants. Moreover, the ogs-prj-file for the next
    #  timestep is updated and saved in the ogs-project folder.
    #  @param t_ini: initial time of next timestep
    #  @param t_end: end time of next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self._t_ini = t_ini
        self._t_end = t_end
        self._xml_t_initial.text = str(self._t_ini)
        self._xml_t_end.text = str(self._t_end)
        self._plant_cell_ids = []
        self._plant_constant_contribution = []
        self._plant_salinity_prefactor = []
        self._constant_contributions = np.zeros_like(self._volumes)
        self._salinity_prefactors = np.zeros_like(self._volumes)
        self._salinity = np.zeros_like(self._volumes)
        self._t_end_list.append(self._t_end)
        try:
            self._t_ini_zero
        except AttributeError:
            self._t_ini_zero = self._t_ini
        ## List containing reduction factor for each plant
        self.belowground_resources = []
