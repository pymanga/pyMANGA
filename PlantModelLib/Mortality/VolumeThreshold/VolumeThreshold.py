#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PlantModelLib.Mortality.NoGrowth import NoGrowth

class VolumeThreshold(NoGrowth):
    """
    VolumeThreshold mortality module.

    Kills a plant if it does not exceed critical thresholds for:
    - aboveground radius (r_ag)
    - belowground radius (r_bg)
    - total volume (volume)

    These thresholds are specified per species in the species file
    (geometry["*_ic"]).
    """

    def __init__(self, args):
        """
        Constructor – required to match the interface, but no input
        parameters are read from XML in this concept.

        Args:
            args (lxml.etree._Element): XML tag for mortalityConcept (unused)
        """
        super().__init__(args)

    def setSurvive(self, plant_module):
        """
        Apply volume-based mortality.

        The plant dies if any of the critical geometry thresholds is not met.

        Args:
            plant_module (PlantModel): Active plant model (e.g. Saltmarsh)
            plant (Plant): The plant instance
        """

        # Thresholds (species-specific, from species file)
        r_ag_ic = plant_module.r_ag_ic
        r_bg_ic = plant_module.r_bg_ic
        volume_ic = plant_module.volume_ic

        # Current state from model
        r_ag = plant_module.r_ag
        r_bg = plant_module.r_bg
        volume = plant_module.volume

        # Survival condition
        if (
            r_ag >= r_ag_ic and
            r_bg >= r_bg_ic and
            volume >= volume_ic
        ):
            self.survive = 1  # Plant survive
        else:
            self.survive = 0  # Plant dies


    def getSurvive(self):
        """
        Get survival status of a plant.
        Returns:
            survival status (bool), 0 = plant died, 1 = plant lived.
        """
        return self.survive
