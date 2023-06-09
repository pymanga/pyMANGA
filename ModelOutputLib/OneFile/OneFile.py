#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
import os
from ModelOutputLib.ModelOutput import ModelOutput


## Output class. This class creates one file for the whole simulation,
# i.e. each time step and plant is included.
# A line contains time, plant, position, desired geometric measures
# and parameters for every nth time step.
class OneFile(ModelOutput):

    def __init__(self, args):
        super().__init__(args)

        self.delimiter = "\t"
        self.createFileWithHeader(filename='Population.csv')

    ## Function to create csv file with selected headings
    # Check if csv file exists in directory
    # If not, create file
    def createFileWithHeader(self, filename):
        file = open(os.path.join(self.output_dir, filename), "w")

        string = ""
        string += 'plant' + self.delimiter + 'time' + self.delimiter + 'x' + \
                  self.delimiter + 'y'
        string = self.addSelectedHeadings(string, self.delimiter)

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
                string = self.addSelectedOutputs(plant, string, self.delimiter,
                                                 growth_information)
                string += "\n"
                for growth_output in self.growth_outputs:
                    del (growth_information[growth_output])
        file.write(string)
        file.close()
