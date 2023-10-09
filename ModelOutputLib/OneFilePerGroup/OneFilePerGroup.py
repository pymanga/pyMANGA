#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from ModelOutputLib.ModelOutput import ModelOutput


class OneFilePerGroup(ModelOutput):

    def __init__(self, args, time):
        """
        Model output concept.
        Create a single file for all model output.
        Each line contains plant ID, time, position and user selected output parameters.
        Args:
            args: module specifications from project file tags
        """
        super().__init__(args, time)
        for path in os.listdir(self.output_dir):
            full_path = os.path.join(self.output_dir, path)
            if os.path.isfile(full_path):
                os.remove(full_path)

        self.delimiter = "\t"

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
        string = self.addSelectedHeadings(string, self.delimiter)

        string += "\n"
        file.write(string)

        file.close()

    def outputContent(self, plant_groups, time, **kwargs):
        for group_name, plant_group in plant_groups.items():
            if not kwargs["group_died"]:
                filename = (group_name + "_" + "Population.csv")
            else:
                filename = (group_name + "_" + "Population.csv" +
                            "_group_died.csv")

            if not os.path.isfile(os.path.join(self.output_dir, filename)):
                self.createFileWithHeader(filename)

            file = open(os.path.join(self.output_dir, filename), "a")

            string = ""
            for plant in plant_group.getPlants():
                growth_information = plant.getGrowthConceptInformation()
                string += (group_name + "_" + "%09.0d" % (plant.getId()) +
                           self.delimiter + str(time) + self.delimiter +
                           str(plant.x) + self.delimiter + str(plant.y))
                string = self.addSelectedOutputs(plant, string, self.delimiter,
                                                 growth_information)
                string += "\n"
                for growth_output in self.growth_outputs:
                    del (growth_information[growth_output])
            file.write(string)
            file.close()
