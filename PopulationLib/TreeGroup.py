#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import PopulationLib as PLib

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TreeGroup:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.trees = []
        self.max_id = 0

    def addTree(self, x, y):
        self.max_id += 1
        self.trees.append(PLib.Tree(x, y, self.species, self.max_id))

    def getTrees(self):
        return self.trees

    def getNumberOfTrees(self):
        return len(self.trees)

    def removeTreesAtIndices(self, indices):
        for i in sorted(indices)[::-1]:
            self.trees.pop(i)
