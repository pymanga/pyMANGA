#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

import PopulationLib as PLib
from PopulationLib import TreeGroup


class Population(TreeGroup):
    def __init__(self, args):
        self.tree_groups = {}
        self.trees = []
        self.max_id = 0
        for arg in args.iter("group"):
            self.addTreeGroup(arg)

    def addTreeGroup(self, args):
        tree_group_creator = PLib.GroupPlanting(args)
        tree_group = tree_group_creator.getGroup()
        self.tree_groups[tree_group.name] = tree_group
        self.max_id += tree_group.getNumberOfTrees()

    def getTreeGroups(self):
        return self.tree_groups

    def getTreeGroup(self, name):
        return self.tree_groups[name]

    def getTrees(self):
        all_trees = []
        for name, group in self.tree_groups.items():
            for tree in group.getTrees():
                all_trees.append(tree)
        all_trees.append(self.trees)
        return all_trees

    def getNumberOfTrees(self):
        n_trees = 0
        for name, group in self.tree_groups.items():
            n_trees += group.getNumberOfTrees()
        n_trees += len(self.trees)
        return n_trees
