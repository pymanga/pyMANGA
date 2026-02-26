#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PlantModelLib import PlantModel
import numpy as np


class Saltmarsh(PlantModel):
    """
    Saltmarsh plant growth concept
    """

    def __init__(self, args):
        """
            args (lxml.etree._Element): Parameters from project file tags
        """
        super().iniMortalityConcept(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepares internal state for the next simulation time step.

        This includes calculation of timestep length and resetting all
        geometric growth weights to zero. These weights are later used
        to track structural changes (delta h, delta r) in AG and BG biovolume.

        Uses:
            t_ini (float): Start time of timestep [s]
            t_end (float): End time of timestep [s]
        """
        self.time = t_end - t_ini  # [s] = [s] - [s]

        # Reset growth weight variables
        self.w_h_bg = 0  # [-]
        self.w_r_bg = 0  # [-]
        self.w_h_ag = 0  # [-]
        self.w_r_ag = 0  # [-]

    def progressPlant(self, plant, aboveground_factor, belowground_factor):
        """
        Executes one time step of plant development:
        - Computes volume and maintenance costs
        - Calculates available resources
        - Performs growth allocation
        - Updates geometry
        - Applies mortality criteria

        Args:
            plant: The plant individual.
            aboveground_factor (float): AG resource availability [-] (0,1)
            belowground_factor (float): BG resource availability [-] (0,1)
        """
        # Initialization
        geometry = plant.getGeometry()
        growth_concept_information = plant.getGrowthConceptInformation()
        self.parameter = plant.getParameter()

        # Current geometry values
        self.r_ag = geometry["r_ag"]  # [m]
        self.h_ag = geometry["h_ag"]  # [m]
        self.r_bg = geometry["r_bg"]  # [m]
        self.h_bg = geometry["h_bg"]  # [m]

        self.survive = 1
        self.f_reslim_ag = aboveground_factor  # [-]
        self.f_reslim_bg = belowground_factor  # [-]

        # STEP 1: Volume calculation
        self.plantVolume()

        # STEP 2: Setup mortality-related variables (modular concept)
        super().setMortalityVariables(growth_concept_information)

        # STEP 3: Maintenance costs
        self.plantMaintenance()

        # STEP 4: Calculate resources
        self.agResources()
        self.bgResources()

        # STEP 5: Resource availability and growth potential
        self.growthResources()

        # STEP 6: Geometric growth based on resource allocation
        self.plantGrowth()

        # STEP 7: Recalculate volume after growth
        self.plantVolume()

        # STEP 8: Calculate wateruptake
        self.waterUptake()
        growth_concept_information["transpiration"] = self.transpiration

        # STEP 9: Update plant internal state
        geometry["r_ag"] = self.r_ag  # [m]
        geometry["h_ag"] = self.h_ag  # [m]
        geometry["r_bg"] = self.r_bg  # [m]
        geometry["h_bg"] = self.h_bg  # [m]

        # STEP 10: Store all relevant model variables in growth concept info
        growth_concept_information.update({
            "f_reslim_ag": self.f_reslim_ag,  #     [-]
            "f_reslim_bg": self.f_reslim_bg,  #     [-]
            "res_ag": self.res_ag,  #               [J]
            "res_bg": self.res_bg,  #               [J]
            "res_eff": self.res_eff,   #            [J]
            "grow": self.grow,  #                   [m³]
            "maint": self.maint,  #                 [m³]
            "volume": self.volume,  #               [m³]
            "w_h_bg": self.w_h_bg,  #               [-]
            "w_r_bg": self.w_r_bg,  #               [-]
            "w_h_ag": self.w_h_ag,  #               [-]
            "w_r_ag": self.w_r_ag,  #               [-]
        })

        # Calculate plant age
        try:
            growth_concept_information["age"] += self.time  # [s]
        except KeyError:
            growth_concept_information["age"] = self.time  # [s]

        # Apply mortality concept
        super().getMortalityVariables(growth_concept_information)

        # Apply all updates to the plant object
        plant.setGeometry(geometry)
        plant.setGrowthConceptInformation(growth_concept_information)

        super().setTreeKiller()

        # set survival status
        if self.survive == 1:
            plant.setSurvival(1)
        else:
            plant.setSurvival(0)

    def plantVolume(self):
        """
        Calculate total plant volume as sum of two cylinders:
        - Aboveground cylinder: h_ag, r_ag
        - Belowground cylinder: h_bg, r_bg

        Sets:
            self.V_ag (float): Aboveground volume [m^3]
            self.V_bg (float): Belowground volume [m^3]
            self.volume (float): Total plant volume [m^3]
            self.r_V_ag_bg (float): AG/BG volume ratio [-]
        Uses:
            self.r_ag (float): Aboveground radius [m]
            self.r_bg (float): Belowground radius [m]
            self.h_ag (float): Aboveground height [m]
            self.h_bg (float): Belowground height [m]
        """
        self.V_ag = np.pi * self.r_ag ** 2 * self.h_ag  # [m^3] = [-] * [m] * [m]
        self.V_bg = np.pi * self.r_bg ** 2 * self.h_bg  # [m^3] = [-] * [m] * [m]
        self.volume = self.V_ag + self.V_bg  # [m^3] = [m^3] + [m^3]
        self.r_V_ag_bg = self.V_ag / max(self.V_bg, 1e-22)  # [-] = [m^3] / [m^3]

    def plantMaintenance(self):
        """
        Calculate the maintenance cost of the plant for the current timestep.

        Maintenance is modeled as proportional to the total volume,
        scaled by a species-specific maintenance factor.

        Sets:
            self.maint (float): Maintenance cost [m³]
        Uses:
            self.volume (float): Aboveground radius [m^3]
            self.parameter["p_maint"] (float): Maintenance factor [1/s]
            self.time (float): Timestep length [s]
        """
        self.maint = self.volume * self.parameter["p_maint"] * self.time  # [m³] = [m^3] * [1/s] * [s]


    def agResources(self):
        """
        Calculate the available aboveground resources.

        AG resources depend on AG resource factor, geometry of plant and parameter p_sun.

        Sets:
            self.res_ag (float): Available aboveground resources [J]
        Uses:
            self.f_reslim_ag (float): Aboveground resource availability [-] (0,1)
            self.r_ag (float): Aboveground radius [m]
            self.parameter["p_sun"] (float): Solar radiation [J/(m^2*s)]
            self.time (float): Timestep length [s]
        """
        self.res_ag = self.f_reslim_ag * np.pi * self.r_ag**2 * self.parameter["p_sun"] * self.time  # \
        # [J] = [-] * [-] * [m^2] * [J/(m^2*s)] * [s]

    def bgResources(self):
        """
        Calculate the available belowground resources.

        AG resources depend on BG resource factor, geometry of plant and parameter p_sun and p_water.

        Sets:
            self.res_bg (float): Available belowground resources [J]
        Uses:
            self.f_reslim_bg (float): Belowground resource availability [J] (0,1)
            self.r_bg (float): Belowground radius [m]
            self.h_bg (float): Belowground height [m]
            self.h_ag (float): Aboveground height [m]
            self.paramter["p_water"] (float): Hydraulic conductivity [-]
            self.parameter["p_sun"] (float): Solar radiation [J/(m^2*s)]
            self.time (float): Timestep length [s]
        """
        self.res_bg = self.f_reslim_bg * np.pi * self.r_bg**2 * self.h_bg * self.parameter['p_sun'] *\
                            self.parameter['p_water'] * 1/(self.h_ag + 0.5 * self.h_bg) * self.time  # \
        # [J] = [-] * [-] * [m^2] * [m] * [J/(m^2*s)] * [-] * [1/(m+m)] * [s]

    def growthResources(self):
        """
        Calculate resource-limited growth potential.

        Uses the minimum of AG and BG resource availability to ensure
        symmetric limitation. Maintenance is subtracted to simulate
        baseline resource consumption.

        Sets:
            self.res_eff (float): Resources effective available for plants [J]
            self.grow_pot (float): Potential growth [m^3]
            self.grow (float): Net available resource units for growth [J]
        Uses:
            self.res_ag (float): Aboveground resource availability factor [J]
            self.res_bg (float): Belowground resource availability factor [J]
            self.parameter["p_grow"] (float): Growth factor [m^3/J]
            self.parameter["p_dieback"] (float): Dieback factor [-]
        """
        self.res_eff = min(self.res_ag, self.res_bg)  # [J] = min([J], [J])
        self.grow_pot = self.res_eff * self.parameter["p_grow"]  # \
        # [m^3] = [J] * [m^3 / J]
        self.grow = self.grow_pot - self.maint  # [m^3] = [m^3] - [m^3]
        if self.grow < 0:
            self.grow *= self.parameter["p_dieback"]

    def plantGrowth(self):
        """
        Allocate net growth into above- and belowground volumes.

        - AG/BG growth allocation is dynamically shifted based on the current volume ratio.
        - Growth is then translated into updated geometry (r, h).

        Sets:
            self.r_ag (float): Aboveground radius [m]
            self.h_ag (float): Aboveground height [m]
            self.r_bg (float): Belowground radius [m]
            self.h_bg (float): Belowground height [m]
            self.V_ag (float): Aboveground volume [m]
            self.V_bg (float): Belowground volume [m]
            ratio_vol (float): AG/BG volume ratio [-]
            self.ratio_ag_bg (float): Resource ratio from AG perspective [-] (0, 1)
            self.f_ad (float): Adjustment factor for AG/BG allocation [-]
            self.w_ratio_ag_bg (float): Weight for AG/BG allocation [-]
            V_ag_incr (float): Aboveground volume increment [m^3]
            V_bg_incr (float): Belowground volume increment [m^3]
        Uses:
            self.parameter['p_ratio_ag_bg'] (float): Species specific parameter AG/BG allocation under uniformly
            distributed resource conditions [-]
            self.parameter['p_ratio_ag'] (float): Species specific AG radius-to-height ratio [-]
            self.parameter['p_ratio_bg'] (float): Species specific BG radius-to-height ratio [-]
            self.f_reslim_ag (float): Aboveground resource limitation factor [-]
            self.f_reslim_bg (float): Belowground resource limitation factor [-]
            self.grow (float): Net available resource units for growth [m^3]
            self.V_ag (float): Current aboveground volume [m^3]
            self.V_bg (float): Current belowground volume [m^3]
        """

        ag = self.f_reslim_ag  # [-]
        bg = self.f_reslim_bg  # [-]

        # Resource ratio from AG perspective
        self.ratio_ag_bg = np.clip(ag / (ag + bg + 1e-22), 1e-6, 0.999999)

        # When growth occurs, resources are allocated appropriately between aboveground and belowground growth
        if self.grow > 0:
            # Current AG/BG volume ratio
            ratio_vol = self.V_ag / max(self.V_bg, 1e-6)

            # Adjustment factor
            self.f_ad = 0.5 - self.ratio_ag_bg

            if ratio_vol > 2.5 and self.f_ad < 0:
                pass  # AG volume too high → reduce AG growth
            elif ratio_vol < 0.15 and self.f_ad > 0:
                pass  # BG volume too high → reduce BG growth
            elif 0.15 <= ratio_vol <= 2.5:
                pass  # within target zone
            else:
                self.f_ad = 0  # prevent maladaptive adjustment

            # Compute AG/BG allocation weight
            self.w_ratio_ag_bg = self.parameter['p_ratio_ag_bg'] * (1 - self.f_ad)

            # Split net growth based on calculated ratio
            V_ag_incr = self.grow * (1 - self.w_ratio_ag_bg)
            V_bg_incr = self.grow * self.w_ratio_ag_bg

        # If the plant shrinks, aboveground and belowground biovolume decrease in equal proportions
        else:
            V_ag_incr = self.grow * 0.5
            V_bg_incr = self.grow * 0.5

        # New volumes
        self.V_ag += V_ag_incr
        self.V_bg += V_bg_incr

        # Recalculation of the geometries based on the new volumes

        self.V_ag = max(self.V_ag, 0.0)
        self.V_bg = max(self.V_bg, 0.0)

        self.h_ag = (self.V_ag / (np.pi * self.parameter['p_ratio_ag'] ** 2)) ** (1 / 3)
        self.r_ag = self.parameter['p_ratio_ag'] * self.h_ag
        self.h_bg = (self.V_bg / (np.pi * self.parameter['p_ratio_bg'] ** 2)) ** (1 / 3)
        self.r_bg = self.parameter['p_ratio_bg'] * self.h_bg

    def waterUptake(self):
        """
        Calculate transpiration (soil water uptake)

        Sets:
            self.transpiration
        Uses:
            self.volume (float): Plant volume [m^3]
            self.parameter["p_transpiration"] (float): Transpiration factor [1/s]
            self.time (float): Timestep Length [s]
        """
        self.transpiration = self.volume * self.parameter["p_transpiration"] * self.time  # [m^3] = [m^3] * [m^3/s] * [s]

    def getTranspiration(self):
        """
        Get transpiration (soil water uptake)

        Returns:
            Transpiration
        """
        return self.transpiration
