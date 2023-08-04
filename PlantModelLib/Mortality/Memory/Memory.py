#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PlantModelLib.Mortality.NoGrowth import NoGrowth
from PlantModelLib.PlantModel import PlantModel

class Memory(NoGrowth):
    def __init__(self, args, case):
        """
        Mortality module.
        Args:
            args: module specification from project file tags
            case: "Memory" (module name)
        """
        super().__init__(args, case)
        # Read input parameters from xml file
        self.getInputParameters(args)
        # Default values if no inputs are given
        try:
            self._threshold
        except:
            # Threshold for biomass increment: 0.5 %
            self._threshold = 0.5 / 100
            print("NOTE: Use default `threshold`: " + str(self._threshold) +
                  ".")
        try:
            self._period
        except:
            # Duration of growth memory: 1 year
            self._period = 1 * 365.25 * 24 * 3600
            print("NOTE: Use default `period`: " + str(self._period) + ".")

    def setSurvive(self, plant_module):
        """
        Determine if plant survives based on memory period and average growth during this period.
        Set attribute survival variable to 0 if plant died. Default  is 1 if plant lived.
        Args:
            plant_module (class): "PlantModel" object
        Sets:
            survival status (bool)
        """
        self._survive = 1

        # Get the number of values representing the memory period
        steps = int(self._period / plant_module.time)

        # Slice grow_memory array to get only relevant data
        relevant_grow_memory = plant_module.grow_memory[-steps:]
        # Check only for survival if memory exist
        if relevant_grow_memory:
            # Calculate average growth during memory period
            grow_memory = np.mean(relevant_grow_memory)

            # Calculate growth relative to biomass (volume per volume or diameter per diameter)
            relative_grow = grow_memory / plant_module.volume

            # Number of time steps per year
            steps_per_year = super().getStepsPerYear(plant_module)
            # Check if relative growth is below a certain threshold (multiply relative growth
            # with number of time steps per year to induce a yearly mortality)
            if relative_grow*steps_per_year < self._threshold:
                self._survive = 0
                print("\t Plant died (Memory).")

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
            plant_module.grow_memory = growth_concept_information["grow_memory"]
        except KeyError:
            plant_module.grow_memory = []

    def getMortalityVariables(self, plant_module, growth_concept_information):
        """
        Get relevant plant attributes required for mortality concept.
        Args:
            plant_module (class): "PlantModel" object
            growth_concept_information (dict): dictionary containing growth information of the respective plant
        Returns:
            dictionary with updated growth concept information
        """
        plant_module.grow_memory.append(plant_module.grow)
        growth_concept_information["grow_memory"] = \
            plant_module.grow_memory
        return growth_concept_information

    def getInputParameters(self, args):
        optional_tags = ["type", "mortality", "threshold", "period"]
        super().getInputParameters(args=args, optional_tags=optional_tags)
        try:
            self._threshold = self.threshold
            self._period = self.period
        except:
            pass
