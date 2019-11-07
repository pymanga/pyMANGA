#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

import PopulationLib


class Population(object):
    def __init__(self, args):
        self.tree_groups = {}

        for arg in args.iter("group"):
            self.addTreeGroup(arg)

    def addTreeGroup(self, args):
        tree_group_creator = PopulationLib.GroupPlanting(args)
        tree_group = tree_group_creator.getGroup()
        self.tree_groups[tree_group.name] = tree_group

    def getTreeGroups(self):
        return self.tree_groups

    def getTreeGroup(self, name):
        return self.tree_groups[name]

    def getAllTrees(self):
        all_trees = []
        for name, group in self.tree_groups.items():
            for tree in group.getTrees():
                all_trees.append(tree)
        return all_trees
