#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ModelOutputLib.OneTimestepOneFile.OneTimestepOneFile import \
    OneTimestepOneFile
import os


class OneTimestepOneFilePerGroup(OneTimestepOneFile):
    """
    Model output concept.
    Create one file per group for each time step, i.e., each file contains plants of one group for each time step.
    Filename includes the group name and time step in seconds, e.g. '<group_name>_t_<time_step>'.
    Each line contains plant, time, position and user selected output parameters.
    """
    def __init__(self, args):
        """
        Args:
            args: module specifications from project file tags
        """
        super().__init__(args)

    def outputContent(self, plant_groups, time, **kwargs):
        for group_name, plant_group in plant_groups.items():
            if not plant_group.getNumberOfPlants() == 0:
                if not kwargs["group_died"]:
                    filename = (group_name + "_t_%012.1f" % (time) + ".csv")
                else:
                    filename = (group_name + "_t_%012.1f_group_died" % (time) + ".csv")

                file = open(os.path.join(self.output_dir, filename), "w")
                string = ""
                string += 'plant' + self.delimiter + 'time' + self.delimiter + 'x' +  \
                          self.delimiter + 'y'
                string = OneTimestepOneFile.addSelectedHeadings(self, string)
                string += "\n"
                file.write(string)
                for plant in plant_group.getPlants():
                    growth_information = plant.getGrowthConceptInformation()
                    string = ""
                    string += (group_name + "_" + "%09.0d" % (plant.getId()) +
                               self.delimiter + str(time) + self.delimiter + str(plant.x) +
                               self.delimiter + str(plant.y))
                    string = OneTimestepOneFile.addSelectedOutputs(
                        self, plant, string, growth_information)
                    string += "\n"
                    file.write(string)

                file.close()
