#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PlantModelLib.Mortality.NoGrowth import NoGrowth


class Random(NoGrowth):

    def __init__(self, args, case):
        """
        Mortality module.
        Args:
            args: module specification from project file tags
            case: "Random" (module name)
        """
        super().__init__(args, case)
        # Read input parameters from xml file
        self.getInputParameters(args)
        # Default values if no inputs are given
        try:
            self._probability
        except:
            # Annual mortality probability
            self._probability = 0.0016
            print("NOTE: Use default `probability`: " + str(self._probability) +
                  ".")

    def setSurvive(self, plant_module):
        """
        Determine if plant survives based on annual probability.
        Set attribute survival variable to 0 if plant died. Default  is 1 if plant lived.
        Args:
            plant_module (class): "PlantModel" object
        Sets:
            survival status (bool)
        """
        self._survive = 1
        r = np.random.uniform(0, 1, 1)
        # Number of time steps per year
        steps_per_year = super().getStepsPerYear(plant_module)
        ## Multiply r with the number of time steps per year to induce a
        # yearly mortality
        if r * steps_per_year < self._probability:
            self._survive = 0

    def getSurvive(self):
        """
        Get survival status of a plant.
        Returns:
            survival status (bool), 0 = plant died, 1 = plant lived.
        """
        return self._survive

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "optional": ["type", "mortality", "probability"]
        }
        super().getInputParameters(**tags)
        try:
            self._probability = self.probability
        except AttributeError:
            pass
