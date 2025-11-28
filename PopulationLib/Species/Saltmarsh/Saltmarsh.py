#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def createPlant():
    geometry = {}
    parameter = {}
    parameter["p_sun"] = 1361
    parameter['p_water'] = 1.5
    geometry["r_ag"] = 0.05
    geometry["r_ag_ic"] = 0.05
    geometry["h_ag"] = 0.1
    geometry["r_bg"] = 0.05
    geometry["r_bg_ic"] = 0.05
    geometry["h_bg"] = 0.1
    geometry['volume_ic'] = 0.0015708
    parameter["p_maint"] = 1.5e-6
    parameter["p_growth"] = 5e-9
    parameter["p_dieback"] = 1
    parameter['p_ratio_ag_bg'] = 0.5
    parameter['p_ratio_ag'] = 0.5
    parameter['p_ratio_bg'] = 0.5
    parameter["p_transpiration"] = 1.5e-5
    parameter["r_salinity"] = "forman"
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    parameter["salt_effect_d"] = -0.045
    parameter["salt_effect_ui"] = 60
    return geometry, parameter
