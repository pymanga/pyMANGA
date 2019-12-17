#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeModelLib.GrowthAndDeathDynamics import GrowthAndDeathDynamics


class SimpleKiwi(GrowthAndDeathDynamics):
    def __init__(self, args):
        ## SimpleTest case for death and growth dynamics. This case is
        #  defined to test the passing of information between the instances.
        #  @param: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the cgrowth and death concept.
        #  In the SimpleTest concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @param: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.trees = []
        self.t_ini = t_ini
        self.t_end = t_end

    def progressTree(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        tree.setGeometry(geometry)
        tree.setSurvival(1)
        dbh = geometry["r_stem"] * 200
        height = (137 + parameter["b2"] * dbh - parameter["b3"] * dbh**2)
        growth = ( parameter["max_growth"] * dbh * 
           (1 - dbh * height / parameter["max_dbh"] / parameter["max_height"]) /
           (274 + 3 * parameter["b2"] * dbh - 4 * parameter["b3"] * dbh**2)
            * belowground_resources) 
        dbh = dbh + growth * (self.t_end - self.t_ini)/(3600*24*365)
        if growth < parameter["mortality_constant"]:
            tree.setSurvival(0)
        print(growth)
        print(dbh)
        geometry["r_stem"] = dbh/200

 
