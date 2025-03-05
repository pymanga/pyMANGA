#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PlantModelLib.Mortality.NoGrowth import NoGrowth


class Threshold(NoGrowth):
    """
    Threshold mortality module.
    """
    def __init__(self, args):
        """
        Args:
            args: module specification from project file tags
            case: "Threshold" (module name)
        """
        super().__init__(args)
        # Read input parameters from xml file
        self.getInputParameters(args)

    def setSurvive(self, plant_module):
        """
        Checks whether the plant survives or not. If the plant volume is below the threshold, the plant dies.
        Args:
            args: module specification from project file tags
        """
        self._survive = 1

        if self.threshold_type == "biovolume":
            if plant_module.volume < self.threshold:
                self._survive = 0
        else:
            AttributeError("Threshold type not implemented.")

    def getSurvive(self):
        return self._survive

    def getInputParameters(self, args):
        """
        Get input parameters from xml file.
        Args:
            args: module specification from project file tags
        """
        tags = {
            "prj_file": args,
            "optional": ["type", "mortality", "threshold", "threshold_type"]
        }
        super().getInputParameters(**tags)

        # Set default values if no inputs are given
        if not hasattr(self, "threshold_type"):
            self.threshold_type = "biovolume"
            print("> Set mortality parameter 'threshold_type' to default:", self.threshold_type)
