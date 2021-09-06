#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeModelLib import TreeModel
import numpy as np
from TreeModelLib.GrowthAndDeathDynamics import Mortality


class SimpleBettina(TreeModel):
    ## SimpleBettina for death and growth dynamics. This module is implements
    #  the BETTINA single tree model as described in the ODD, appendix of
    #  https://doi.org/10.1016/j.ecolmodel.2018.10.005 \n
    #  @param Tags to define SimpleBettina: type
    #  @date 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Growth and death dynamics of type " + case + ".")

        M = Mortality.Mortality(args)
        self.mortality_concept = M.getMortConcept()
        self.mortality_concept_names = []
        for concept in self.mortality_concept:
            self.mortality_concept_names.append(concept.getConceptName())

    ## This functions prepares the growth and death concept.
    #  In the SimpleBettina concept, trees are saved in a simple list
    #  and the timestepping is updated. In preparation for the next time-
    #  step, the list is simply resetted.\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next
    def prepareNextTimeStep(self, t_ini, t_end):
        self.time = t_end - t_ini

    ## This functions is the main routine for reading the tree geometry and
    #  parameters, scheduling the computations and updating the tree geometry.\n
    #  @param tree - object of type tree\n
    #  @param aboveground_resources - fraction of maximum light interception
    #  (shading effect)\n
    #  @param belowground_resources - fract of max water upt (compet and/or
    #  salinity > 0)
    def progressTree(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        growth_concept_information = tree.getGrowthConceptInformation()
        self.parameter = tree.getParameter()
        self.r_crown = geometry["r_crown"]
        self.h_crown = geometry["h_crown"]
        self.r_root = geometry["r_root"]
        self.h_root = geometry["h_root"]
        self.r_stem = geometry["r_stem"]
        self.h_stem = geometry["h_stem"]
        self.survive = 1

        self.flowLength()
        self.treeVolume()

        # Define variables that are only required for specific Mortality
        # concepts
        for mortality_concept in self.mortality_concept:
            mortality_concept.getMortalityVariables(
                self, growth_concept_information)

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

        # Set Mortality-related variables
        for mortality_concept in self.mortality_concept:
            growth_concept_information = \
                mortality_concept.setMortalityVariables(
                    self, growth_concept_information)

        tree.setGeometry(geometry)
        tree.setGrowthConceptInformation(growth_concept_information)
        if self.survive == 1:
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

    ## This functions updates the geometric measures of the tree.
    def treeGrowth(self):
        inc_r_stem = (self.weight_girthgrowth * self.grow /
                      (2 * np.pi * self.r_stem * self.flow_length))
        self.r_stem += inc_r_stem
        inc_h_stem = (self.weight_stemgrowth * self.grow /
                      (np.pi * self.r_stem ** 2))
        self.h_stem += inc_h_stem
        inc_r_crown = (self.weight_crowngrowth * self.grow /
                       (2 * np.pi *
                        (self.h_crown * self.r_crown + self.r_stem ** 2)))
        self.r_crown += inc_r_crown
        inc_r_root = (self.weight_rootgrowth * self.grow /
                      (2 * np.pi * self.r_root * self.h_root +
                       0.5 ** 0.5 * np.pi * self.r_stem ** 2))
        self.r_root += inc_r_root

    ## This functions calculates the growths weights for distributing
    # biomass increment to the geometric (allometric) tree measures.
    def treeGrowthWeights(self):
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

    ## This function calculates the resource demand for biomass maintenance.
    def treeMaintenance(self):
        self.maint = self.volume * self.parameter["maint_factor"] * self.time

    ## This function calculates the flow length from fine roots to leaves.
    def flowLength(self):
        self.flow_length = (2 * self.r_crown + self.h_stem +
                            0.5 ** 0.5 * self.r_root)

    ## This function calculates the total tree volume.
    def treeVolume(self):
        self.volume = (self.h_root * np.pi * self.r_root ** 2 +
                       self.flow_length * np.pi * self.r_stem ** 2 +
                       self.h_crown * np.pi * self.r_crown ** 2)

    ## This function calculates the available aboveground resources (
    #  intercepted light
    #  measured equivalent to respective water uptake).
    #  @param aboveground_resources - fraction of maximum light interception
    #  (shading effect)\n
    def agResources(self, aboveground_resources):
        self.ag_resources = aboveground_resources * (
                np.pi * self.r_crown ** 2 * self.parameter[
            "sun_c"] * self.time)

    ## This function calculates the available belowground resources (m³
    # water per time step).
    #  @param belowground_resources - fract of max water upt (compet and/or
    #  salinity > 0)
    def bgResources(self, belowground_resources):
        self.rootSurfaceResistance()
        self.xylemResistance()
        self.bg_resources = belowground_resources * (
            (-self.time * self.deltaPsi() /
             (self.root_surface_resistance + self.xylem_resistance) / np.pi))

    ## This function calculates the root surface resistance.
    def rootSurfaceResistance(self):
        self.root_surface_resistance = (1 / self.parameter["lp"] /
                                        self.parameter["k_geom"] / np.pi /
                                        self.r_root ** 2 / self.h_root)

    ## This function calculates the xylem resistance.
    def xylemResistance(self):
        self.xylem_resistance = (self.flow_length / self.parameter["kf_sap"] /
                                 np.pi / self.r_stem ** 2)

    ## This function calculates the potential gradient with soil water
    # potential = 0.
    def deltaPsi(self):
        return (self.parameter["leaf_water_potential"] +
                (2 * self.r_crown + self.h_stem) * 9810)

    ## This function calculates the available resources and the biomass
    # increment.
    def growthResources(self):
        self.available_resources = min(self.ag_resources, self.bg_resources)
        self.grow = (self.parameter["growth_factor"] *
                     (self.available_resources - self.maint))
        # Iterate through mortality concepts
        # if tree dies in one of them he's dead
        survive = []
        for mortality_concept in self.mortality_concept:
            survive.append(mortality_concept.getSurvival(self))

        if 0 in survive:
            self.survive = 0
