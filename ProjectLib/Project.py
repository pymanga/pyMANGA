#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from TreeModelLib.AbovegroundCompetition import AbovegroundCompetition
from . import XMLtoProject


class MangaProject:
    ## MangaProject defined in corresponding xml-file.
    def __init__(self, **args):
        try:
            self.prjfile = args["xml_project_file"]
        except KeyError:
            raise KeyError("XML-Project file missing!")
        xml_to_prj = XMLtoProject.XMLtoProject(**args)
        self.args = xml_to_prj.getProjectArguments()

    def getBelowgoundCompetitionConcept(self):
        return self.args["belowground_competition"]

    def getAbovegroundCompetitionConcept(self):
        return self.args["aboveground_competition"]

    def iniAbovegroundCompetition(self):
        arg = self.args["aboveground_competition"]
        self.AbovegroundCompetition = (
                AbovegroundCompetition.AbovegroundCompetition(arg))

    def getDeathAndGrowthConcept(self):
        return self.args["tree_growth_and_death"]




if __name__ == '__main__':
    prj = MangaProject(xml_project_file = "testproject.xml")
