#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List containing species-specific plant model parameters required in `pyMANGA.PlantModelLib.Bettina`,
 `pyMANGA.PlantModelLib.Kiwi` and `pyMANGA.ResourceLib.BelowGround.Individual.FON`.
"""


def createPlant():
    geometry = {}
    parameter = {}
    # plant module BETTINA
    geometry["h_root"] = 0.004                          # m
    geometry["h_crown"] = 0.004                         # m
    geometry["r_root"] = 0.2                            # m
    geometry["r_stem"] = 0.005                          # m
    geometry["h_stem"] = 0.05                           # m
    geometry["r_crown"] = 0.2                           # m
    parameter["leaf_water_potential"] = -7.86e6         # Pa
    parameter["kf_sap"] = 1.04e-10                      # m**2 / s / Pa
    parameter["lp"] = 0.33e-14                          # m / s / Pa
    parameter["k_geom"] = 4000                          # 1 / m
    parameter["half_max_h_growth_weight"] = 0.12        # -
    parameter["maint_factor"] = 2e-7                    # 1 / s
    parameter["sun_c"] = 2.5e-8                         # m / s
    parameter["growth_factor"] = 0.0047                 # -
    parameter["h_sigmo_slope"] = 0.5                    # -
    parameter["sigmo_slope"] = 0.015                    # -
    # plant module KIWI
    geometry["height"] = 0                              # m
    parameter["salt_effect_d"] = -0.18
    parameter["salt_effect_ui"] = 72
    parameter["max_height"] = 3500                      # cm
    parameter["max_dbh"] = 140                          # cm
    parameter["max_growth"] = 162                       # cm
    parameter["b2"] = 48.04
    parameter["b3"] = 0.172
    parameter["mortality_constant"] = 0.467
    parameter["a_zoi_scaling"] = 10
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    return geometry, parameter
