#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeModelLib.GrowthAndDeathDynamics import GrowthAndDeathDynamics


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
        self.t_ini = t_ini
        self.t_end = t_end  # ist der fluß von "time" richtig?

    def progressTree(self, tree, aboveground_resources, belowground_resources, time):
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        r_crown = geometry["r_crown"]
        h_crown = geometry["h_crown"] 
        r_root = geometry["r_root"]
        h_root = geometry["h_root"]
        r_stem = geometry["r_stem"]
        h_stem = geometry["h_stem"]
        self.die = 0		# was ist alles self?
        self.flowLength(tree)
        self.treeVolume(tree)
        self.treeMaintenance(tree, time)
        self.bgResources(tree, time, belowground_resources)
        self.agResources(tree, time, aboveground_resources)
        self.growthResources(tree)
        self.treeGrowthWeights(tree)
        self.treeGrowth(tree)
        geometry["r_crown"] = r_crown
        geometry["h_crown"] = h_crown
        geometry["r_root"] = r_root
        geometry["h_root"] = h_root
        geometry["r_stem"] = r_stem
        geometry["h_stem"] = h_stem
        tree.setGeometry(geometry)
        if (self.die == 0):
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)          # richtig?

    def treeGrowth(self, tree):
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
 
    def treeGrowthWeights(self, tree):
        self.weight_stemgrowth = (
                parameter["half_max_h_growth_weight"] /
                (1 + np.exp(- (self.r_crown - self.r_root) /
                              (self.r_crown + self.r_root) /
                              parameter["h_sigmo_slope"])))
        self.weight_crowngrowth = (
                (1 - self.weight_stemgrowth) /
                (1 + np.exp((self.ag_resources - self.bg_resources) /
                            (self.ag_resources - self.bg_resources) /
                            parameter["sigmo_slope"])))

        self.weight_girthgrowth = (
                (1 - self.weight_stemgrowth - self.weight_crowngrowth) /
                (1 + np.exp((self.root_surface_resistance -
                             self.xylem_resistance) /
                 (self.root_surface_resistance + self.xylem_resistance) /
                 parameter["sigmo_slope"])))

        self.weight_rootgrowth = (1 - self.weight_stemgrowth -
                                  self.weight_crowngrowth -
                                  self.weight_girthgrowth)

    def treeMaintenance(self, tree, time): # was macht denn tree?
        self.maint = self.volume * parameter["maint_factor"] * time

    def flowLength(self, tree):
        self.flow_length = (
                2 * self.r_crown + self.h_stem +
                0.5 ** 0.5 * self.root_radius)

    def treeVolume(self,tree):
        self.volume = (self.h_root * np.pi * self.r_root**2 +
                self.flow_length * np.pi * self.r_stem**2 +
                self.h_crown * np.pi * self.r_crown**2)

    def agResources(self, tree, time, aboveground_resources):
        self.ag_resources = aboveground_resources * (
                np.pi * self.r_crown**2 *
                parameter["sun_c"] * time)
 
    def bgResources(self, tree, time, belowground_resources):
        self.rootSurfaceResistance(tree)
        self.xylemResistance(tree)
        self.deltaPsi(tree)
        self.bg_resources = belowground_resources * ((- time * self.delta_psi /
                         (self.root_surface_resistance + self.xylem_resistance)))

    def rootSurfaceResistance(self,tree):
        self.root_surface_resistance = ( 1 / parameter["lp"] /
                parameter["k_geom"] / np.pi / self.r_root**2 / self.h_root)

    def xylemResistance(self,tree):
        self.xylem_resistance = (
                self.flow_length / parameter["kf_sap"] /
                np.pi / self.r_stem**2)

    def deltaPsi(self,tree):
        self.delta_psi = (
                parameter["leaf_water_potential"] +
                (2 * self.r_crown + self.h_stem) * 9810)

    def growthResources(self,tree):
        self.available_resources = min(self.ag_resources, self.bg_resources)
        self.grow = (parameter["growth_factor"] *
                     (self.available_resources - self.maint))
        if(self.grow < 0):
            self.grow = 0
            self.die = 1
