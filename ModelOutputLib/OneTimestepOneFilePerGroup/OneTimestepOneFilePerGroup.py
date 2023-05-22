#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from ModelOutputLib.OneTimestepOneFile.OneTimestepOneFile import \
    OneTimestepOneFile
import os


## Output class. This class creates one file per timestep per group at a
#  defined location. A line containing time, position, desired geometric
#  measures and desired parameters is written at every nth timestep.
class OneTimestepOneFilePerGroup(OneTimestepOneFile):

    def outputContent(self, tree_groups, time, **kwargs):
        delimiter = "\t"
        for group_name, tree_group in tree_groups.items():
            if not tree_group.getNumberOfTrees() == 0:
                if not kwargs["group_died"]:
                    filename = (group_name + "_t_%012.1f" % (time) + ".csv")
                else:
                    filename = (group_name + "_t_%012.1f_group_died" % (time) + ".csv")

                file = open(os.path.join(self.output_dir, filename), "w")
                string = ""
                string += 'tree' + delimiter + 'time' + delimiter + 'x' +  \
                          delimiter + 'y'
                string = OneTimestepOneFile.addSelectedHeadings(
                    self, string, delimiter)
                string += "\n"
                file.write(string)
                for tree in tree_group.getTrees():
                    growth_information = tree.getGrowthConceptInformation()
                    string = ""
                    string += (group_name + "_" + "%09.0d" % (tree.getId()) +
                               delimiter + str(time) + delimiter + str(tree.x) +
                               delimiter + str(tree.y))
                    string = OneTimestepOneFile.addSelectedOutputs(
                        self, tree, string, delimiter, growth_information)
                    string += "\n"
                    file.write(string)
                    for growth_output in self.growth_outputs:
                        del (growth_information[growth_output])
                file.close()
