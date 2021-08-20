#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np


class Memory:
    def __init__(self, args, case):
        self.survive = 1
        self.threshold = 0.5
        self.period = 5
        self.getMemoryPeriod(args)

        print("Initiate mortality of type " + case + " with a memory period "
              "of " + str(self.period) + " years and a threshold of " +
              str(self.threshold) + ".")

    def getSurvival(self, args):
        self.survive = 1
        # get the number of values representing the memory period
        period_in_sec = self.period * 3600 * 24 * 365
        steps = period_in_sec / args.time

        # slice grow_memory array to get only relevant data
        relevant_grow_memory = args.grow_memory[-int(steps):]

        # exclude the very first time step if included in the relevant data
        # as this increment value is an outlier
        if len(relevant_grow_memory) < steps:
            relevant_grow_memory = relevant_grow_memory[1:]

        # if no memory exists fill the array to avail run time errors
        if not relevant_grow_memory:
            relevant_grow_memory.append(0)

        # get current growth increment
        grow_inc = args.grow - args.grow_before

        if grow_inc < self.threshold * np.mean(relevant_grow_memory):
            self.survive = 0
            print("\t Tree died because because of too little growth.")

        return self.survive

    def getConceptName(self):
        return "Memory"

    def getMemoryPeriod(self, args):
        missing_tags = ["mortality", "threshold", "period",
                        "type", "variant", "f_growth"]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "threshold":
                self.threshold = float(args.find("threshold").text)
            elif tag == "period":
                self.period = float(args.find("period").text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for mortality in growth and death "
                    "initialisation!")