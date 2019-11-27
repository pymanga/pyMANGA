#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from VisualizationLib.Visualization import Visualization


class NONE(Visualization):
    def __init__(self, args):
        self.case = args.find("type").text
        print("Running without visualization.")

    def update(self, tree_groups, time):
        pass

    def show(self, time):
        pass
