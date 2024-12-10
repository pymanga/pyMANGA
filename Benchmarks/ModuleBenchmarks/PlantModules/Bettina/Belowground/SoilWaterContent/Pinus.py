#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def createPlant():
    """
    Constructor containing species-specific parameters and the initial geometry of a plant required by the Bettina plant module.
    Returns:
        multiple dict
    """
    geometry = {}
    parameter = {}

    fine_root_thickness = 0.0005
    RAI = 6.0

    # plant module BETTINA
    geometry["h_root"] = fine_root_thickness * RAI / 2      # m
    geometry["h_crown"] = 0.002                             # m
    geometry["r_root"] = 0.05                               # m
    geometry["r_stem"] = 0.00125                            # m
    geometry["h_stem"] = 0.1                                # m
    geometry["r_crown"] = 0.05                              # m
    parameter["leaf_water_potential"] = -9e5                # Pa
    parameter["kf_sap"] = 5.0e-10                           # m**2 / s / Pa
    parameter["lp"] = 4.8e-14                               # m / s / Pa
    parameter["k_geom"] = 4 / fine_root_thickness           # 1 / m
    parameter["half_max_h_growth_weight"] = 0.15            # -
    parameter["maint_factor"] = 2e-7                        # 1 / s
    parameter["sun_c"] = 2.5e-8                             # m / s
    parameter["growth_factor"] = 0.02                       # -
    parameter["h_sigmo_slope"] = 0.3                        # -
    parameter["sigmo_slope"] = 0.015                        # -
    parameter["pF"] = 4.0                                   # ?
    # resource module FixedSalinity
    parameter["r_salinity"] = "bettina"
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    return geometry, parameter
