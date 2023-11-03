#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from VisualizationLib.Visualization import Visualization


class NONE(Visualization):
    ## Constructor of dummy objects in order to drop visualization
    def __init__(self, args):
        self.case = args[0].find("type").text
        print("Running without visualization.")

    ## Dummy update function
    def update(self, plant_groups, time):
        pass

    ## Dummy show function
    def show(self, time):
        pass
