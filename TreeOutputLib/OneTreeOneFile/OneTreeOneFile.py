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

    ## Constructor of dummy objects in order to drop output
    #  @param args xml element parsed from project to this constructor.
    def __init__(self, args):
        super().__init__(args)
        for path in os.listdir(self.output_dir):
            full_path = os.path.join(self.output_dir, path)
            if os.path.isfile(full_path):
                os.remove(full_path)

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
                        string = super().addSelectedHeadings(string, delimiter)
                        string += "\n"
                        file.write(string)
                    string = ""
                    string += (str(time) + delimiter + str(tree.x) +
                               delimiter + str(tree.y))
                    string = super().addSelectedOutputs(tree, string,
                                                        delimiter,
                                                        growth_information)
                    string += "\n"
                    file.write(string)
                    file.close()
        self._output_counter += 1
