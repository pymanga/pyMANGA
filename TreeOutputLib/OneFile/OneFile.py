#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
import os
from TreeOutputLib.OneTimestepOneFile.OneTimestepOneFile import OneTimestepOneFile


## Output class. This class creates one file for the whole simulation,
# i.e. each time step and tree is included.
# A line contains time, tree, position, desired geometric measures
# and parameters for every nth time step.
class OneFile(OneTimestepOneFile):
    def __init__(self, args):
        OneTimestepOneFile.__init__(self, args)

    def writeOutput(self, tree_groups, time):
        self._output_counter = (self._output_counter %
                                self.output_each_nth_timestep)
        files_in_folder = os.listdir(self.output_dir)

        if self._output_counter == 0:
            delimiter = "\t"
            filename = "Population.csv"
            file = open(os.path.join(self.output_dir, filename), "a")

            if filename not in files_in_folder:
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
