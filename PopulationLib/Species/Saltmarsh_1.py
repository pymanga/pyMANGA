#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List containing species specific plant model parameters.
@date: 2018 - Today
@author: jasper.bathmann@ufz.de
"""


def createPlant():
    ini_r_ag = 0.005
    ini_h_ag = 0.01
    ini_r_bg = 0.005
    ini_h_bg = 0.01
    maint_factor = 0.000002
    growth_factor = 0.0000004
    max_h = 1.5
    w_b_a = 0.7
    w_ag = 0.2
    w_bg = 0.3
    sun_c = 2.5e-8

    geometry = {}
    parameter = {}
    geometry["r_ag"] = ini_r_ag
    geometry["h_ag"] = ini_h_ag
    geometry["r_bg"] = ini_r_bg
    geometry["h_bg"] = ini_h_bg
    parameter["maint_factor"] = maint_factor
    parameter["growth_factor"] = growth_factor
    parameter['w_b_a'] = w_b_a
    parameter['w_ag'] = w_ag
    parameter['w_bg'] = w_bg
    parameter["max_h"] = max_h
    parameter["sun_c"] = sun_c
    # plant module KIWI
    geometry["height"] = 0
    parameter["salt_effect_d"] = -0.1
    parameter["salt_effect_ui"] = 80
    parameter["max_height"] = 3500 # cm
    parameter["max_dbh"] = 140 # cm
    parameter["max_growth"] = 162
    parameter["b2"] = 48.04
    parameter["b3"] = 0.172
    parameter["mortality_constant"] = 0.467
    parameter["a_zoi_scaling"] = 10
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    return geometry, parameter