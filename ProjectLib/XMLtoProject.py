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
from ProjectLib import Project


## Creates MangaProject defined in corresponding xml-file
class XMLtoProject(Project.MangaProject):

    def __init__(self, **args):
        try:
            self.prjfile = args["xml_project_file"]
        except KeyError:
            raise KeyError("XML-Project file missing!")
        self.args = {}
        self.readProjectFile()
        self.addNumpyRandomSeed()
        self.addResourceConcept()
        self.addPlantDynamicConcept()
        self.addPopulationConcept()
        self.addPlantTimeLoopConcept()
        self.addVisualizationConcept()
        self.addModelOutputConcept()
        self.argsToProject()

    def readProjectFile(self):
        tree = etree.parse(self.prjfile)
        self.root = tree.getroot()
        #  The for loop removes ambiguous spaces of the tag arguments
        for tag in self.root.iter():
            tag.text = tag.text.strip()

    def addNumpyRandomSeed(self):
        self.args["random_seed"] = self.root.find("random_seed")

    def addResourceConcept(self):
        self.plant_dynamics = self.findChild(self.root, "resources")
        self.args["aboveground_resources_concept"] = self.findChild(
            self.plant_dynamics, "aboveground")
        self.args["belowground_resource_concept"] = self.findChild(
            self.plant_dynamics, "belowground")

    def addPlantDynamicConcept(self):
        self.args["plant_dynamics"] = self.findChild(self.root, "plant_dynamics")

    def addPopulationConcept(self):
        self.args["population"] = self.findChild(
            self.root, "population")

    def addPlantTimeLoopConcept(self):
        self.args["time_loop"] = self.findChild(self.root,
                                                     "time_loop")

    def addVisualizationConcept(self):
        self.args["visualization"] = self.findChild(self.root, "visualization")

    ## Parsing information concerning output of plant data from input-file to
    #  project arguments.
    def addModelOutputConcept(self):
        self.args["model_output"] = self.findChild(self.root, "output")

    def findChild(self, parent, key):
        child = parent.find(key)
        if child is None:
            raise KeyError("key " + key + " is missing in project file")
        return child


if __name__ == '__main__' and __package__ is None:
    prj = XMLtoProject(xml_project_file="testproject.xml")
