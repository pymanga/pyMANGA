#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def createPlant():
    geometry = {}
    parameter = {}
    geometry["r_ag"] = 0.05
    geometry["h_ag"] = 0.1
    geometry["r_bg"] = 0.05
    geometry["h_bg"] = 0.1
    parameter["maint_factor"] = 0.00002
    parameter["growth_factor"] = 0.0000002
    parameter['w_b_a'] = 0.7
    parameter['w_ag'] = 0.2
    parameter['w_bg'] = 0.6
    parameter["r_salinity"] = "forman"
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    parameter["salt_effect_d"] = -0.1
    parameter["salt_effect_ui"] = 80
    return geometry, parameter
