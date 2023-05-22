#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from ModelOutputLib.ModelOutput import ModelOutput
import os


## Output class. This class creates one file per timestep at a defined
#  location. A line containing time, position, desired geometric measures and
#  desired parameters is written at every nth timestep.
class OneTimestepOneFile(ModelOutput):

    def outputContent(self, tree_groups, time, **kwargs):
        delimiter = "\t"

        if not kwargs["group_died"]:
            filename = ("Population_t_%012.1f" % (time) + ".csv")
        else:
            filename = ("Population_t_%012.1f_group_died" % (time) + ".csv")

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
                           delimiter + str(time) + delimiter + str(tree.x) +
                           delimiter + str(tree.y))
                string = self.addSelectedOutputs(tree, string, delimiter,
                                                 growth_information)
                string += "\n"
                file.write(string)
                for growth_output in self.growth_outputs:
                    del (growth_information[growth_output])
        file.close()
