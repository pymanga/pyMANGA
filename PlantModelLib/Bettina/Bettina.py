#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PlantModelLib import PlantModel
import numpy as np


class Bettina(PlantModel):
    """
    Bettina plant model.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): plant module specifications from project file tags
        """
        case = args.find("vegetation_model_type").text
        super().iniMortalityConcept(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepare next time step by initializing relevant variables.
        Args:
            t_ini (int): start of current time step in seconds
            t_end (int): end of current time step in seconds
        """
        self.time = t_end - t_ini

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        growth_concept_information = tree.getGrowthConceptInformation()
        self.extractRelevantInformation(geometry, tree.getParameter())

        self.survive = 1
        # Define variables that are only required for specific Mortality
        # concepts
        super().setMortalityVariables(growth_concept_information)

        self.treeMaintenance()
        self.bgResources(belowground_resources)
        self.agResources(aboveground_resources)
        self.growthResources()
        self.treeGrowthWeights()
        self.treeGrowth()
        geometry["r_crown"] = self.r_crown
        geometry["h_crown"] = self.h_crown
        geometry["r_root"] = self.r_root
        geometry["h_root"] = self.h_root
        geometry["r_stem"] = self.r_stem
        geometry["h_stem"] = self.h_stem
        growth_concept_information[
            "root_surface_resistance"] = self.root_surface_resistance
        growth_concept_information["xylem_resistance"] = self.xylem_resistance
        growth_concept_information["ag_resources"] = self.ag_resources
        growth_concept_information["bg_resources"] = self.bg_resources
        growth_concept_information["growth"] = self.grow
        growth_concept_information["available_resources"] = (
            self.available_resources)
        psi_zero = self.deltaPsi()
        growth_concept_information["psi_zero"] = psi_zero
        growth_concept_information["salinity"] = (
            (belowground_resources * psi_zero - psi_zero) / 85000000.)
        growth_concept_information["weight_girthgrowth"] = \
            self.weight_girthgrowth
        growth_concept_information["weight_stemgrowth"] = \
            self.weight_stemgrowth
        growth_concept_information["weight_crowngrowth"] = \
            self.weight_crowngrowth
        growth_concept_information["weight_rootgrowth"] = \
            self.weight_rootgrowth
        growth_concept_information["bg_factor"] = belowground_resources
        growth_concept_information["ag_factor"] = aboveground_resources
        try:
            growth_concept_information["age"] += self.time
        except KeyError:
            growth_concept_information["age"] = self.time

        # Get Mortality-related variables
        super().getMortalityVariables(growth_concept_information)

        tree.setGeometry(geometry)
        tree.setGrowthConceptInformation(growth_concept_information)
        if self.survive == 1:
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

    def extractRelevantInformation(self, geometry, parameter):
        self.parameter = parameter
        self.r_crown = geometry["r_crown"]
        self.h_crown = geometry["h_crown"]
        self.r_root = geometry["r_root"]
        self.h_root = geometry["h_root"]
        self.r_stem = geometry["r_stem"]
        self.h_stem = geometry["h_stem"]

        self.flowLength()
        self.treeVolume()
        self.rootSurfaceResistance()
        self.xylemResistance()

    ## This functions updates the geometric measures of the tree.
    def treeGrowth(self):
        """
        Update tree geometry.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'increase of allometric measures'.
        Sets:
            multiple float
        """
        inc_r_stem = (self.weight_girthgrowth * self.grow /
                      (2 * np.pi * self.r_stem * self.flow_length))
        self.r_stem += inc_r_stem
        inc_h_stem = (self.weight_stemgrowth * self.grow /
                      (np.pi * self.r_stem**2))
        self.h_stem += inc_h_stem
        inc_r_crown = (self.weight_crowngrowth * self.grow /
                       (2 * np.pi *
                        (self.h_crown * self.r_crown + self.r_stem**2)))
        self.r_crown += inc_r_crown
        inc_r_root = (self.weight_rootgrowth * self.grow /
                      (2 * np.pi * self.r_root * self.h_root +
                       0.5**0.5 * np.pi * self.r_stem**2))
        self.r_root += inc_r_root

    def treeGrowthWeights(self):
        """
        Calculate the growth weights for distributing biomass increment to the tree geometries.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'weights'.
        Sets:
            multiple float
        """
        self.weight_stemgrowth = (
            self.parameter["half_max_h_growth_weight"] /
            (1 + np.exp(-(self.r_crown - self.r_root) /
                        (self.r_crown + self.r_root) /
                        self.parameter["h_sigmo_slope"])))
        self.weight_crowngrowth = ((1 - self.weight_stemgrowth) / (1 + np.exp(
            (self.ag_resources - self.bg_resources) /
            (self.ag_resources + self.bg_resources) /
            self.parameter["sigmo_slope"])))

        self.weight_girthgrowth = (
            (1 - self.weight_stemgrowth - self.weight_crowngrowth) /
            (1 + np.exp(
                (self.root_surface_resistance - self.xylem_resistance) /
                (self.root_surface_resistance + self.xylem_resistance) /
                self.parameter["sigmo_slope"])))

        self.weight_rootgrowth = (1 - self.weight_stemgrowth -
                                  self.weight_crowngrowth -
                                  self.weight_girthgrowth)

    def treeMaintenance(self):
        """
        Calculate the resource demand for biomass maintenance.

        For parameter reference, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 2.5.
        Sets:
            float
        """
        self.maint = self.volume * self.parameter["maint_factor"] * self.time

    def flowLength(self):
        """
        Calculate the flow length from fine roots to leaves.
        Sets:
            float
        """
        self.flow_length = (2 * self.r_crown + self.h_stem +
                            0.5**0.5 * self.r_root)

    def treeVolume(self):
        """
        Calculate the total tree volume.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'volume of plant components'.
        Sets:
            float
        """
        self.volume = (self.h_root * np.pi * self.r_root**2 +
                       self.flow_length * np.pi * self.r_stem**2 +
                       self.h_crown * np.pi * self.r_crown**2)

    def agResources(self, aboveground_resources):
        """
        Calculate the available aboveground resources (intercepted light measured equivalent to respective water uptake).

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Args:
            aboveground_resources (float): aboveground resource growth reduction factor
        Sets:
            float
        """
        self.ag_resources = aboveground_resources * (
            np.pi * self.r_crown**2 * self.parameter["sun_c"] * self.time)

    def bgResources(self, belowground_resources):
        """
        Calculate the available belowground resources (m³ water per time step).

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Args:
            belowground_resources (float): belowground resource growth reduction factor
        Sets:
            float
        """
        self.rootSurfaceResistance()
        self.xylemResistance()
        self.bg_resources = belowground_resources * (
            (-self.time * self.deltaPsi() /
             (self.root_surface_resistance + self.xylem_resistance) / np.pi))

    def rootSurfaceResistance(self):
        """
        Calculate the root surface resistance.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Sets:
            float
        """
        self.root_surface_resistance = (1 / self.parameter["lp"] /
                                        self.parameter["k_geom"] / np.pi /
                                        self.r_root**2 / self.h_root)

    def xylemResistance(self):
        """
        Calculate the xylem resistance.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Sets:
            float
        """
        self.xylem_resistance = (self.flow_length / self.parameter["kf_sap"] /
                                 np.pi / self.r_stem**2)

    def deltaPsi(self):
        """
        Calculate the water potential gradient with soil water potential = 0.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resources'.
        Returns:
            float
        """
        return (self.parameter["leaf_water_potential"] +
                (2 * self.r_crown + self.h_stem) * 9810)

    def growthResources(self):
        """
        Calculate the available resources and the biomass increment.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resources'.
        Sets:
            multiple float
        """
        self.available_resources = min(self.ag_resources, self.bg_resources)
        self.grow = (self.parameter["growth_factor"] *
                     (self.available_resources - self.maint))
        # Check if trees survive based on selected mortality concepts
        super().setTreeKiller()
