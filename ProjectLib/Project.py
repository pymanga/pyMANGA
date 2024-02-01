#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from VisualizationLib import Visualization
import PopulationLib
from TimeLoopLib import DynamicTimeLoop
import numpy as np
import datetime


class MangaProject:
    """
    Store and manage all the information needed to run a MANGA model.
    """
    def argsToProject(self):
        """
        Initialize selected modules and pass arguments from project file.
        Sets:
            multiple dictionaries
        """
        self.iniInitiation()
        self.iniNumpyRandomSeed()
        self.iniAbovegroundResourceConcept()
        self.iniBelowgroundResourceConcept()
        self.iniPopulationConcept()
        self.iniTimeLoopConcept()
        self.iniVisualizationConcept()
        self.iniModelOutputConcept()

    def getBelowgroundResourceConcept(self):
        """
        Get below-ground resource object.
        Returns:
            class
        """
        return self.belowground_resource_concept
    
    def iniInitiation(self):
        """
        Initiate pyMANGA simulation.
        """
        print("Running pyMANGA v2.0.0 - ", 
              datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "\n==============================================",
              "\nSimulation Settings:",
              "\n--------------------")
        

    def iniNumpyRandomSeed(self):
        """
        Set random seed.
        """
        if self.args["random_seed"] is not None:
            _seed = int(self.args["random_seed"].text.strip())
            np.random.seed(_seed)
            print("Random Seed: {}.".format(_seed))

    def iniBelowgroundResourceConcept(self):
        """
        Initialize below-ground resource concept.
        Sets:
            class
        """
        arg = self.args["belowground_resource_concept"]
        case = arg.find("type").text
        if case == "Default":
            from ResourceLib.BelowGround.Individual.Default import Default as createBC
        elif case == "OGS":
            from ResourceLib.BelowGround.Individual.OGS import OGS as createBC
        elif case == "OGSWithoutFeedback":
            from ResourceLib.BelowGround.Individual.OGSWithoutFeedback import OGSWithoutFeedback as createBC
        elif case == "FON":
            from ResourceLib.BelowGround.Individual.FON import FON as createBC
        elif case == "FixedSalinity":
            from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity as createBC
        elif case == "SymmetricZOI":
            from ResourceLib.BelowGround.Individual.SymmetricZOI import \
                SymmetricZOI as createBC
        elif case == "Network":
            from ResourceLib.BelowGround.Network.Network import Network as createBC
        elif case == "NetworkFixedSalinity":
            from ResourceLib.BelowGround.Network.NetworkFixedSalinity import NetworkFixedSalinity as createBC
        elif case == "NetworkOGS":
            from ResourceLib.BelowGround.Network import NetworkOGS as createBC
        elif case == "OGSExternal":
            from ResourceLib.BelowGround.Generic.OGSExternal import OGSExternal as createBC
        elif case == "NetworkOGSExternal":
            from ResourceLib.BelowGround.Generic import NetworkOGSExternal as createBC
        elif case == "Merge":
            from ResourceLib.BelowGround.Generic import Merge as createBC
        else:
            raise KeyError("Required below-ground competition case " + case +
                           " not implemented.")
        self.belowground_resource_concept = createBC(arg)
        print("Below-ground resources: {}.".format(case))

    def getAbovegroundResourceConcept(self):
        """
        Get above-ground resource object.
        Returns:
            class
        """
        return self.aboveground_resource_concept

    def iniAbovegroundResourceConcept(self):
        """
        Initialize above-ground resource concept.
        Sets:
            class
        """
        arg = self.args["aboveground_resources_concept"]
        case = arg.find("type").text
        if case == "Default":
            from ResourceLib.AboveGround.Default import Default as createAC
        elif case == "AsymmetricZOI":
            from ResourceLib.AboveGround.AsymmetricZOI import AsymmetricZOI as createAC
        else:
            raise KeyError("Required above-ground competition not implemented.")
        self.aboveground_resource_concept = createAC(arg)
        print("Above-ground resources: {}.".format(case))

    def getSolarRadiationConcept(self):
        """
        Get radiation object.
        Returns:
            class
        """
        return self.radiation_concept
    
    def iniSolarRadiationConcept(self):
        """
        Initialize radiation concept.
        Sets:
            class
        """
        arg = self.args["radiation"]
        case = arg.find("type").text
        if case == "SolarRadiation":
            from ResourceLib.SolarRadiation.SolarRadiation import SolarRadiation as createSR
        else:
            raise KeyError("Solar radiation not implemented.")
        self.solar_radiation_concept = createSR(arg)
        print("Solar radiation: {}.".format(case))

    def getPlantDynamicConcept(self):
        """
        Get plant model object.
        Returns:
            class
        """
        return self.plant_dynamic_concept

    def iniPopulationConcept(self):
        """
        Initialize population concept.
        Sets:
            class
        """
        arg = self.args["population"]
        self.population_concept = (PopulationLib.Population(arg))

    def getPopulationConcept(self):
        """
        Get population object.
        Returns:
            class
        """
        return self.population_concept

    def iniTimeLoopConcept(self):
        """
        Initialize time loop concept.
        Sets:
            class
        """
        arg = self.args["time_loop"]
        self.time_stepping = (DynamicTimeLoop(arg))

    def getTimeStepping(self):
        """
        Get time loop object.
        Returns:
            class
        """
        return self.time_stepping

    def iniVisualizationConcept(self):
        """
        Initialize visualization concept.
        Sets:
            class
        """
        arg = self.args["visualization"]
        self.visualization = Visualization(arg)

    def getVisualizationConcept(self):
        """
        Get visualization object.
        Returns:
            class
        """
        return self.visualization

    def iniModelOutputConcept(self):
        """
        Initialize model output concept.
        Sets:
            class
        """
        arg = self.args["model_output"]
        case = arg.find("type").text
        if case == "NONE":
            from ModelOutputLib.NONE import NONE as createOut
        elif case == "OneFile":
            from ModelOutputLib.OneFile import OneFile as createOut
        elif case == "OneFilePerGroup":
            from ModelOutputLib.OneFilePerGroup import OneFilePerGroup as createOut
        elif case == "OneTimestepOneFile":
            from ModelOutputLib.OneTimestepOneFile import OneTimestepOneFile as createOut
        elif case == "OnePlantOneFile":
            from ModelOutputLib.OnePlantOneFile import OnePlantOneFile as createOut
        elif case == "OneTimestepOneFilePerGroup":
            from ModelOutputLib.OneTimestepOneFilePerGroup import OneTimestepOneFilePerGroup as createOut
        else:
            raise KeyError("Required model_output of type '" + case +
                           "' not implemented!")
        print("Model output: {}.".format(case))

        ## Containing configuration on model_output
        self.model_output_concept = createOut(arg)

    def getModelOutputConcept(self):
        """
        Get model output object.
        Returns:
            class
        """
        return self.model_output_concept

    def runProject(self, time_stepping):
        """
        Start time loop to run model.
        """
        self.time_stepping.runTimeLoop(time_stepping)

    def getProjectArguments(self):
        """
        Get module specifications from project file tags.
        Returns:
            string
        """
        return self.args

    def getProjectArgument(self, key):
        """
        Get specific module specifications from project file tags.
        Returns:
            string
        """
        return self.args[key]
