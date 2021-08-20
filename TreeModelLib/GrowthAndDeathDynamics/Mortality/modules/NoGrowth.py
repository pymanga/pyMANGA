#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

#from TreeModelLib.GrowthAndDeathDynamics.Mortality import Mortality


class NoGrowth:
    def __init__(self, args):
        # case = args.find("mortality").text
        # print("Mortality concept of type " + case + ".")

        self.survive = 1

    def getSurvival(self, args):
        if args.grow <= 0:
            self.survive = 0
            print("\t\t Tree died.")

        return self.survive

    # # functions to pass the method check
    # def progressTree(self):
    #     pass
    #
    # def addTree(self):
    #     pass
    #
    # def prepareNextTimestep(self):
    #     pass