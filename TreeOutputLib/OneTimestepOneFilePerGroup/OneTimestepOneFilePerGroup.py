#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeOutputLib.OneTimestepOneFile.OneTimestepOneFile import OneTimestepOneFile


## Output class. This class creates one file per timestep per group at a 
#  defined location. A line containing time, position, desired geometric 
#  measures and desired parameters is written at every nth timestep.
class OneTimestepOneFilePerGroup(OneTimestepOneFile):
    ## Writes output to predefined folder
    #  For each timestep a file is created throughout the simulation.
    #  This function is only able to work, if the output directory exists and
    #  is empty at the begin of the model run
    def writeOutput(self, tree_groups, time):
        self._output_counter = (self._output_counter %
                                self.output_each_nth_timestep)
        if self._output_counter == 0:
            for group_name, tree_group in tree_groups.items():
                filename = (group_name + "_t_%012.1f" % (time) + ".csv")
                file = open(self.output_dir + filename, "w")
                string = ""
                string += "tree,\t time,\t x,\t y"
                for geometry_output in self.geometry_outputs:
                    string += ",\t" + geometry_output
                for parameter_output in self.parameter_outputs:
                    string += ",\t" + parameter_output
                for growth_output in self.growth_outputs:
                    string += ",\t" + growth_output
                string += "\n"
                file.write(string)
                for tree in tree_group.getTrees():
                    growth_information = tree.getGrowthConceptInformation()
                    string = ""
                    string += (group_name + "_" + "%09.0d" % (tree.getId()) +
                               ",\t" + str(time) + ",\t" + str(tree.x) +
                               ",\t" + str(tree.y))
                    if (len(self.geometry_outputs) > 0):
                        geometry = tree.getGeometry()
                        for geometry_output in self.geometry_outputs:
                            string += ",\t" + str(geometry[geometry_output])
                    if (len(self.parameter_outputs) > 0):
                        parameter = tree.getParameter()
                        for parameter_output in self.parameter_outputs:
                            string += ",\t" + str(parameter[parameter_output])
                    if (len(growth_information) > 0):
                        for growth_output_key in self.growth_outputs:
                            try:
                                string += ",\t" + str(
                                    growth_information[growth_output_key])
                            except KeyError:
                                raise KeyError(
                                    "Key " + growth_output_key +
                                    " not available in growth concept!" +
                                    " Please read growth concept documentation."
                                )
                    string += "\n"
                    file.write(string)
                file.close()
        self._output_counter += 1
