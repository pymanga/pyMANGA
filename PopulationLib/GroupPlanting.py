#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import PopulationLib as PLib
from PopulationLib import PlantGroup


## Initializes groups of plant population and defines necessary functions.
class GroupPlanting(PlantGroup):
    ## Function initializing plant group and initial population of this group,
    #  depending on specification in project file.
    #  @param args: arguments specified in project file. Please see tag
    #  documentation.
    def __init__(self, args):
        self.tags_group = args
        self.species = self.tags_group.find("species").text
        self.name = self.tags_group.find("name").text
        self.plant_model = self.tags_group.find("vegetation_model_type").text
        self.plants = []
        self.max_id = 0

        distribution = self.tags_group.find("distribution")
        distribution_type = distribution.find("type").text
        self.distribution_type = distribution_type
        print("Plant group name: {}.".format(self.name) +
              "\nDistribution type: {}.".format(distribution_type) +
              "\nSpecies: {}.".format(self.species))
        if distribution_type == "Random":
            self.plantRandomDistributedPlants()
        elif distribution_type == "GroupFromFile":
            self.plantPlantsFromFile()
        else:
            raise KeyError("Population initialisation of type " +
                           distribution_type + " not implemented!")

    ## Function initializing plant population of size n_individuals within given
    #  rectangular domain.
    #  @param args: arguments specified in project file. Please see tag
    #  documentation.
    def plantRandomDistributedPlants(self):
        tags = {
            "prj_file": self.tags_group,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "n_individuals"],
            "optional": ["n_recruitment_per_step"]
        }
        self.getInputParameters(**tags)
        self.n_individuals = int(self.n_individuals)
        self.l_x = self.x_2 - self.x_1
        self.l_y = self.y_2 - self.y_1
        for i in range(self.n_individuals):
            r_x, r_y = (np.random.rand(2))
            x_i = self.x_1 + self.l_x * r_x
            y_i = self.y_1 + self.l_y * r_y
            self.addPlant(x=x_i, y=y_i, xml_args=self.tags_group,
                          plant_model=self.plant_model,
                          initial_geometry=False)

    ## Function initializing plant population of size n_individuals within given
    #  rectangular domain.
    #  @param self.tags_group: arguments specified in project file. Please see tag
    #  documentation.
    def plantPlantsFromFile(self):
        tags = {
            "prj_file": self.tags_group,
            "required": ["type", "filename"],
            "optional": ["n_recruitment_per_step"]
        }
        self.getInputParameters(**tags)

        # Loading the Population Data
        plant_file = open(self.filename)
        i = 0
        x_idx, y_idx = 99999, 99999
        r_crown_idx, r_stem_idx, r_root_idx, h_stem_idx = (99999, 99999, 99999,
                                                           99999)
        geometry = {}
        max_x, max_y = -99999, -99999
        min_x, min_y = 99999, 99999
        for line in plant_file.readlines():
            line = line.replace("\t", "").split(",")

            if i == 0:
                j = 0
                for tag in line:
                    tag = tag.strip()
                    if tag == "x" and x_idx == 99999:
                        x_idx = int(j)
                        i += 1
                    if tag == "y" and y_idx == 99999:
                        y_idx = int(j)
                        i += 1
                    if tag == "r_crown" and r_crown_idx == 99999:
                        r_crown_idx = int(j)
                        i += 1
                    if tag == "r_stem" and r_stem_idx == 99999:
                        r_stem_idx = int(j)
                        i += 1
                    if tag == "r_root" and r_root_idx == 99999:
                        r_root_idx = int(j)
                        i += 1
                    if tag == "h_stem" and h_stem_idx == 99999:
                        i += 1
                        h_stem_idx = int(j)
                    j += 1
                if i != 6:
                    raise KeyError(
                        6 - i, "Plant properties were not correctly " +
                        "indicated in the population input file! " +
                        "Please check the documentation!")
            else:
                x, y = float(line[x_idx]), float(line[y_idx])
                geometry["r_crown"] = float(line[r_crown_idx])
                geometry["r_root"] = float(line[r_root_idx])
                geometry["r_stem"] = float(line[r_stem_idx])
                geometry["h_stem"] = float(line[h_stem_idx])
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                self.addPlant(x=x, y=y, xml_args=self.tags_group,
                              plant_model=self.plant_model, initial_geometry=geometry)
        self.x_1 = min_x
        self.y_1 = min_y
        self.l_x = max_x - self.x_1
        self.l_y = max_y - self.y_1


    ## Randomly recruiting plants within given domain.
    def recruitPlants(self):
        for i in range(self.n_recruitment_per_step):
            r_x, r_y = (np.random.rand(2))
            x_i = self.x_1 + self.l_x * r_x
            y_i = self.y_1 + self.l_y * r_y
            self.addPlant(x=x_i, y=y_i, xml_args=self.tags_group,
                          plant_model=self.plant_model,
                          initial_geometry=False)

    ## Returns all living plants belonging to this group.
    def getGroup(self):
        return self.plant_group

    def getNRecruits(self):
        return self.n_recruitment_per_step

    def getInputParameters(self, **tags):
        """
        Read module tags from project file.
        Args:
            tags (dict): dictionary containing tags found in the project file as well as required and optional tags of
            the module under consideration.
        """
        try:
            prj_file_tags = tags["prj_file"]
        except KeyError:
            prj_file_tags = []
            print("WARNING: Module attributes are missing.")
        try:
            required_tags = tags["required"]
        except KeyError:
            required_tags = []
        try:
            optional_tags = tags["optional"]
        except KeyError:
            optional_tags = []

        for arg in prj_file_tags.iterdescendants():
            tag = arg.tag
            for i in range(0, len(required_tags)):
                if tag == required_tags[i]:
                    try:
                        super(GroupPlanting, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(GroupPlanting, self).__setattr__(tag, str(arg.text))
            try:
                required_tags.remove(tag)
            except ValueError:
                pass

            for i in range(0, len(optional_tags)):
                if tag == optional_tags[i]:
                    try:
                        super(GroupPlanting, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(GroupPlanting, self).__setattr__(tag, str(arg.text))

        if len(required_tags) > 0:
            string = ""
            for tag in required_tags:
                string += tag + " "
            raise KeyError(
                "Missing input parameters (in project file) for population module initialisation: " + string)

        try:
            self.n_recruitment_per_step = int(self.n_recruitment_per_step)
        except AttributeError:
            self.n_recruitment_per_step = 0
