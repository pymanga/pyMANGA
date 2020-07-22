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
from PopulationLib import TreeGroup


## Initializes groups of tree population and defines necessary functions.
class GroupPlanting(TreeGroup):
    ## Function initializing tree group and initial population of this group,
    #  depending on specification in project file.
    #  @param args: arguments specified in project file. Please see tag
    #  documentation.
    def __init__(self, args):
        self.species = args.find("species").text
        self.name = args.find("name").text
        self.trees = []
        self.max_id = 0

        distribution = args.find("distribution")
        distribution_type = distribution.find("type").text
        print("Initialise tree group " + self.name + " with " +
              distribution_type + " distribution type and trees of species " +
              self.species + ".")
        if distribution_type == "Random":
            self.plantRandomDistributedTrees(distribution)
        elif distribution_type == "GroupFromFile":
            self.plantTreesFromFile(distribution)
        else:
            raise KeyError("Population initialisation of type " +
                           distribution_type + " not implemented!")

    ## Function initializing tree population of size n_individuals within given
    #  rectangular domain.
    #  @param args: arguments specified in project file. Please see tag
    #  documentation.
    def plantRandomDistributedTrees(self, args):
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "n_individuals"
        ]
        #  Set default value
        self.n_recruitment = 0
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "n_individuals":
                n_individuals = int(arg.text)
            elif tag == "x_1":
                self.x_1 = float(arg.text)
            elif tag == "x_2":
                x_2 = float(arg.text)
            elif tag == "y_1":
                self.y_1 = float(arg.text)
            elif tag == "y_2":
                y_2 = float(arg.text)
            elif tag == "n_recruitment_per_step":
                self.n_recruitment = int(arg.text)
            if tag != "n_recruitment_per_step":
                try:

                    missing_tags.remove(tag)
                except ValueError:
                    raise ValueError(
                        "Tag " + tag +
                        " not specified for random tree planting!")

        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for random tree planting in project file.")
        self.l_x = x_2 - self.x_1
        self.l_y = y_2 - self.y_1
        for i in range(n_individuals):
            r_x, r_y = (np.random.rand(2))
            x_i = self.x_1 + self.l_x * r_x
            y_i = self.y_1 + self.l_y * r_y
            self.addTree(x_i, y_i)

    ## Function initializing tree population of size n_individuals within given
    #  rectangular domain.
    #  @param args: arguments specified in project file. Please see tag
    #  documentation.
    def plantTreesFromFile(self, args):
        missing_tags = ["type", "filename"]
        #  Set default value
        self.n_recruitment = 0
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "filename":
                filename = arg.text
            elif tag == "n_recruitment_per_step":
                self.n_recruitment = int(arg.text)
            if tag != "n_recruitment_per_step":
                try:
                    missing_tags.remove(tag)
                except ValueError:
                    raise ValueError(
                        "Tag " + tag +
                        " not specified for random tree planting!")

        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Mandatory tag(s) " + string +
                "is(are) not given for tree planting in project file.")

        # Loading the Population Data
        tree_file = open(filename)
        i = 0
        x_idx, y_idx = 99999, 99999
        r_crown_idx, r_stem_idx, r_root_idx, h_stem_idx = (99999, 99999, 99999,
                                                           99999)
        geometry = {}
        max_x, max_y = -99999, -99999
        min_x, min_y = 99999, 99999
        for line in tree_file.readlines():
            line = line.replace("\t", "").split(",")

            if i == 0:
                j = 0
                for tag in line:
                    tag = tag.strip()
                    print(tag)
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
                        6 - i, "Tree properties were not correctly " +
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
                self.addTree(x, y, initial_geometry=geometry)
        self.x_1 = min_x
        self.y_1 = min_y
        self.l_x = max_x - self.x_1
        self.l_y = max_y - self.y_1

    ## Randomly recruiting trees within given domain.
    def recruitTrees(self):
        for i in range(self.n_recruitment):
            r_x, r_y = (np.random.rand(2))
            x_i = self.x_1 + self.l_x * r_x
            y_i = self.y_1 + self.l_y * r_y
            self.addTree(x_i, y_i)

    ## Returns all living trees belonging to this group.
    def getGroup(self):
        return self.tree_group
