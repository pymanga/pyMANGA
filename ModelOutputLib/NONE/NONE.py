#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from ModelOutputLib.ModelOutput import ModelOutput


class NONE(ModelOutput):
    ## Constructor of dummy objects in order to drop output
    def __init__(self, args):
        ## defining the type of output
        self.case = args.find("type").text
        print("Running without tree output.")

    def writeOutput(self, tree_groups, time, force_output=False, group_died=False):
        pass

    ## This function returns the output directory
    def getOutputDir(self):
        return ""
