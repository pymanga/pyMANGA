#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from lxml import etree


class Tree:
    def __init__(self, x, y, species, tree_id):
        self.tree_id = tree_id
        self.species = species
        self.trees = []
        self.x = x
        self.y = y
        self.survival = 1
        if species == "Avicennia":
            from PopulationLib.Species import Avicennia
            self.geometry, self.parameter = Avicennia.createTree()
        else:
            raise KeyError("Species " + species + " unknown!")
        self.growth_concept_information = {}

    def getPosition(self):
        return self.x, self.y

    def getGeometry(self):
        return self.geometry

    def setGeometry(self, geometry):
        self.geometry = geometry

    def getGrowthConceptInformation(self):
        return self.growth_concept_information

    def setGrowthConceptInformation(self, growth_concept_information):
        self.growth_concept_information = growth_concept_information

    def getParameter(self):
        return self.parameter

    def getSurvival(self):
        return self.survival

    def setSurvival(self, survival):
        self.survival = survival

    def getId(self):
        return self.tree_id
