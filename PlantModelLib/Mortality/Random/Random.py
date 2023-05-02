#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from PlantModelLib.Mortality.NoGrowth import NoGrowth


class Random(NoGrowth):

    def __init__(self, args, case):
        super().__init__(args, case)
        # Read input parameters from xml file
        self.getInputParameters(args)
        # Default values if no inputs are given
        try:
            self._probability
        except:
            # Threshold for biomass increment: 0.5 %
            self._probability = 0.0016
            print("NOTE: Use default `probability`: " + str(self._probability) +
                  ".")

    def setSurvive(self, args):
        self._survive = 1
        r = np.random.uniform(0, 1, 1)
        # Number of time steps per year
        steps_per_year = self.getStepsPerYear(args)
        ## Multiply r with the number of time steps per year to induce a
        # yearly mortality
        if r * steps_per_year < self._probability:
            self._survive = 0
            print("\t Tree died (Random).")

    def getSurvive(self):
        return self._survive

    def getStepsPerYear(self, args):
        return (3600 * 24 * 365.25) / args.time

    def getInputParameters(self, args):
        # All tags are optional
        missing_tags = ["type", "mortality", "probability"]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "probability":
                self._probability = float(args.find("probability").text)
            elif tag == "type":
                case = args.find("type").text
            try:
                missing_tags.remove(tag)
            except ValueError:
                print("WARNING: Tag " + tag + " not specified for " +
                      super().getConceptName() + " (" + case + ") " +
                      "mortality initialisation!")
