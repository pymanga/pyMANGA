#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from VisualizationLib.Visualization import Visualization


class SimplePyplot(Visualization):
    def __init__(self, args):
        ## SimpleTest case for belowground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @VAR: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        self.case = args.find("type").text
        print("Initiate visualization of type " + self.case + ".")

    def update(self, tree_groups):
        print("dummy")
