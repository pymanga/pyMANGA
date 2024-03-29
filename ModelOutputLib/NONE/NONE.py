#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ModelOutputLib.ModelOutput import ModelOutput


class NONE(ModelOutput):
    """
    Dummy class to avoid writing model output.
    """
    def __init__(self, args):
        """
        Args:
            args: module specifications from project file tags
        """
        self.case = args.find("type").text
        print("Running without plant output.")

    def writeOutput(self, plant_groups, time, force_output=False, group_died=False):
        pass

    def getOutputDir(self):
        return ""
