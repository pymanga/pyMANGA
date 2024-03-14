#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ModelOutputLib.ModelOutput import ModelOutput
import os


class OneTimestepOneFile(ModelOutput):
    """
    Model output concept.
    Create one file for each time step, i.e., each file contains the complete population of a single time step.
    Filename includes time step in seconds, e.g. 'Population_t_<time_step>'.
    Each line contains plant, time, position and user selected output parameters.
    """
    def __init__(self, args):
        """
        Args:
            args: module specifications from project file tags
        """
        super().__init__(args)

    def outputContent(self, plant_groups, time, **kwargs):
        if not kwargs["group_died"]:
            filename = ("Population_t_%012.1f" % (time) + ".csv")
        else:
            filename = ("Population_t_%012.1f_group_died" % (time) + ".csv")

        file = open(os.path.join(self.output_dir, filename), "w")
        string = ""
        string += 'plant' + self.delimiter + 'time' + self.delimiter + 'x' + \
                  self.delimiter + 'y'
        string = self.addSelectedHeadings(string)

        string += "\n"
        file.write(string)
        for group_name, plant_group in plant_groups.items():
            for plant in plant_group.getPlants():
                growth_information = plant.getGrowthConceptInformation()
                string = ""
                string += (group_name + "_" + "%09.0d" % (plant.getId()) +
                           self.delimiter + str(time) + self.delimiter + str(plant.x) +
                           self.delimiter + str(plant.y))
                string = self.addSelectedOutputs(plant, string, growth_information)
                string += "\n"
                file.write(string)

        file.close()
