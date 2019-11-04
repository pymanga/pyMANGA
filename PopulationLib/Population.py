#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from lxml import etree
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import PopulationLib as PLib


class Population(object):
    def __init__(self, args):
        self.tree_population = []

        for arg in args.iter("group"):
            self.addTreeGroup(arg)

    def addTreeGroup(self, args):
        tree_group_creator = PLib.GroupPlanting.GroupPlanting(args)
        tree_group = tree_group_creator.getGroup()
        self.tree_population.append(tree_group)

    def getTreeGroups(self):
        return self.tree_population
