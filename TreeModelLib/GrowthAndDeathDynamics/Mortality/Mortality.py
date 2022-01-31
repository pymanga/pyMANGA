#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np


class Mortality:
    ## This class initializes the mortality concept defined in the xml input
    # file.
    # See growth-and-death-concept SimpleBettina for integration in
    # existing concepts.
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
            elif case == "RandomGrowth":
                self.iniRandomGrowth(args, case)
            elif case == "Memory":
                self.iniMemory(args, case)
            else:
                raise KeyError("Required mortality not implemented. "
                               "Available concepts: `NoGrowth`, `Random`, "
                               "`RandomGrowth`, `Memory`")
            print("Mortality concept of type " + case + " successfully "
                  "initiated.")

    def iniNoGrowth(self, args, case):
        from .NoGrowth import NoGrowth
        self.mortality_concept.append(NoGrowth(args, case))

    def iniRandom(self, args, case):
        from .Random import Random
        self.mortality_concept.append(Random(args, case))

    def iniRandomGrowth(self, args, case):
        from .RandomGrowth import RandomGrowth
        self.mortality_concept.append(RandomGrowth(args, case))

    def iniMemory(self, args, case):
        from .Memory import Memory
        self.mortality_concept.append(Memory(args, case))

    def getMortConcept(self):
        return self.mortality_concept
