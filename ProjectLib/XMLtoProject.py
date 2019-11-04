#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from lxml import etree


class XMLtoProject(object):
    def __init__(self, **args):
        self.prjfile = args["xml_project_file"]
        self.prj_arguments = {}
        self.readProjectFile()
        self.addTreeDynamicConcepts()

    def getProjectArguments(self):
        return self.prj_arguments

    def readProjectFile(self):
        tree = etree.parse(self.prjfile)
        self.root = tree.getroot()
        for tag in self.root.iter():
            tag.text = tag.text.strip()

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
