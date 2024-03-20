# first approach saltmarsh model

from PlantModelLib import PlantModel
import numpy as np


class Saltmarsh(PlantModel):
    def __init__(self, args):
        """
        Plant model concept.
        Args:
            args: Saltmarsh module specifications from project file tags
        """
        super().iniMortalityConcept(args)
        self.sickly = False

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepare next time step by initializing relevant variables.
        Args:
            t_ini (int): start of current time step in seconds
            t_end (int): end of current time step in seconds
        """
        self.time = t_end - t_ini
        self.w_h_bg = 0
        self.w_r_bg = 0
        self.w_h_ag = 0
        self.w_r_ag = 0

    def progressPlant(self, plant, aboveground_factor, belowground_factor):
        """
        Manage growth procedures for a timestep --- read plant geometry and parameters,
        schedule computations, and update plant geometry and survival.
        Args:
            plant (dict): plant object
            aboveground_factor (float): aboveground resource growth reduction factor
            belowground_factor (float): belowground resource growth reduction factor
        """
        geometry = plant.getGeometry()
        growth_concept_information = plant.getGrowthConceptInformation()
        self.parameter = plant.getParameter()
        self.r_ag = geometry["r_ag"]
        self.h_ag = geometry["h_ag"]
        self.r_bg = geometry["r_bg"]
        self.h_bg = geometry["h_bg"]
        self.max_h = self.parameter["max_h"]
        self.survive = 1
        self.ag_factor = aboveground_factor
        self.bg_factor = belowground_factor

        self.plantVolume()

        # Define variables that are only required for specific Mortality
        # concepts
        super().setMortalityVariables(growth_concept_information)

        self.plantMaintenance()
        self.growthResources()
        self.plantGrowthWeights()
        self.plantGrowth()

        geometry["r_ag"] = self.r_ag
        geometry["h_ag"] = self.h_ag
        geometry["r_bg"] = self.r_bg
        geometry["h_bg"] = self.h_bg
        growth_concept_information["ag_factor"] = self.ag_factor
        growth_concept_information["bg_factor"] = self.bg_factor
        growth_concept_information["growth"] = self.grow
        growth_concept_information["maint"] = self.maint
        growth_concept_information["volume"] = self.volume

        growth_concept_information["w_h_bg"] = self.w_h_bg
        growth_concept_information["w_r_bg"] = self.w_r_bg
        growth_concept_information["w_h_ag"] = self.w_h_ag
        growth_concept_information["w_r_ag"] = self.w_r_ag

        # Get Mortality-related variables
        super().getMortalityVariables(growth_concept_information)

        plant.setGeometry(geometry)
        plant.setGrowthConceptInformation(growth_concept_information)

        if self.survive == 1:
            plant.setSurvival(1)
        else:
            plant.setSurvival(0)

    def plantGrowth(self):
        """
        Growth of the different geometries of the plant.
        Sets:
            floats
        """
        self.inc_h_ag = self.w_h_ag * self.grow
        if self.h_ag + self.inc_h_ag < self.max_h:
            self.h_ag += self.inc_h_ag

            self.inc_r_ag = self.w_r_ag * self.grow
            self.r_ag += self.inc_r_ag

            self.inc_r_bg = self.w_r_bg * self.grow
            self.r_bg += self.inc_r_bg

            self.inc_h_bg = self.w_h_bg * self.grow
            self.h_bg += self.inc_h_bg
        else:
            self.inc_r_ag = 0
            self.inc_h_ag = 0
            self.inc_r_bg = 0
            self.inc_h_bg = 0

    def plantGrowthWeights(self):
        """
        Calculation of the growth weights for the different geometries of the plant.
        Sets:
            float
        """
        if self.bg_factor != 0 or self.ag_factor != 0:
            ratio_b_a_resource = ((self.bg_factor /
                                   (self.bg_factor + self.ag_factor)) - 0.5) / 5
            w_ratio_b_a = self.parameter['w_b_a'] * (1 + ratio_b_a_resource)

            self.w_r_ag = w_ratio_b_a * self.parameter['w_ag']
            self.w_h_ag = w_ratio_b_a * (1 - self.parameter['w_ag'])
            self.w_r_bg = self.parameter['w_bg'] * (1 - w_ratio_b_a)
            self.w_h_bg = (1 - w_ratio_b_a) * (1 - self.parameter['w_bg'])

    def plantMaintenance(self):
        """
        Calculate the maintenance of the plant.
        Sets:
            float
        """
        self.maint = self.volume * self.parameter["maint_factor"] * self.time

    def plantVolume(self):
        """
        Calculate the total plant volume.
        Sets:
            float
        """
        volume_ag = np.pi * self.r_ag ** 2 * self.h_ag
        volume_bg = np.pi * self.r_bg ** 2 * self.h_bg
        self.r_volum_ag_bg = volume_ag / volume_bg
        self.volume = volume_ag + volume_bg

    def growthResources(self):
        """
        calculates the resources available for growth and the growth factor.
        Sets:
            floats
        """
        self.available_resources = min(self.ag_factor, self.bg_factor) * self.time

        self.grow = self.parameter["growth_factor"] * (self.available_resources - self.maint)
        # Check if trees survive based on selected mortality concepts
        super().setTreeKiller()
