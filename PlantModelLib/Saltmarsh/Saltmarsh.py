# first approach saltmarsh model

from PlantModelLib import PlantModel
import numpy as np


class Saltmarsh(PlantModel):
    """
    Saltmarsh plant module.
    """
    def __init__(self, args):
        """
        Saltmarsh plant model concept.
        Args:
            args: Saltmarsh module specifications from project file tags
        """
        super().iniMortalityConcept(args)

    def prepareNextTimeStep(self, t_ini, t_end):

        # timestep length
        self.time = t_end - t_ini

        # growth weights
        self.w_h_bg = 0
        self.w_r_bg = 0
        self.w_h_ag = 0
        self.w_r_ag = 0

    def progressPlant(self, plant, aboveground_factor, belowground_factor):

        geometry = plant.getGeometry()
        growth_concept_information = plant.getGrowthConceptInformation()
        self.parameter = plant.getParameter()
        self.r_ag = geometry["r_ag"]
        self.h_ag = geometry["h_ag"]
        self.r_bg = geometry["r_bg"]
        self.h_bg = geometry["h_bg"]
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
        self.h_ag += self.inc_h_ag

        self.inc_r_ag = self.w_r_ag * self.grow
        self.r_ag += self.inc_r_ag

        self.inc_r_bg = self.w_r_bg * self.grow
        self.r_bg += self.inc_r_bg

        self.inc_h_bg = self.w_h_bg * self.grow
        self.h_bg += self.inc_h_bg

    def plantGrowthWeights(self):
        """
        Calculation of the growth weights for the different geometries of the plant.
        Sets:
            float
        """
        if (self.bg_factor + self.ag_factor) != 0:
            # normalization leads to adapation of -20 to +20 % of w_b_a
            ratio_b_a_resource = ((self.bg_factor /
                                   (self.bg_factor + self.ag_factor)) - 0.5) / 5
            # new ratio of belowground to aboveground growth weight:
            w_ratio_b_a = self.parameter['w_b_a'] * (1 + ratio_b_a_resource)

            self.w_r_ag = w_ratio_b_a * self.parameter['w_ag']
            self.w_h_ag = w_ratio_b_a * (1 - self.parameter['w_ag'])
            self.w_r_bg = self.parameter['w_bg'] * (1 - w_ratio_b_a)
            self.w_h_bg = (1 - w_ratio_b_a) * (1 - self.parameter['w_bg'])

    def plantMaintenance(self):
        """
        Calculate the maintenance of the plant. Unit: [-]
        Sets:
            float
        """
        self.maint = self.volume * self.parameter["maint_factor"] * self.time

    def plantVolume(self):
        """
        Calculate the total plant volume.
        Saltmarsh plants consist of two cylinders, one above- and one belowground.
        These are each characterised by the cylinder height and cylinder radius.
        Sets:
            float
        """
        self.volume_ag = np.pi * self.r_ag ** 2 * self.h_ag
        self.volume_bg = np.pi * self.r_bg ** 2 * self.h_bg
        self.r_volum_ag_bg = self.volume_ag / self.volume_bg
        self.volume = self.volume_ag + self.volume_bg

    def growthResources(self):
        """
        calculates the resources available for growth and the growth factor. Unit: [-]
        Sets:
            floats
        """

        self.available_resources = min(self.ag_factor, self.bg_factor)

        self.grow = self.parameter["growth_factor"] * (self.available_resources - self.maint) * self.time

        # Check if trees survive based on selected mortality concepts
        super().setTreeKiller()
