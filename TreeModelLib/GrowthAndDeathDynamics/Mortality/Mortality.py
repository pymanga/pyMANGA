#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np


class Mortality:
    def __init__(self, args):
        self.mortality_concept = []
        self.survive = 1

        # Check if mortality concept is defined in project xml
        # Otherwise use default concept
        default_case = "NoGrowth"
        try:
            cases = args.find("mortality").text
        except AttributeError:
            cases = default_case
            print("WARNING: Default Mortality concept '" + default_case +
                  "' is used.")

        cases = cases.split()
        for case in cases:
            if not case or case == "NoGrowth":
                self.iniNoGrowth(args, case)
            elif case == "Random":
                self.iniRandom(args, case)
            elif case == "Memory":
                self.iniMemory(args, case)
            else:
                raise KeyError("Required mortality not implemented.")
            print("Mortality concept of type " + case + " successfully "
                                                        "initiated.")

    def iniNoGrowth(self, args, case):
        from .modules import NoGrowth
        self.mortality_concept.append(NoGrowth.NoGrowth(args, case))

    def iniRandom(self, args, case):
        from .modules import Random
        self.mortality_concept.append(Random.Random(args, case))

    def iniMemory(self, args, case):
        from .modules import Memory
        self.mortality_concept.append(Memory.Memory(args, case))

    def getMortConcept(self):
        return self.mortality_concept

