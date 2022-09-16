#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeOutputLib.TreeOutput import TreeOutput
import os


## Output class. This class creates one file per timestep at a defined
#  location. A line containing time, position, desired geometric measures and
#  desired parameters is written at every nth timestep.
class OneTimestepOneFile(TreeOutput):
    ## Constructor of dummy objects in order to drop output
    #  @param args xml element parsed from project to this constructor.
    def __init__(self, args):
        self.__init__subtype__(args)

    ## Writes output to predefined folder
    #  For each timestep a file is created throughout the simulation.
    #  This function is only able to work, if the output directory exists and
    #  is empty at the begin of the model run
    def writeOutput(self, tree_groups, time):
        self._output_counter = (self._output_counter %
                                self.output_each_nth_timestep)
        it_is_output_time = True
        if self.output_times is not None:
            it_is_output_time = (time in self.output_times)
        if self._output_counter == 0 and it_is_output_time:
            delimiter = "\t"
            filename = ("Population_t_%012.1f" % (time) + ".csv")
            file = open(os.path.join(self.output_dir, filename), "w")
            string = ""
            string += 'tree' + delimiter + 'time' + delimiter + 'x' + \
                      delimiter + 'y'
            string = self.addSelectedHeadings(string, delimiter)

            string += "\n"
            file.write(string)
            for group_name, tree_group in tree_groups.items():
                for tree in tree_group.getTrees():
                    growth_information = tree.getGrowthConceptInformation()
                    string = ""
                    string += (group_name + "_" + "%09.0d" % (tree.getId()) +
                               delimiter + str(time) + delimiter +
                               str(tree.x) + delimiter + str(tree.y))
                    string = self.addSelectedOutputs(tree, string, delimiter,
                                                     growth_information)
                    string += "\n"
                    file.write(string)
                    for growth_output in self.growth_outputs:
                        del (growth_information[growth_output])
            file.close()
        self._output_counter += 1


