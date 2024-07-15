#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List containing species specific tree model parameters.
@date: 2018 - Today
@author: jasper.bathmann@ufz.de
"""


def createPlant():
    geometry = {}
    parameter = {}
    geometry["h_root"] = 0.004
    geometry["h_crown"] = 0.004
    geometry["r_root"] = 0.25
    geometry["r_stem"] = 0.01
    geometry["h_stem"] = 0.015
    geometry["r_crown"] = 0.3
    parameter["leaf_water_potential"] = -6450000
    parameter["kf_sap"] = 3.12e-10
    parameter["lp"] = 3.3e-15
    parameter["k_geom"] = 4000
    parameter["half_max_h_growth_weight"] = 0.12
    parameter["maint_factor"] = 1.4e-6
    parameter["sun_c"] = 5e-8
    parameter["growth_factor"] = 3.5e-3
    parameter["h_sigmo_slope"] = 0.05
    parameter["sigmo_slope"] = 0.015
    parameter["r_salinity"] = "bettina"
    return geometry, parameter
