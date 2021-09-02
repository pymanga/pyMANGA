#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from TreeModelLib.GrowthAndDeathDynamics.Mortality.NoGrowth import NoGrowth


class Random(NoGrowth):
    def __init__(self, args, case):
        super().__init__(args, case)
        # Read input parameters from xml file
        self.getInputParameters(args)
        # Default values if no inputs are given
        try:
            self.probability
        except:
            # Threshold for biomass increment: 0.5 %
            self.probability = 0.0016
            print("NOTE: Use default `probability`: " + str(self.probability) +
                  ".")

    def getSurvival(self, args):
        self.survive = 1
        r = np.random.random(1)
        # Number of time steps per year
        steps_per_year = (3600 * 24 * 365) / args.time
        ## Multiply r with the number of time steps per year to induce a
        # yearly mortality
        if r * steps_per_year < self.probability:
            self.survive = 0
            print("\t Tree died randomly. Random number: " + str(r[0]))

        return self.survive

    def getInputParameters(self, args):
        # All tags are optional
        missing_tags = ["mortality", "probability", "threshold", "period",
                        "type", "variant", "f_growth"]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "probability":
                self.probability = float(args.find("probability").text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for mortality in growth and death "
                    "initialisation!")
