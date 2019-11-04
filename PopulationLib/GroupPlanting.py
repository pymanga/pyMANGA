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


class GroupPlanting(object):
    def __init__(self, args):
        species = args.find("species").text
        group_name = args.find("name").text
        self.tree_group = PLib.TreeGroup.TreeGroup(group_name, species)

        distribution = args.find("distribution")
        distribution_type = distribution.find("type").text
        print("Initialise tree group " + group_name + " with " +
              distribution_type + " distribution type and trees of species " +
              species + ".")
        if distribution_type == "Random":
            self.plantRandomDistributedTrees(distribution)
        else:
            raise KeyError("Population initialisation of type " +
                           distribution_type + " not implemented!")

    def plantRandomDistributedTrees(self, args):
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "n_individuals"
        ]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "n_individuals":
                n_individuals = int(arg.text)
            elif tag == "x_1":
                x_1 = float(arg.text)
            elif tag == "x_2":
                x_2 = float(arg.text)
            elif tag == "y_1":
                y_1 = float(arg.text)
            elif tag == "y_2":
                y_2 = float(arg.text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError("Tag " + tag +
                                 " not specified for random tree planting!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for random tree planting in project file.")
        l_x = x_2 - x_1
        l_y = y_2 - y_1
        for i in range(n_individuals):
            r_x, r_y = (np.random.rand(2))
            x_i = x_1 + l_x * r_x
            y_i = y_1 + l_y * r_y
            self.tree_group.addTree(x_i, y_i)

    def getGroup(self):
        return self.tree_group
