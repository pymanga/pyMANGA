#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List containing species-specific plant model parameters required in `pyMANGA.PlantModelLib.Kiwi` and `pyMANGA.ResourceLib.BelowGround.Individual.FON`.
"""


def createPlant():
    geometry = {}
    parameter = {}
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
    # resource module FixedSalinity
    parameter["r_salinity"] = "forman"
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    return geometry, parameter
