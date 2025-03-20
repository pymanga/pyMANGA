#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from VisualizationLib import Visualization
from PopulationLib.PopManager.Population import Population
from TimeLoopLib import DynamicTimeLoop
import numpy as np
import datetime
import importlib


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
        print("Running pyMANGA v3.1.0 - ",
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

    def importModule(self, module_name, modul_dir, prj_args):
        """
        Import modules defined in the project file
        Args:
            module_name (string): name of the module
            modul_dir (string): path to the module
            prj_args (lxml.etree._Element): module specifications from project file tags
        Returns:
            class
        """
        # Path to class
        module_full_path = modul_dir + module_name
        # Try to import class and initialize it
        try:
            module = importlib.import_module(module_full_path)
            my_class = getattr(module, module_name)
            my_instance = my_class(prj_args)
        except ModuleNotFoundError:
            print("ModuleNotFoundError: No module named '" + module_full_path + "'")
            print("Make sure the module exists and spelling is correct.")
            exit()
        return my_instance

    def iniBelowgroundResourceConcept(self):
        """
        Initialize below-ground resource concept.
        Sets:
            class
        """
        arg = self.args["belowground_resource_concept"]
        case = arg.find("type").text
        if "network" in case.lower():
            module_dir = 'ResourceLib.BelowGround.Network.'
        elif "merge" in case.lower():
            module_dir = 'ResourceLib.BelowGround.Generic.'
        else:
            module_dir = 'ResourceLib.BelowGround.Individual.'

        self.belowground_resource_concept = self.importModule(module_name=case,
                                                              modul_dir=module_dir,
                                                              prj_args=arg)
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

        module_dir = 'ResourceLib.AboveGround.'
        self.aboveground_resource_concept = self.importModule(module_name=case,
                                                              modul_dir=module_dir,
                                                              prj_args=arg)
        print("Above-ground resources: {}.".format(case))

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
        self.population_concept = Population(arg)

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
        module_dir = 'ModelOutputLib.'
        self.model_output_concept = self.importModule(module_name=case,
                                                      modul_dir=module_dir,
                                                      prj_args=arg)
        print("Model output: {}.".format(case))

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
