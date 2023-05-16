#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from ModelOutputLib.ModelOutput import ModelOutput
import os


## Output class. This class creates one file per plant at a defined location.
#  A line containing time, position, desired geometric measures and desired
#  parameters is written at every nth timestep.
class OnePlantOneFile(ModelOutput):

    ## Constructor of dummy objects in order to drop output
    #  @param args xml element parsed from project to this constructor.
    def __init__(self, args):
        super().__init__(args)
        for path in os.listdir(self.output_dir):
            full_path = os.path.join(self.output_dir, path)
            if os.path.isfile(full_path):
                os.remove(full_path)

    def outputContent(self, plant_groups, time, **kwargs):
        delimiter = "\t"
        files_in_folder = os.listdir(self.output_dir)
        for group_name, plant_group in plant_groups.items():
            for plant in plant_group.getPlants():
                growth_information = plant.getGrowthConceptInformation()
                if not kwargs["group_died"]:
                    filename = (group_name + "_" + "%09.0d" % (plant.getId()) +
                                ".csv")
                else:
                    filename = (group_name + "_" + "%09.0d" % (plant.getId()) +
                                "_group_died.csv")
                file = open(os.path.join(self.output_dir, filename), "a")
                if filename not in files_in_folder:
                    string = ""
                    string += 'time' + delimiter + 'x' + delimiter + 'y'
                    string = super().addSelectedHeadings(string, delimiter)
                    string += "\n"
                    file.write(string)
                string = ""
                string += (str(time) + delimiter + str(plant.x) + delimiter +
                           str(plant.y))
                string = super().addSelectedOutputs(plant, string, delimiter,
                                                    growth_information)
                string += "\n"
                file.write(string)
                file.close()
