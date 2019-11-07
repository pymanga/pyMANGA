#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from ProjectLib import XMLtoProject
from TreeModelLib import AbovegroundCompetition
from TreeModelLib import BelowgroundCompetition
from TreeModelLib import GrowthAndDeathDynamics
import PopulationLib
from TimeLoopLib import TreeDynamicTimeLoop


class MangaProject(object):
    ## MangaProject defined in corresponding xml-file.
    def __init__(self, **args):
        try:
            self.prjfile = args["xml_project_file"]
        except KeyError:
            raise KeyError("XML-Project file missing!")
        xml_to_prj = XMLtoProject(**args)
        self.args = xml_to_prj.getProjectArguments()
        self.iniAbovegroundCompetition()
        self.iniBelowgroundCompetition()
        self.iniDeathAndGrowthConcept()
        self.iniPopulation()
        self.iniTreeTimeLoop()

    def getBelowgroundCompetition(self):
        return self.belowground_competition

    def iniBelowgroundCompetition(self):
        arg = self.args["belowground_competition"]
        self.belowground_competition = (BelowgroundCompetition(arg))

    def getAbovegroundCompetition(self):
        return self.aboveground_competition

    def iniAbovegroundCompetition(self):
        arg = self.args["aboveground_competition"]
        self.aboveground_competition = (AbovegroundCompetition(arg))

    def getDeathAndGrowthConcept(self):
        return self.growth_and_death_dynamics

    def iniDeathAndGrowthConcept(self):
        arg = self.args["tree_growth_and_death"]
        self.growth_and_death_dynamics = (GrowthAndDeathDynamics(arg))

    def iniPopulation(self):
        arg = self.args["initial_population"]
        self.population = (PopulationLib.Population(arg))

    def getPopulation(self):
        return self.population

    def iniTreeTimeLoop(self):
        arg = self.args["tree_time_loop"]
        self.tree_time_stepping = (TreeDynamicTimeLoop(arg))

    def getTreeTimeStepping(self):
        return self.tree_time_stepping

    def runProject(self, time_stepping):
        self.tree_time_stepping.runTimeLoop(time_stepping)


if __name__ == '__main__':
    prj = MangaProject(xml_project_file="testproject.xml")
