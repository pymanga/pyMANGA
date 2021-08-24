#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np


class Random:
    def __init__(self, args, case):
        self.survive = 1
        self.probability = 0.002
        self.getProbability(args)

        print("Initiate mortality of type " + case +
              " with a random mortality of " +
              str(self.probability*100) + " %.")

    def getSurvival(self, args):
        self.survive = 1
        r = np.random.random(1)
        # Number of time steps per year
        ts_per_year = int(args.time / (3600 * 24 * 365))
        ## Multiply r with the number of time steps per year to induce a
        # yearly mortality
        if r * ts_per_year < self.probability:
            self.survive = 0
            print("\t Tree died randomly. Random number: " + str(r[0]))

        return self.survive

    def getConceptName(self):
        return "Random"

    def getProbability(self, args):
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
