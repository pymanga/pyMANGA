#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeModelLib.GrowthAndDeathDynamics import GrowthAndDeathDynamics
import numpy as np


class SimpleBettina(GrowthAndDeathDynamics):
    def __init__(self, args):
        ## SimpleTest case for death and growth dynamics. This case is
        #  defined to test the passing of information between the instances.
        #  @VAR: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        print("Growth and death dynamics of type " + case + ".")

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the cgrowth and death concept.
        #  In the SimpleTest concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @VAR: t_ini - initial time for next timestep \n
        #  t_end - end time for next 
        self.time = t_end - t_ini

    def progressTree(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        self.parameter = tree.getParameter()
        self.r_crown = geometry["r_crown"]
        self.h_crown = geometry["h_crown"] 
        self.r_root = geometry["r_root"]
        self.h_root = geometry["h_root"]
        self.r_stem = geometry["r_stem"]
        self.h_stem = geometry["h_stem"]
        self.die = 0
        self.flowLength()
        self.treeVolume()
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
        tree.setGeometry(geometry)
        if (self.die == 0):
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)         

    def treeGrowth(self):
        inc_rs = (self.weight_girthgrowth * self.grow /
                (2 * np.pi * self.r_stem * self.flow_length)) 
        self.r_stem += inc_rs
        inc_hs = (self.weight_stemgrowth * self.grow /
                (np.pi * self.r_stem ** 2))
        inc_rc = (self.weight_crowngrowth * self.grow /
                (2 * np.pi * (self.h_crown * self.r_crown +
                self.r_stem ** 2)))
        inc_rr = (self.weight_rootgrowth * self.grow /
                (2 * np.pi * self.r_root * self.h_root +
                 0.5 ** 0.5 * np.pi * self.r_stem ** 2))
        self.r_root += inc_rr
        self.h_stem += inc_hs
        self.r_crown += inc_rc
 
    def treeGrowthWeights(self):
        self.weight_stemgrowth = (
                self.parameter["half_max_h_growth_weight"] /
                (1 + np.exp(- (self.r_crown - self.r_root) /
                              (self.r_crown + self.r_root) /
                              self.parameter["h_sigmo_slope"])))
        self.weight_crowngrowth = (
                (1 - self.weight_stemgrowth) /
                (1 + np.exp((self.ag_resources - self.bg_resources) /
                            (self.ag_resources - self.bg_resources) /
                            self.parameter["sigmo_slope"])))

        self.weight_girthgrowth = (
                (1 - self.weight_stemgrowth - self.weight_crowngrowth) /
                (1 + np.exp((self.root_surface_resistance -
                             self.xylem_resistance) /
                 (self.root_surface_resistance + self.xylem_resistance) /
                 self.parameter["sigmo_slope"])))

        self.weight_rootgrowth = (1 - self.weight_stemgrowth -
                                  self.weight_crowngrowth -
                                  self.weight_girthgrowth)

    def treeMaintenance(self):
        self.maint = self.volume * self.parameter["maint_factor"] * self.time

    def flowLength(self):
        self.flow_length = (
                2 * self.r_crown + self.h_stem +
                0.5 ** 0.5 * self.r_root)

    def treeVolume(self):
        self.volume = (self.h_root * np.pi * self.r_root**2 +
                self.flow_length * np.pi * self.r_stem**2 +
                self.h_crown * np.pi * self.r_crown**2)

    def agResources(self, aboveground_resources):
        self.ag_resources = aboveground_resources * (
                np.pi * self.r_crown**2 *
                self.parameter["sun_c"] * self.time)
 
    def bgResources(self, belowground_resources):
        self.rootSurfaceResistance()
        self.xylemResistance()
        self.deltaPsi()
        self.bg_resources = belowground_resources * ((- self.time * self.delta_psi /
                         (self.root_surface_resistance + self.xylem_resistance)))

    def rootSurfaceResistance(self):
        self.root_surface_resistance = ( 1 / self.parameter["lp"] /
                self.parameter["k_geom"] / np.pi / self.r_root**2 / self.h_root)

    def xylemResistance(self):
        self.xylem_resistance = (
                self.flow_length / self.parameter["kf_sap"] /
                np.pi / self.r_stem**2)

    def deltaPsi(self):
        self.delta_psi = (
                self.parameter["leaf_water_potential"] +
                (2 * self.r_crown + self.h_stem) * 9810)

    def growthResources(self):
        self.available_resources = min(self.ag_resources, self.bg_resources)
        self.grow = (self.parameter["growth_factor"] *
                     (self.available_resources - self.maint))
        if(self.grow < 0):
            self.grow = 0
            self.die = 1
