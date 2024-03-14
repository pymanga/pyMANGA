#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from ModelOutputLib.ModelOutput import ModelOutput


class OneFile(ModelOutput):

    def __init__(self, args, time):
        """
        Model output concept.
        Create a single file for all model output.
        Each line contains plant ID, time, position and user selected output parameters.
        Args:
            args: module specifications from project file tags
        """
        super().__init__(args)
        self.createFileWithHeader(filename='Population.csv')

    def createFileWithHeader(self, filename):
        """
        Create csv file with selected headings.
        Args:
            filename (string): name of output file
        """
        file = open(os.path.join(self.output_dir, filename), "w")

        string = ""
        string += 'plant' + self.delimiter + 'time' + self.delimiter + 'x' + \
                  self.delimiter + 'y'
        string = self.addSelectedHeadings(string)

        string += "\n"
        file.write(string)

        file.close()

    def outputContent(self, plant_groups, time, **kwargs):
        if not kwargs["group_died"]:
            file = open(os.path.join(self.output_dir, 'Population.csv'), "a")
        else:
            filename = 'Population_group_died.csv'
            self.createFileWithHeader(filename=filename)
            file = open(os.path.join(self.output_dir, filename), "a")

        string = ""
        for group_name, plant_group in plant_groups.items():
            for plant in plant_group.getPlants():
                growth_information = plant.getGrowthConceptInformation()
                string += (group_name + "_" + "%09.0d" % (plant.getId()) +
                           self.delimiter + str(time) + self.delimiter +
                           str(plant.x) + self.delimiter + str(plant.y))
                string = self.addSelectedOutputs(plant, string, growth_information)
                string += "\n"

        file.write(string)
        file.close()
