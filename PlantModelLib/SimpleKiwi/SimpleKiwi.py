#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: ronny.peters@tu-dresden.de
"""
from PlantModelLib import PlantModel


class SimpleKiwi(PlantModel):
    ## SimpleKiwi for death and growth dynamics. For details see
    #  https://doi.org/10.1016/S0304-3800(00)00298-2 \n
    #  @param Tags to define SimpleKiwi, see tag documentation \n
    #  @date 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")

    ## This functions prepares the growth and death concept.
    #  In the SimpleKiwi concept, the timestepping is updated.
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next
    def prepareNextTimeStep(self, t_ini, t_end):
        self._t_ini = t_ini
        self._t_end = t_end

    ## This function calculates the growth factor and updates tree geometry\n
    #  @param tree - object of type tree\n
    #  @param aboveground_resources - not used in this module\n
    #  @param belowground_resources - fraction of max water uptake (competition and/or salinity > 0)
    def progressTree(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        tree.setGeometry(geometry)
        dbh = geometry["r_stem"] * 200
        geometry["h_stem"] = (137 + parameter["b2"] * dbh - parameter["b3"] * dbh**2)
        growth = (
            parameter["max_growth"] * dbh *
            (1 - dbh * geometry["h_stem"] / parameter["max_dbh"] / parameter["max_height"])
            /
            (274 + 3 * parameter["b2"] * dbh - 4 * parameter["b3"] * dbh**2) *
            belowground_resources)
        dbh = dbh + growth * (self._t_end - self._t_ini) / (3600 * 24 * 365)
        tree.setSurvival(1)
        if growth < parameter["mortality_constant"]:
            tree.setSurvival(0)
        geometry["r_stem"] = dbh / 200
