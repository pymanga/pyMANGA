#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeModelLib.GrowthAndDeathDynamics import GrowthAndDeathDynamics


class SimpleKiwi(GrowthAndDeathDynamics):
    ## SimpleKiwi for death and growth dynamics. For details see
    #  https://doi.org/10.1016/S0304-3800(00)00298-2 \n
    #  @param Tags to define SimpleBettina: type
    #  @date 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")

    ## This functions prepares the growth and death concept.
    #  In the SimpleKiwi concept, the timestepping is updated. 
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next
    def prepareNextTimeStep(self, t_ini, t_end):
        self.t_ini = t_ini
        self.t_end = t_end

    ## This functions is the main routine for reading the tree geometry and
    #  parameters, scheduling the computations and updating the tree geometry.\n
    #  @param tree - object of type tree\n
    #  @param aboveground_resources - fraction of maximum light interception (shading effect)\n
    #  @param belowground_resources - fract of max water upt (compet and/or salinity > 0)
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

 
