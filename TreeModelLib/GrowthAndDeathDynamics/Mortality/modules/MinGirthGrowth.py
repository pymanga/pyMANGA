#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np


class MinGirthGrowth:
    def __init__(self, args, case):
        self.survive = 1
        self.min_girth_growth = 0.05   # cm per year (Grueters et al. 2021)
        self.period = 5
        self.getMinGrowthValue(args)

        print("Initiate mortality of type " + case +
              " with min. yearly DBH growth of " +
              str(self.min_girth_growth) + " cm and memory of " +
              str(self.period) + " years.")

    def getSurvival(self, args):
        self.survive = 1

        # get the number of values representing the memory period
        period_in_sec = self.period * 3600 * 24 * 365
        steps = int(period_in_sec / args.time)

        # slice grow_memory array to get only relevant data
        r_stem_inc = args.r_stem_memory[-int(steps):]

        # exclude the first time steps as the stem does not grow in the
        # beginning in BETTINA
        if len(r_stem_inc) >= int(steps):
            # calculate current growth increment
            avg_girth_growth = np.mean(r_stem_inc)
            steps_per_year = (3600 * 24 * 365) / args.time
            avg_girth_growth_y = avg_girth_growth * steps_per_year

            # transform yearly DBH increment rate in r_stem in m
            min_girth_growth_y_m = self.min_girth_growth / 2 / 100   # in m
            if avg_girth_growth_y < min_girth_growth_y_m:
                self.survive = 0
                print("\t Tree died because average DBH increment fell below "
                      "threshold.")

        return self.survive

    def getConceptName(self):
        return "MinGirthGrowth"

    def getMinGrowthValue(self, args):
        missing_tags = ["mortality", "min_girth_growth", "period",
                        "probability", "threshold",
                        "type", "variant", "f_growth"]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "min_girth_growth":
                self.min_girth_growth = float(args.find("min_girth_growth").text)
            elif tag == "period":
                self.period = float(args.find("period").text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for mortality in growth and death "
                    "initialisation!")
