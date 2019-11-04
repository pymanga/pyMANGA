#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from lxml import etree


class Tree(object):
    def __init__(self, x, y, species, tree_id):
        self.tree_id = tree_id
        self.species = species
        self.trees = []
        if species == "Avicennia":
            from PopulationLib.Species import Avicennia
            self.geometry, self.parameter = Avicennia.createTree()
        else:
            raise KeyError("Species " + species + " unknown!")

    def getGeometry(self):
        return self.geometry

    def getParameter(self):
        return self.parameter
