#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from .NoGrowth import NoGrowth


class Memory(NoGrowth):
    def __init__(self, args, case):
        self.threshold = 0.5
        self.period = 5 * 365.25 * 24 * 3600
        self.getMemoryPeriod(args)

        print("Initiate mortality of type " + case + " with a memory period "
              "of " + str(self.period) + " years and a threshold of " +
              str(self.threshold) + ".")

    def getSurvival(self, args):
        self.survive = 1
        # get the number of values representing the memory period
        steps = int(self.period / args.time)

        # slice grow_memory array to get only relevant data
        relevant_grow_memory = args.grow_inc_memory[-steps:]

        # exclude the very first time step if included in the relevant data
        # as this increment value is an outlier
        if len(relevant_grow_memory) < steps:
            relevant_grow_memory = relevant_grow_memory[1:]

        # if no memory exists fill the array to avoid run time errors
        if not relevant_grow_memory:
            relevant_grow_memory.append(0)

        # get current growth increment
        grow_inc = args.grow - args.grow_before

        if grow_inc < self.threshold * np.mean(relevant_grow_memory):
            self.survive = 0
            print("\t Tree died because because of too little growth.")

        return self.survive

    def getMortalityVariables(self, args, growth_concept_information):
        try:
            args.grow = growth_concept_information["growth"]
            args.grow_inc_memory = growth_concept_information["grow_inc_memory"]
        except KeyError:
            args.grow = 0
            args.grow_inc_memory = []
        args.grow_before = args.grow

    def setMortalityVariables(self, args, growth_concept_information):
        growth_inc = args.grow - args.grow_before
        args.grow_inc_memory.append(growth_inc)
        growth_concept_information["grow_inc_memory"] = \
            args.grow_inc_memory
        return growth_concept_information

    def getMemoryPeriod(self, args):
        missing_tags = ["mortality", "threshold", "period", "probability",
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