#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def createPlant():
    geometry = {}
    parameter = {}
    geometry["r_ag"] = 0.005
    geometry["h_ag"] = 0.01
    geometry["r_bg"] = 0.005
    geometry["h_bg"] = 0.01
    parameter["maint_factor"] = 0.0002
    parameter["growth_factor"] = 0.00000006
    parameter['w_b_a'] = 0.7
    parameter['w_ag'] = 0.2
    parameter['w_bg'] = 0.3
    parameter["max_h"] = 1.5
    # resource module FON
    parameter["aa"] = 10
    parameter["bb"] = 1
    parameter["fmin"] = 0.1
    return geometry, parameter
