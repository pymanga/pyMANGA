#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeOutputLib.TreeOutput import TreeOutput


class NONE(TreeOutput):
    ## Constructor of dummy objects in order to drop output
    def __init__(self, args):
        ## defining the type of output
        self.case = args.find("type").text
        print("Running without tree output.")
