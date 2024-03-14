#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PlantModelLib.Mortality.Random import Random


class RandomGrowth(Random):
    """
    RandomGrowth mortality module.
    """
    def __init__(self, args, case):
        """
        Args:
            args: module specification from project file tags
            case: "RandomGrowth" (module name)
        """
        super(Random, self).__init__(args, case)
        # Read input parameters from xml file
        self.getInputParameters(args)

    def setSurvive(self, plant_module):
        """
        Determine if plant survives based on relative biomass increment per time step and the calibration factor.
        Set attribute survival variable to 0 if plant died. Default  is 1 if plant lived.
        Args:
            plant_module (class): "PlantModel" object
        Sets:
            survival status (bool)
        """
        self._survive = 1
        # Calculate the probability to die
        plant_module.delta_volume = plant_module.volume - plant_module.volume_before

        # = dV/dt/V
        relative_volume_increment = plant_module.delta_volume / (plant_module.time *
                                                         plant_module.volume)
        p_die = self.k_die / relative_volume_increment

        # Get a random number
        r = np.random.uniform(0, 1, 1)
        if r < p_die:
            self._survive = 0

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
        # Variable to store volume of previous time step (m³)
        try:
            plant_module.volume_before = growth_concept_information[
                "volume_previous_ts"]

            if plant_module.volume_before == "NaN":
                plant_module.volume_before = 0
        except KeyError:
            plant_module.volume_before = 0

    def getMortalityVariables(self, plant_module, growth_concept_information):
        """
        Get relevant plant attributes required for mortality concept.
        Args:
            plant_module (class): "PlantModel" object
            growth_concept_information (dict): dictionary containing growth information of the respective plant
        Returns:
            dictionary with updated growth concept information
        """
        # The current plant volume is the volume of t-1 in the next time step
        growth_concept_information["volume_previous_ts"] = \
            plant_module.volume
        return growth_concept_information

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "optional": ["type", "mortality", "k_die"]
        }
        super(Random, self).getInputParameters(**tags)

        # Default values if no inputs are given
        if not hasattr(self, "k_die"):
            self.k_die = 1e-12
            print("> Set mortality parameter 'k_die' to default:", self.k_die)
