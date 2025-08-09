#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def createPlant():
    geometry = {}
    parameter = {}
    geometry["r_ag"] = 0.05
    geometry["r_ag_ic"] = 0.05
    geometry["h_ag"] = 0.05
    geometry["r_bg"] = 0.05
    geometry["r_bg_ic"] = 0.05
    geometry["h_bg"] = 0.05
    geometry['volume_ic'] = 0.0007853975
    parameter["maint_factor"] = 4.5e-10
    parameter["growth_factor"] = 6.6e-8
    parameter['w_b_a'] = 0.5
    parameter['w_ag'] = 0.5
    parameter['w_bg'] = 0.5
    parameter["r_salinity"] = "forman"
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    parameter["salt_effect_d"] = -0.1
    parameter["salt_effect_ui"] = 80
    return geometry, parameter
