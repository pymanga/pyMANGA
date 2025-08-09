#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PlantModelLib import PlantModel
import numpy as np


class Saltmarsh(PlantModel):
    """
    Saltmarsh plant module.

    This class implements an individual-based plant model for saltmarsh vegetation.
    It simulates growth and mortality based on resource availability, maintenance costs,
    geometric constraints, and dynamic feedback between above- and belowground structures.

    Growth is resource-driven and constrained by geometrical principles (cylindrical volumes),
    while mortality can be assessed via modular concepts inherited from the parent class.
    """

    def __init__(self, args):
        """
        Constructor for the Saltmarsh plant model.
        Initializes the selected mortality concept from XML specification.

        Args:
            args (lxml.etree._Element): Parameters from project file tags.
        """
        super().iniMortalityConcept(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepares internal state for the next simulation time step.

        This includes calculation of timestep length and resetting all
        geometric growth weights to zero. These weights are later used
        to track structural changes (delta h, delta r) in AG and BG organs.

        Args:
            t_ini (float): Start time of timestep.
            t_end (float): End time of timestep.
        """
        self.time = t_end - t_ini  # Duration of timestep in seconds

        # Reset growth weight variables (used to store deltas)
        self.w_h_bg = 0  # Change in belowground height
        self.w_r_bg = 0  # Change in belowground radius
        self.w_h_ag = 0  # Change in aboveground height
        self.w_r_ag = 0  # Change in aboveground radius

    def progressPlant(self, plant, aboveground_factor, belowground_factor):
        """
        Executes one time step of plant development:
        - Computes volume and maintenance costs
        - Calculates available resources
        - Performs growth allocation
        - Updates geometry
        - Applies mortality criteria

        Args:
            plant (Plant): The plant individual.
            aboveground_factor (float): AG resource availability [0,1].
            belowground_factor (float): BG resource availability [0,1].
        """
        # INITIALIZATION
        geometry = plant.getGeometry()
        growth_concept_information = plant.getGrowthConceptInformation()
        self.parameter = plant.getParameter()

        # Current geometry values
        self.r_ag = geometry["r_ag"]
        self.h_ag = geometry["h_ag"]
        self.r_bg = geometry["r_bg"]
        self.h_bg = geometry["h_bg"]
        self.r_ag_ic = geometry["r_ag_ic"]
        self.r_bg_ic = geometry["r_bg_ic"]
        self.volume_ic = geometry["volume_ic"]

        self.survive = 1  # Temporary survival flag
        self.ag_factor = aboveground_factor
        self.bg_factor = belowground_factor

        # STEP 1: Volume calculation
        self.plantVolume()

        # STEP 2: Setup mortality-related variables (modular concept)
        super().setMortalityVariables(growth_concept_information)

        # STEP 3: Maintenance costs
        self.plantMaintenance()

        # STEP 4: Resource availability and growth potential
        self.growthResources()

        # STEP 5: Geometric growth based on resource allocation
        self.plantGrowth()

        # Recalculate volume after growth
        self.plantVolume()

        # STEP 6: Update plant internal state
        geometry["r_ag"] = self.r_ag
        geometry["h_ag"] = self.h_ag
        geometry["r_bg"] = self.r_bg
        geometry["h_bg"] = self.h_bg

        # Store all relevant model variables in growth concept info
        growth_concept_information.update({
            "ag_factor": self.ag_factor,
            "bg_factor": self.bg_factor,
            "growth": self.grow,
            "maint": self.maint,
            "volume": self.volume,
            "w_h_bg": self.w_h_bg,
            "w_r_bg": self.w_r_bg,
            "w_h_ag": self.w_h_ag,
            "w_r_ag": self.w_r_ag,
            "ratio_ag": self.ratio_ag,
            "w_ratio_b_a": self.w_ratio_ag_bg,
            "adjustment": self.adjustment
        })

        # Calculate plant age
        try:
            growth_concept_information["age"] += self.time
        except KeyError:
            growth_concept_information["age"] = self.time

        # Mortality
        super().getMortalityVariables(growth_concept_information)

        # Apply all updates to the plant object
        plant.setGeometry(geometry)
        plant.setGrowthConceptInformation(growth_concept_information)

        # set survival status
        if self.survive == 1:
            plant.setSurvival(1)
        else:
            plant.setSurvival(0)

    def plantVolume(self):
        """
        Calculates total plant volume as sum of two cylinders:
        - Aboveground cylinder: h_ag, r_ag
        - Belowground cylinder: h_bg, r_bg

        Sets:
            self.V_ag (float): Aboveground volume [m³]
            self.V_bg (float): Belowground volume [m³]
            self.volume (float): Total plant volume [m³]
            self.r_V_ag_bg (float): AG/BG volume ratio [-]
        """
        self.V_ag = np.pi * self.r_ag ** 2 * self.h_ag
        self.V_bg = np.pi * self.r_bg ** 2 * self.h_bg
        self.r_V_ag_bg = self.V_ag / max(self.V_bg, 1e-6)  # Avoid division by zero
        self.volume = self.V_ag + self.V_bg

    def plantMaintenance(self):
        """
        Calculates the maintenance cost of the plant for the current timestep.

        Maintenance is modeled as proportional to the total volume,
        scaled by a species-specific maintenance factor.

        Sets:
            self.maint (float): Maintenance cost [resource units]
        """
        self.maint = self.volume * self.parameter["maint_factor"] * self.time

    def growthResources(self):
        """
        Calculates resource-limited growth potential.

        Uses the minimum of AG and BG resource availability to ensure
        symmetric limitation. Maintenance is subtracted to simulate
        baseline resource consumption.

        Sets:
            self.available_resources (float)
            self.grow (float): Net available resource units for growth.
        """
        self.available_resources = min(self.ag_factor, self.bg_factor)

        growth_potential = (self.available_resources * self.time) - self.maint
        self.grow = self.parameter["growth_factor"] * growth_potential

        # Mortality concept may adjust internal kill flags
        super().setTreeKiller()

    def plantGrowth(self):
        """
        Allocates net growth into above- and belowground volumes.

        - AG/BG allocation is dynamically shifted based on the current volume ratio.
        - Growth is then translated into updated geometry (r, h).
        - Negative growth is permitted (biomass loss under resource stress).

        Sets:
            self.r_ag, self.h_ag, self.r_bg, self.h_bg
            self.V_ag, self.V_bg
            self.ratio_ag, self.adjustment, self.w_ratio_ag_bg
        """
        ag = self.ag_factor
        bg = self.bg_factor

        # Resource ratio from AG perspective (normalized between 0 and 1)
        self.ratio_ag = np.clip(ag / (ag + bg + 1e-22), 1e-6, 0.999999)

        # Compare current AG/BG volume ratio with "optimal" range
        ratio_vol = self.V_ag / max(self.V_bg, 1e-6)

        # Shift AG/BG allocation depending on mismatch between current ratio and resource ratio
        self.adjustment = 0.5 - self.ratio_ag

        if ratio_vol > 2.5 and self.adjustment < 0:
            pass  # AG volume too high → reduce AG growth
        elif ratio_vol < 0.15 and self.adjustment > 0:
            pass  # BG volume too high → reduce BG growth
        elif 0.15 <= ratio_vol <= 2.5:
            pass  # within target zone
        else:
            self.adjustment = 0  # prevent maladaptive adjustment

        # Compute AG/BG allocation weight
        self.w_ratio_ag_bg = self.parameter['w_b_a'] * (1 - self.adjustment)

        # Split net growth based on calculated ratio
        if self.grow > 0:
            V_ag_incr = self.grow * (1 - self.w_ratio_ag_bg)
            V_bg_incr = self.grow * self.w_ratio_ag_bg
        else:
            V_ag_incr = self.grow * 0.5
            V_bg_incr = self.grow * 0.5

        self.V_ag += V_ag_incr
        self.V_bg += V_bg_incr

        # Recalculate plant geometry (cylinder geometry → invert volume formula)
        self.h_ag = (self.V_ag / (np.pi * self.parameter['w_ag'] ** 2)) ** (1 / 3)
        self.r_ag = self.parameter['w_ag'] * self.h_ag
        self.h_bg = (self.V_bg / (np.pi * self.parameter['w_bg'] ** 2)) ** (1 / 3)
        self.r_bg = self.parameter['w_bg'] * self.h_bg
