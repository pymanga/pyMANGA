#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

#from TreeModelLib.GrowthAndDeathDynamics.Mortality import Mortality


class NoGrowth:
    def __init__(self, args, case):
        self.survive = 1

        print("Initiate mortality of type " + case + " .")

    def getSurvival(self, args):
        self.survive = 1
        if args.grow <= 0:
            self.survive = 0
            print("\t\t Tree died because growth was <= 0.")
        return self.survive

    def getConceptName(self):
        return "NoGrowth"
