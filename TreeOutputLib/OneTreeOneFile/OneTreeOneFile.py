#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeOutputLib.TreeOutput import TreeOutput
import os


## Output class. This class creates one file per tree at a defined location.
#  A line containing time, position, desired geometric measures and desired
#  parameters is written at every nth timestep.
class OneTreeOneFile(TreeOutput):

    ## Constructor of dummy objects in order to drop output
    #  @param args xml element parsed from project to this constructor.
    def __init__(self, args):
        super().__init__(args)
        for path in os.listdir(self.output_dir):
            full_path = os.path.join(self.output_dir, path)
            if os.path.isfile(full_path):
                os.remove(full_path)

    def outputContent(self, tree_groups, time, **kwargs):
        delimiter = "\t"
        files_in_folder = os.listdir(self.output_dir)
        for group_name, tree_group in tree_groups.items():
            for tree in tree_group.getTrees():
                growth_information = tree.getGrowthConceptInformation()
                if not kwargs["group_died"]:
                    filename = (group_name + "_" + "%09.0d" % (tree.getId()) +
                                ".csv")
                else:
                    filename = (group_name + "_" + "%09.0d" % (tree.getId()) +
                                "_group_died.csv")
                file = open(os.path.join(self.output_dir, filename), "a")
                if filename not in files_in_folder:
                    string = ""
                    string += 'time' + delimiter + 'x' + delimiter + 'y'
                    string = super().addSelectedHeadings(string, delimiter)
                    string += "\n"
                    file.write(string)
                string = ""
                string += (str(time) + delimiter + str(tree.x) + delimiter +
                           str(tree.y))
                string = super().addSelectedOutputs(tree, string, delimiter,
                                                    growth_information)
                string += "\n"
                file.write(string)
                file.close()
