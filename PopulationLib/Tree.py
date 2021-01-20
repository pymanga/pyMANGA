#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from lxml import etree
import importlib.util


class Tree:
    def __init__(self, x, y, species, tree_id, initial_geometry=False, group_name=""):
        self.tree_id = tree_id
        self.species = species
        self.trees = []
        self.x = x
        self.y = y
        self.survival = 1
        self.group_name = group_name
        if species == "Avicennia":
            from PopulationLib.Species import Avicennia
            self.geometry, self.parameter = Avicennia.createTree()
        elif "/" in species:
            try:
                spec = importlib.util.spec_from_file_location("", species)
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                self.geometry, self.parameter = foo.createTree()
            except FileNotFoundError:
                raise FileNotFoundError("The file " + species +
                                        " does not exist.")
            except AttributeError:
                raise AttributeError("The file " + species + " is not " +
                                     "correctly defining a tree species. "
                                     "Please review the file.")
        else:
            raise KeyError("Species " + species + " unknown!")
        if initial_geometry:
            self.geometry["r_crown"] = initial_geometry["r_crown"]
            self.geometry["r_root"] = initial_geometry["r_root"]
            self.geometry["r_stem"] = initial_geometry["r_stem"]
            self.geometry["h_stem"] = initial_geometry["h_stem"]
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
