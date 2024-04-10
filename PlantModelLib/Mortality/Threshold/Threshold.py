#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PlantModelLib.Mortality.NoGrowth import NoGrowth
from PlantModelLib.PlantModel import PlantModel


class Threshold(NoGrowth):
    """
    Threshold mortality module.
    """
    def __init__(self, args, case):
        """
        Args:
            args: module specification from project file tags
            case: "Threshold" (module name)
        """
        super().__init__(args, case)
        # Read input parameters from xml file
        self.getInputParameters(args)

    def setSurvive(self, plant_module):
        """
        Determine if plant survives.
        Set attribute survival variable to 0 if plant died. Default  is 1 if plant lived.
        Args:
            plant_module (class): "PlantModel" object
        Sets:
            survival status (bool)
        """
        self._survive = 1

        if self.threshold_type == "biovolume":
            print("Threshold: " + str(self.threshold))
            print("Volume: " + str(plant_module.volume))
            if plant_module.volume < self.threshold:
                self._survive = 0
        else:
            AttributeError("Threshold type not implemented.")

    def getSurvive(self):
        """
        Get survival status of a plant.
        Returns:
            survival status (bool), 0 = plant died, 1 = plant lived.
        """
        return self._survive

    def setMortalityVariables(self, plant_module, growth_concept_information):
        """
        Initiate variables that are not yet in available in the selected growth module but are required
        in this mortality module.
        Args:
            plant_module (class): "PlantModel" object
            growth_concept_information (dict): dictionary containing growth information of the respective plant
        Sets:
            value in dictionary
        """
        # Variable to store growth (m³ per time step)
        try:
            pass
        except KeyError:
            pass

    def getMortalityVariables(self, plant_module, growth_concept_information):
        """
        Get relevant plant attributes required for mortality concept.
        Args:
            plant_module (class): "PlantModel" object
            growth_concept_information (dict): dictionary containing growth information of the respective plant
        Returns:
            dictionary with updated growth concept information
        """
        # plant_module.grow_memory.append(plant_module.grow)
        # growth_concept_information["grow_memory"] = \
        #    plant_module.grow_memory
        # return growth_concept_information

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "optional": ["type", "mortality", "threshold", "threshold_type"]
        }
        super().getInputParameters(**tags)

        # Set default values if no inputs are given
        if not hasattr(self, "threshold_type"):
            self.threshold_type = "biovolume"
            print("> Set mortality parameter 'threshold_type' to default:", self.threshold_type)
