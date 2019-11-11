#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from TreeModelLib import AbovegroundCompetition
from TreeModelLib import BelowgroundCompetition
from TreeModelLib import GrowthAndDeathDynamics
from VisualizationLib import Visualization
import PopulationLib
from TimeLoopLib import TreeDynamicTimeLoop


class MangaProject:
    ## Parent class for MangaProjects.
    def argsToProject(self):
        self.iniAbovegroundCompetition()
        self.iniBelowgroundCompetition()
        self.iniDeathAndGrowthConcept()
        self.iniPopulation()
        self.iniTreeTimeLoop()
        self.iniVisualization()

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

    def iniVisualization(self):
        arg = self.args["visualization"]
        self.visualization = (Visualization(arg))

    def getVisualization(self):
        return self.visualization

    def runProject(self, time_stepping):
        self.tree_time_stepping.runTimeLoop(time_stepping)

    def getProjectArguments(self):
        return self.args

    def getProjectArgument(self, key):
        return self.args[key]
