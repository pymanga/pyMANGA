#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

#from TreeModelLib.AbovegroundCompetition import AbovegroundCompetition
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import XMLtoProject
else:
    from . import XMLtoProject
from TreeModelLib import AbovegroundCompetition as AC
from TreeModelLib import BelowgroundCompetition as BC
from TreeModelLib import GrowthAndDeathDynamics as GADD


class MangaProject:
    ## MangaProject defined in corresponding xml-file.
    def __init__(self, **args):
        try:
            self.prjfile = args["xml_project_file"]
        except KeyError:
            raise KeyError("XML-Project file missing!")
        xml_to_prj = XMLtoProject.XMLtoProject(**args)
        self.args = xml_to_prj.getProjectArguments()
        self.iniAbovegroundCompetition()
        self.iniBelowgroundCompetition()
        self.iniDeathAndGrowthConcept()

    def getBelowgoundCompetitionConcept(self):
        return self.belowground_competition

    def iniBelowgroundCompetition(self):
        arg = self.args["belowground_competition"]
        self.belowground_competition = (BC.BelowgroundCompetition(arg))

    def getAbovegroundCompetition(self):
        return self.aboveground_competition

    def iniAbovegroundCompetition(self):
        arg = self.args["aboveground_competition"]
        self.aboveground_competition = (AC.AbovegroundCompetition(arg))

    def getDeathAndGrowthConcept(self):
        return self.growth_and_death_dynamics

    def iniDeathAndGrowthConcept(self):
        arg = self.args["tree_growth_and_death"]
        self.growth_and_death_dynamics = (GADD.GrowthAndDeathDynamics(arg))


if __name__ == '__main__':
    prj = MangaProject(xml_project_file = "testproject.xml")
