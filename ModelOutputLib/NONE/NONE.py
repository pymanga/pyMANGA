#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ModelOutputLib.ModelOutput import ModelOutput


class NONE(ModelOutput):
    def __init__(self, args, time):
        """
        Dummy class to avoid writing model output.
        Args:
            args: module specifications from project file tags
        """
        self.case = args.find("type").text
        print("Running without plant output.")

    def writeOutput(self, plant_groups, time, force_output=False, group_died=False):
        pass

    ## This function returns the output directory
    def getOutputDir(self):
        return ""
