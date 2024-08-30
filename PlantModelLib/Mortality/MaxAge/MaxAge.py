#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PlantModelLib.Mortality.NoGrowth import NoGrowth


class MaxAge(NoGrowth):
    """
    MaxAge mortality module.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): mortality module specifications from project file tags
        """
        super().__init__(args)
        # Read input parameters from xml file
        self.getInputParameters(args)

        # Calculate annual probability to die
        self.p = 1 - self.p_max_age**(1/self.max_age)

    def setSurvive(self, plant_module):
        """
        Determine if plant survives based on annual probability to reach maximum age.
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
        if r * steps_per_year < self.p:
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
            "optional": ["type", "max_age", "p_max_age"]
        }
        super().getInputParameters(**tags)

        # Default values if no inputs are given
        if not hasattr(self, "max_age"):
            self.max_age = 300
            print("> Set mortality parameter 'max_age' to default:", self.max_age)
        if not hasattr(self, "p_max_age"):
            self.p_max_age = 0.02
            print("> Set mortality parameter 'p_max_age' to default:", self.p_max_age)
