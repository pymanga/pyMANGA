#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

import PopulationLib as PLib
from PopulationLib import PlantGroup


class Population(PlantGroup):

    def __init__(self, args):
        self.tree_groups = {}
        self.trees = []
        self.max_id = 0
        for arg in args.iter("group"):
            self.addPlantGroup(arg)

    def addPlantGroup(self, args):
        tree_group = PLib.GroupPlanting(args)
        self.tree_groups[tree_group.name] = tree_group
        self.max_id += tree_group.getNumberOfPlants()

    def getPlantGroups(self):
        return self.tree_groups

    def getPlantGroup(self, name):
        return self.tree_groups[name]

    def getUngroupedTrees(self):
        return self.trees

    def getPlants(self):
        all_trees = []
        for name, group in self.tree_groups.items():
            for tree in group.getPlants():
                all_trees.append(tree)
        all_trees.append(self.trees)
        return all_trees

    def getNumberOfPlants(self):
        n_trees = 0
        for name, group in self.tree_groups.items():
            n_trees += group.getNumberOfPlants()
        n_trees += len(self.trees)
        return n_trees
