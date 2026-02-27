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
    (geometry["*_thr"]).
    """

    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): XML tag for mortalityConcept (unused)
        """
        super().__init__(args)
        self.survive = 1  # Default: plant survives

    def setSurvive(self, plant_module):
        """
        Apply volume-based mortality.

        The plant dies if any of the critical geometry thresholds is not met.

        Args:
            plant_module (PlantModel): Active plant model (e.g. Saltmarsh)
        """

        self.survive = 1

        # Thresholds (species-specific, from species file)
        r_ag_thr = plant_module.r_ag_thr
        r_bg_thr = plant_module.r_bg_thr
        volume_thr = plant_module.volume_thr

        # Current state from model
        r_ag = plant_module.r_ag
        r_bg = plant_module.r_bg
        volume = plant_module.volume

        # Survival condition
        if not (
            r_ag >= r_ag_thr and
            r_bg >= r_bg_thr and
            volume >= volume_thr
        ):
            self.survive = 0  # Plant dies


    def getSurvive(self):
        """
        Get survival status of a plant.
        Returns:
            survival status (bool), 0 = plant died, 1 = plant lived.
        """
        return self.survive
