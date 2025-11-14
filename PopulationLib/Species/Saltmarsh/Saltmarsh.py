#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def createPlant():
    geometry = {}
    parameter = {}
    parameter["sun_c"] = 1361
    parameter['water_c'] = 1.5
    geometry["r_ag"] = 0.05
    geometry["r_ag_ic"] = 0.05
    geometry["h_ag"] = 0.1
    geometry["r_bg"] = 0.05
    geometry["r_bg_ic"] = 0.05
    geometry["h_bg"] = 0.1
    geometry['volume_ic'] = 0.0007853975
    parameter["maint_factor"] = 1.5e-6
    parameter["growth_factor"] = 5e-9
    parameter["dieback_factor"] = 1
    parameter['w_b_a'] = 0.5
    parameter['w_ag'] = 0.5
    parameter['w_bg'] = 0.5
    parameter["r_salinity"] = "forman"
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    parameter["salt_effect_d"] = -0.045
    parameter["salt_effect_ui"] = 60
    return geometry, parameter
