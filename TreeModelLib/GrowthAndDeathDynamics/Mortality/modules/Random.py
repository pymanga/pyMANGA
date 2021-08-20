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
        self.threshold = 0.05
        self.getThreshold(args)

        print("Initiate mortality of type " + case +
              " with a random mortality of " +
              str(self.threshold*100) + " %.")

    def getSurvival(self, args):
        self.survive = 1
        r = np.random.random(1)
        if r < self.threshold:
            self.survive = 0
            print("\t Tree died randomly. Random number: " + str(r[0]))

        return self.survive

    def getConceptName(self):
        return "Random"

    def getThreshold(self, args):
        missing_tags = ["mortality", "threshold",
                        "type", "variant", "f_growth"]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "threshold":
                self.threshold = float(args.find("threshold").text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for mortality in growth and death "
                    "initialisation!")
