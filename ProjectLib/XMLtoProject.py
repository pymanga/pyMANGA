#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from ProjectLib.Project import MangaProject


class XMLtoProject(MangaProject):
    def __init__(self, **args):
        """
        Create a pyMANGA project based on the specifications in the project file, i.e.,
        read xml tags.
        Args:
            **args (dict)
        """
        try:
            self.prjfile = args["xml_project_file"]
        except KeyError:
            raise KeyError("XML-Project file missing!")
        self.args = {}
        self.readProjectFile()
        self.addNumpyRandomSeed()
        self.addResourceConcept()
        # self.addPlantDynamicConcept()
        self.addPopulationConcept()
        self.addPlantTimeLoopConcept()
        self.addVisualizationConcept()
        self.addModelOutputConcept()
        self.argsToProject()

    def readProjectFile(self):
        """
        Construct XML tree
        """
        tree = etree.parse(self.prjfile)
        self.root = tree.getroot()
        #  The for loop removes ambiguous spaces of the tag arguments
        for tag in self.root.iter():
            tag.text = tag.text.strip()

    def addNumpyRandomSeed(self):
        """
        Store the value of the random seed.
        Sets:
            dictionary
        """
        self.args["random_seed"] = self.root.find("random_seed")

    def addResourceConcept(self):
        """
        Store the values that define above- and below-ground resource modules.
        Sets:
            dictionary
        """
        self.plant_dynamics = self.findChild(self.root, "resources")
        self.args["aboveground_resources_concept"] = self.findChild(
            self.plant_dynamics, "aboveground")
        self.args["belowground_resource_concept"] = self.findChild(
            self.plant_dynamics, "belowground")

    def addPlantDynamicConcept(self):
        """
        Store the values that define plant model module.
        Sets:
            dictionary
        """
        self.args["plant_dynamics"] = self.findChild(self.root, "plant_dynamics")

    def addPopulationConcept(self):
        """
        Store the values that define the population.
        Sets:
            dictionary
        """
        self.args["population"] = self.findChild(
            self.root, "population")

    def addPlantTimeLoopConcept(self):
        """
        Store the values that define the time loop.
        Sets:
            dictionary
        """
        self.args["time_loop"] = self.findChild(self.root,
                                                     "time_loop")

    def addVisualizationConcept(self):
        """
        Store the values that define the visualization module.
        Sets:
            dictionary
        """
        self.args["visualization"] = self.findChild(self.root, "visualization")

    def addModelOutputConcept(self):
        """
        Store the values that define the model output module.
        Sets:
            dictionary
        """
        self.args["model_output"] = self.findChild(self.root, "output")

    def findChild(self, parent, key):
        """
        Helper to find child element of XML tree element.
        Args:
            parent (lxml.etree._Element): xml tree element
            key (string): key to look for
        Returns:
            lxml.etree._Element
        """
        child = parent.find(key)
        if child is None:
            raise KeyError("key " + key + " is missing in project file")
        return child

