#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from VisualizationLib import Visualization
from TreeOutputLib import TreeOutput
import PopulationLib
from TimeLoopLib import TreeDynamicTimeLoop
import numpy as np


## Class to store and manage all information necessary for a MANGA model run.
class MangaProject:
    ## Parent class for MangaProjects.
    def argsToProject(self):
        self.iniNumpyRandomSeed()
        self.iniAbovegroundCompetition()
        self.iniBelowgroundCompetition()
        self.iniDeathAndGrowthConcept()
        self.iniPopulation()
        self.iniTreeTimeLoop()
        self.iniVisualization()
        self.iniTreeOutput()

    def getBelowgroundCompetition(self):
        return self.belowground_competition

    def iniNumpyRandomSeed(self):
        if self.args["random_seed"] is not None:
            print("Setting seed for random number generator.")
            _seed = int(self.args["random_seed"].text.strip())
            np.random.seed(_seed)

    def iniBelowgroundCompetition(self):
        arg = self.args["belowground_competition"]
        case = arg.find("type").text
        if case == "SimpleTest":
            from TreeModelLib.BelowgroundCompetition.SimpleTest import SimpleTest as createBC
        elif case == "OGSLargeScale3D":
            from TreeModelLib.BelowgroundCompetition.OGSLargeScale3D import OGSLargeScale3D as createBC
        elif case == "OGSWithoutFeedback":
            from TreeModelLib.BelowgroundCompetition.OGSWithoutFeedback import OGSWithoutFeedback as createBC
        elif case == "FON":
            from TreeModelLib.BelowgroundCompetition.FON import FON as createBC
        elif case == "FixedSalinity":
            from TreeModelLib.BelowgroundCompetition.FixedSalinity import FixedSalinity as createBC
        elif case == "SimpleNetwork":
            from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork as createBC
        elif case == "NetworkFixedSalinity":
            from TreeModelLib.BelowgroundCompetition.NetworkFixedSalinity import NetworkFixedSalinity as createBC
        elif case == "OGSLargeScale3DExternal":
            from TreeModelLib.BelowgroundCompetition.OGSLargeScale3DExternal import OGSLargeScale3DExternal as createBC
        elif case == "NetworkOGSLargeScale3D":
            from TreeModelLib.BelowgroundCompetition.NetworkOGSLargeScale3D import \
                NetworkOGSLargeScale3D as createBC
        elif case == "NetworkOGSLargeScale3DExternal":
            from TreeModelLib.BelowgroundCompetition.NetworkOGSLargeScale3DExternal\
                import NetworkOGSLargeScale3DExternal as createBC
        elif case == "SymmetricZOI":
            from TreeModelLib.BelowgroundCompetition.SymmetricZOI import \
                SymmetricZOI as createBC
        elif case == "SZoiFixedSalinity":
            from TreeModelLib.BelowgroundCompetition.SZoiFixedSalinity import \
                SZoiFixedSalinity as createBC
        else:
            raise KeyError("Required belowground competition case " + case +
                           " not implemented.")
        self.belowground_competition = createBC(arg)
        print(case + " belowground competition successfully initiated.")

    def getAbovegroundCompetition(self):
        return self.aboveground_competition

    def iniAbovegroundCompetition(self):
        arg = self.args["aboveground_competition"]
        case = arg.find("type").text
        if case == "SimpleTest":
            from TreeModelLib.AbovegroundCompetition.SimpleTest import SimpleTest as createAC
        elif case == "SimpleAsymmetricZOI":
            from TreeModelLib.AbovegroundCompetition.SimpleAsymmetricZOI import SimpleAsymmetricZOI as createAC
        else:
            raise KeyError("Required aboveground competition not implemented.")
        self.aboveground_competition = createAC(arg)
        print(case + " aboveground competition successfully initiated.")

    def getDeathAndGrowthConcept(self):
        return self.growth_and_death_dynamics

    def iniDeathAndGrowthConcept(self):
        arg = self.args["tree_growth_and_death"]
        case = arg.find("type").text
        if case == "SimpleTest":
            from PlantModelLib.SimpleTest import SimpleTest as createGD
        elif case == "SimpleBettina":
            from PlantModelLib.SimpleBettina import SimpleBettina as createGD
        elif case == "SimpleKiwi":
            from PlantModelLib.SimpleKiwi import SimpleKiwi as createGD
        elif case == "NetworkBettina":
            from PlantModelLib.NetworkBettina import NetworkBettina as createGD
        else:
            raise KeyError("Required growth and death not implemented.")
        self.growth_and_death_dynamics = createGD(arg)
        print(case + " growth and death dynamics initiated.")

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
        self.visualization = Visualization(arg)

    def getVisualization(self):
        return self.visualization

    ## Constructor for tree output
    def iniTreeOutput(self):
        arg = self.args["tree_output"]
        case = arg.find("type").text
        if case == "NONE":
            from TreeOutputLib.NONE import NONE as createOut
        elif case == "OneFile":
            from TreeOutputLib.OneFile import OneFile as createOut
        elif case == "OneTimestepOneFile":
            from TreeOutputLib.OneTimestepOneFile import OneTimestepOneFile as createOut
        elif case == "OneTreeOneFile":
            from TreeOutputLib.OneTreeOneFile import OneTreeOneFile as createOut
        elif case == "OneTimestepOneFilePerGroup":
            from TreeOutputLib.OneTimestepOneFilePerGroup import OneTimestepOneFilePerGroup as createOut
        else:
            raise KeyError("Required tree_output of type '" + case +
                           "' not implemented!")
        print(case + " tree output sucesscully initiated.")

        ## Containing configuration on tree_output
        self.tree_output = createOut(arg)

    ## Returns tree output defined for the project
    def getTreeOutput(self):
        return self.tree_output

    def runProject(self, time_stepping):
        self.tree_time_stepping.runTimeLoop(time_stepping)

    def getProjectArguments(self):
        return self.args

    def getProjectArgument(self, key):
        return self.args[key]
