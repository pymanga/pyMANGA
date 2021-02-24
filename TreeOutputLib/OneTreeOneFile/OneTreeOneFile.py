#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeOutputLib.OneTimestepOneFile.OneTimestepOneFile import \
    OneTimestepOneFile
import os


## Output class. This class creates one file per tree at a defined location.
#  A line containing time, position, desired geometric measures and desired
#  parameters is written at every nth timestep.
class OneTreeOneFile(OneTimestepOneFile):
    ## Writes output to predefined folder
    #  For each tree a file is created and updated throughout the simulation.
    #  This function is only able to work, if the output directory exists and
    #  is empty at the begin of the model run
    def writeOutput(self, tree_groups, time):
        self._output_counter = (self._output_counter %
                                self.output_each_nth_timestep)
        if self._output_counter == 0:
            delimiter = "\t"
            files_in_folder = os.listdir(self.output_dir)
            for group_name, tree_group in tree_groups.items():
                for tree in tree_group.getTrees():
                    growth_information = tree.getGrowthConceptInformation()
                    filename = (group_name + "_" + "%09.0d" % (tree.getId()) +
                                ".csv")
                    file = open(os.path.join(self.output_dir, filename), "a")
                    if filename not in files_in_folder:
                        string = ""
                        string += 'time' + delimiter + 'x' + delimiter + 'y'
                        for geometry_output in self.geometry_outputs:
                            string += delimiter + geometry_output
                        for parameter_output in self.parameter_outputs:
                            string += delimiter + parameter_output
                        for growth_output in self.growth_outputs:
                            string += delimiter + growth_output
                        for network_output in self.network_outputs:
                            string += delimiter + network_output
                        string += "\n"
                        file.write(string)
                    string = ""
                    string += (str(time) + delimiter + str(tree.x) +
                               delimiter + str(tree.y))
                    if (len(self.geometry_outputs) > 0):
                        geometry = tree.getGeometry()
                        for geometry_output in self.geometry_outputs:
                            string += delimiter + str(
                                geometry[geometry_output])
                    if (len(self.parameter_outputs) > 0):
                        parameter = tree.getParameter()
                        for parameter_output in self.parameter_outputs:
                            string += delimiter + str(
                                parameter[parameter_output])
                    if (len(growth_information) > 0):
                        for growth_output_key in self.growth_outputs:
                            try:
                                string += delimiter + str(
                                    growth_information[growth_output_key])
                            except KeyError:
                                raise KeyError(
                                    "Key " + growth_output_key +
                                    " not available in growth concept!" +
                                    " Please read growth concept documentation."
                                )
                    if len(self.network_outputs) > 0:
                        network = tree.getNetwork()
                        for network_output in self.network_outputs:
                            string += delimiter + str(network[network_output])
                    string += "\n"
                    file.write(string)
                    file.close()
        self._output_counter += 1
