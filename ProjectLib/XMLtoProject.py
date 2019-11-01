#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from lxml import etree


class MangaProject:
    ## MangaProject defined in corresponding xml-file.
    def __init__(self, args):
        self.args = args

    def getBelowgoundCompetitionConcept(self):
        return self.args["belowground_competition"]

    def getAbovegroundCompetitionConcept(self):
        return self.args["aboveground_competition"]

    def getDeathAndGrowthConcept(self):
        return self.args["tree_growth_and_death"]



class XMLtoProject(object):
    def __init__(self, **args):
        try:
            self.prjfile = args["xml_project_file"]
        except KeyError:
            raise KeyError("XML-Project file missing!")
        self.prj_arguments = {}
        self.readProjectFile()
        self.addTreeDynamicConcepts()
        MangaProject(self.prj_arguments)

    def readProjectFile(self):
        tree = etree.parse(self.prjfile)
        self.root = tree.getroot()

    def addTreeDynamicConcepts(self):
        self.tree_dynamics = self.findChild(self.root, "tree_dynamics")
        self.prj_arguments["aboveground_competition"] = self.findChild(
                self.tree_dynamics, "aboveground_competition")
        self.prj_arguments["belowground_competition"] = self.findChild(
                self.tree_dynamics, "aboveground_competition")
        self.prj_arguments["tree_growth_and_death"] = self.findChild(
                self.tree_dynamics, "tree_growth_and_death")

    def findChild(self, parent, key):
        child = parent.find(key)
        if child is None:
            raise KeyError("key '" + key + "' is missing in project file")
        return child


if __name__ == '__main__':
    prj = XMLtoProject(xml_project_file = "testproject.xml")
