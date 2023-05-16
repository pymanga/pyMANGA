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

    def outputContent(self, plant_groups, time, **kwargs):
        delimiter = "\t"
        for group_name, plant_group in plant_groups.items():
            if not plant_group.getNumberOfPlants() == 0:
                if not kwargs["group_died"]:
                    filename = (group_name + "_t_%012.1f" % (time) + ".csv")
                else:
                    filename = (group_name + "_t_%012.1f_group_died" % (time) + ".csv")

                file = open(os.path.join(self.output_dir, filename), "w")
                string = ""
                string += 'plant' + delimiter + 'time' + delimiter + 'x' +  \
                          delimiter + 'y'
                string = OneTimestepOneFile.addSelectedHeadings(
                    self, string, delimiter)
                string += "\n"
                file.write(string)
                for plant in plant_group.getPlants():
                    growth_information = plant.getGrowthConceptInformation()
                    string = ""
                    string += (group_name + "_" + "%09.0d" % (plant.getId()) +
                               delimiter + str(time) + delimiter + str(plant.x) +
                               delimiter + str(plant.y))
                    string = OneTimestepOneFile.addSelectedOutputs(
                        self, plant, string, delimiter, growth_information)
                    string += "\n"
                    file.write(string)
                    for growth_output in self.growth_outputs:
                        del (growth_information[growth_output])
                file.close()
