#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from VisualizationLib import Visualization
from ModelOutputLib import ModelOutput
import PopulationLib
from TimeLoopLib import DynamicTimeLoop
import numpy as np


## Class to store and manage all information necessary for a MANGA model run.
class MangaProject:
    ## Parent class for MangaProjects.
    def argsToProject(self):
        self.iniNumpyRandomSeed()
        self.iniAbovegroundResourceConcept()
        self.iniBelowgroundResourceConcept()
        self.iniPlantDynamicConcept()
        self.iniPopulationConcept()
        self.iniTimeLoopConcept()
        self.iniVisualizationConcept()
        self.iniModelOutputConcept()

    def getBelowgroundResourceConcept(self):
        return self.belowground_resource_concept

    def iniNumpyRandomSeed(self):
        if self.args["random_seed"] is not None:
            print("Setting seed for random number generator.")
            _seed = int(self.args["random_seed"].text.strip())
            np.random.seed(_seed)

    def iniBelowgroundResourceConcept(self):
        arg = self.args["belowground_resource_concept"]
        case = arg.find("type").text
        if case == "SimpleTest":
            from ResourceLib.BelowGround.Individual.SimpleTest import SimpleTest as createBC
        elif case == "OGSLargeScale3D":
            from ResourceLib.BelowGround.Individual.OGSLargeScale3D import OGSLargeScale3D as createBC
        elif case == "OGSWithoutFeedback":
            from ResourceLib.BelowGround.Individual.OGSWithoutFeedback import OGSWithoutFeedback as createBC
        elif case == "FON":
            from ResourceLib.BelowGround.Individual.FON import FON as createBC
        elif case == "FixedSalinity":
            from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity as createBC
        elif case == "SymmetricZOI":
            from ResourceLib.BelowGround.Individual.SymmetricZOI import \
                SymmetricZOI as createBC
        elif case == "SZoiFixedSalinity":
            from ResourceLib.BelowGround.Individual.SZoiFixedSalinity import \
                SZoiFixedSalinity as createBC
        elif case == "Network":
            from ResourceLib.BelowGround.Network.Network import Network as createBC
        elif case == "NetworkFixedSalinity":
            from ResourceLib.BelowGround.Network.NetworkFixedSalinity import NetworkFixedSalinity as createBC
        elif case == "NetworkOGS":
            from ResourceLib.BelowGround.Network import NetworkOGS as createBC
        elif case == "OGSLargeScale3DExternal":
            from ResourceLib.BelowGround.Generic.OGSLargeScale3DExternal import OGSLargeScale3DExternal as createBC
        elif case == "NetworkOGSLargeScale3DExternal":
            from ResourceLib.BelowGround.Generic import NetworkOGSLargeScale3DExternal as createBC

        else:
            raise KeyError("Required below-ground competition case " + case +
                           " not implemented.")
        self.belowground_resource_concept = createBC(arg)
        print(case + " below-ground competition successfully initiated.")

    def getAbovegroundResourceConcept(self):
        return self.aboveground_resource_concept

    def iniAbovegroundResourceConcept(self):
        arg = self.args["aboveground_resources_concept"]
        case = arg.find("type").text
        if case == "SimpleTest":
            from ResourceLib.AboveGround.SimpleTest import SimpleTest as createAC
        elif case == "SimpleAsymmetricZOI":
            from ResourceLib.AboveGround.SimpleAsymmetricZOI import SimpleAsymmetricZOI as createAC
        else:
            raise KeyError("Required above-ground competition not implemented.")
        self.aboveground_resource_concept = createAC(arg)
        print(case + " above-ground competition successfully initiated.")

    def getPlantDynamicConcept(self):
        return self.plant_dynamic_concept

    def iniPlantDynamicConcept(self):
        arg = self.args["plant_dynamics"]
        case = arg.find("type").text
        if case == "SimpleTest":
            from PlantModelLib.SimpleTest import SimpleTest as createGD
        elif case == "Bettina":
            from PlantModelLib.Bettina import Bettina as createGD
        elif case == "SimpleKiwi":
            from PlantModelLib.SimpleKiwi import SimpleKiwi as createGD
        elif case == "BettinaNetwork":
            from PlantModelLib.BettinaNetwork import BettinaNetwork as createGD
        else:
            raise KeyError("Required plant dynamic concept not implemented.")
        self.plant_dynamic_concept = createGD(arg)
        print(case + " plant dynamic concept initiated.")

    def iniPopulationConcept(self):
        arg = self.args["population"]
        self.population_concept = (PopulationLib.Population(arg))

    def getPopulationConcept(self):
        return self.population_concept

    def iniTimeLoopConcept(self):
        arg = self.args["time_loop"]
        self.time_stepping = (DynamicTimeLoop(arg))

    def getTimeStepping(self):
        return self.time_stepping

    def iniVisualizationConcept(self):
        arg = self.args["visualization"]
        self.visualization = Visualization(arg)

    def getVisualizationConcept(self):
        return self.visualization

    ## Constructor for model output
    def iniModelOutputConcept(self):
        arg = self.args["model_output"]
        case = arg.find("type").text
        if case == "NONE":
            from ModelOutputLib.NONE import NONE as createOut
        elif case == "OneFile":
            from ModelOutputLib.OneFile import OneFile as createOut
        elif case == "OneTimestepOneFile":
            from ModelOutputLib.OneTimestepOneFile import OneTimestepOneFile as createOut
        elif case == "OnePlantOneFile":
            from ModelOutputLib.OnePlantOneFile import OnePlantOneFile as createOut
        elif case == "OneTimestepOneFilePerGroup":
            from ModelOutputLib.OneTimestepOneFilePerGroup import OneTimestepOneFilePerGroup as createOut
        else:
            raise KeyError("Required model_output of type '" + case +
                           "' not implemented!")
        print(case + " model output successfully initiated.")

        ## Containing configuration on model_output
        self.model_output_concept = createOut(arg)

    ## Returns model output defined for the project
    def getModelOutputConcept(self):
        return self.model_output_concept

    def runProject(self, time_stepping):
        self.time_stepping.runTimeLoop(time_stepping)

    def getProjectArguments(self):
        return self.args

    def getProjectArgument(self, key):
        return self.args[key]
