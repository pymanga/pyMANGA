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
        case = args.find("mortality").text
        if not case or case == "NoGrowth":
            self.iniNoGrowth(args)
        elif case == "Random":
            self.iniRandom(args)
        elif case == "Memory":
            self.iniMemory(args)
        else:
            raise KeyError("Required mortality not implemented.")
        print("Mortality concept of type " + case + " successfully initiated.")

    def iniNoGrowth(self, args):
        from .modules import NoGrowth
        self.mortality_concept = NoGrowth.NoGrowth(args)

    def iniRandom(self, args):
        from .modules import Random
        self.mortality_concept = Random.Random(args)

    def iniMemory(self, args):
        from .modules import Memory
        self.mortality_concept = Memory.Memory(args)

    def getMortConcept(self):
        return self.mortality_concept

