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
        self.args = {}
        try:
            self.prjfile = args["xml_project_file"]
            self.readProjectFile()
        except KeyError:
            try:
                tree = args["xml_tree"]
                self.xmlTextStrip(tree)
            except KeyError:
                raise KeyError("Input not correct!")
        self.addTreeDynamicConcepts()
        self.addInitialPopulation()
        self.addTreeTimeLoop()
        self.addVisualization()
        self.addTreeOutput()

        self.argsToProject()

    def readProjectFile(self):
        tree = etree.parse(self.prjfile)
        self.xmlTextStrip(tree)

    def xmlTextStrip(self, tree):
        if tree.getroot() == None:
            raise AttributeError("XML-Tree for project configuration is " +
                                 "missing.")
        self.root = tree.getroot()
        #  The for loop removes ambiguous spaces of the tag arguments
        for tag in self.root.iter():
            print(tag.text, tag)
            tag.text = tag.text.strip()

    def addTreeDynamicConcepts(self):
        self.tree_dynamics = self.findChild(self.root, "tree_dynamics")
        self.args["aboveground_competition"] = self.findChild(
            self.tree_dynamics, "aboveground_competition")
        self.args["belowground_competition"] = self.findChild(
            self.tree_dynamics, "belowground_competition")
        self.args["tree_growth_and_death"] = self.findChild(
            self.tree_dynamics, "tree_growth_and_death")

    def addInitialPopulation(self):
        self.args["initial_population"] = self.findChild(
            self.root, "initial_population")

    def addTreeTimeLoop(self):
        self.args["tree_time_loop"] = self.findChild(self.root,
                                                     "tree_time_loop")

    def addVisualization(self):
        self.args["visualization"] = self.findChild(self.root, "visualization")

    ## Parsing information concerning output of tree data from input-file to
    #  project arguments.
    def addTreeOutput(self):
        self.args["tree_output"] = self.findChild(self.root, "tree_output")

    def findChild(self, parent, key):
        child = parent.find(key)
        if child is None:
            raise KeyError("Key '" + key + "' is missing in project file")
        return child


if __name__ == '__main__' and __package__ is None:
    prj = XMLtoProject(xml_project_file="testproject.xml")
