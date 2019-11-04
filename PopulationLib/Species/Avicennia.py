#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List containing species specific tree model parameters.
@date: 2018 - Today
@author: jasper.bathmann@ufz.de
"""


def createTree():
    ini_root_depth = 0.004
    ini_stem_radius = 0.005
    ini_stem_height = 0.05
    ini_root_radius = 0.2
    ini_crown_radius = 0.2
    leaf_water_potential = -7860000
    kf_sap = 1.6e-10
    lp = 0.33e-14
    k_geom = 4000
    half_max_h_growth_weight = 0.15
    maint_factor = 6e-7
    sun_c = 8e-8
    growth_factor = 0.0015
    h_sigmo_slope = 0.5
    sigmo_slope = 0.15
    geometry = {}
    parameter = {}
    geometry["h_root"] = ini_root_depth
    geometry["r_root"] = ini_root_radius
    geometry["r_stem"] = ini_stem_radius
    geometry["h_stem"] = ini_stem_height
    geometry["r_crown"] = ini_crown_radius
    parameter["leaf_water_potential"] = leaf_water_potential
    parameter["kf_sap"] = kf_sap
    parameter["lp"] = lp
    parameter["k_geom"] = k_geom
    parameter["half_max_h_growth_weight"] = half_max_h_growth_weight
    parameter["maint_factor"] = maint_factor
    parameter["sun_c"] = sun_c
    parameter["growth_factor"] = growth_factor
    parameter["h_sigmo_slope"] = h_sigmo_slope
    parameter["sigmo_slope"] = sigmo_slope
    return geometry, parameter
