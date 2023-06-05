#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List containing species specific tree model parameters.
@date: 2018 - Today
@author: jasper.bathmann@ufz.de
"""


def createTree():
    # Werte 'gerundet' von Janosch's Kalibrierungs-File
    # Werte am nächsten an median(pF)
    fine_root_thickness = 0.0005
    RAI = 6.0

    ini_crown_depth = 0.002
    ini_root_depth = fine_root_thickness * RAI / 2

    ini_stem_radius = 0.00125
    ini_stem_height = 0.1
    ini_root_radius = 0.05
    ini_crown_radius = 0.05

    k_geom = 4 / fine_root_thickness
    kf_sap = 5.0e-10
    lp = 4.8e-14
    leaf_water_potential = -900000.0

    sun_c = 2.5e-8
    growth_factor = 0.02 # k_grow
    half_max_h_growth_weight = 0.15
    maint_factor = 0

    pF = 4.0 #2

    h_sigmo_slope = 0.3
    sigmo_slope = 0.015

    geometry = {}
    parameter = {}
    geometry["h_root"] = ini_root_depth
    geometry["h_crown"] = ini_crown_depth
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
    parameter["pF"] = pF
    return geometry, parameter
