#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork
from TreeModelLib.BelowgroundCompetition.OGSLargeScale3D import OGSLargeScale3D


class NetworkOGSLargeScale3D(SimpleNetwork, OGSLargeScale3D):
    def __init__(self, args):
        OGSLargeScale3D.__init__(self, args)