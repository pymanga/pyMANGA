#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:25:03 2018

@author: bathmann
"""

if __name__ == '__main__':
    from AbovegroundCompetition import AbovegroundCompetition
    from BelowgroundCompetition import BelowgroundCompetition
    from GrowthAndDeathDynamics import GrowthAndDeathDynamics
else:
    from .AbovegroundCompetition import AbovegroundCompetition
    from .BelowgroundCompetition import BelowgroundCompetition
    from .GrowthAndDeathDynamics import GrowthAndDeathDynamics
