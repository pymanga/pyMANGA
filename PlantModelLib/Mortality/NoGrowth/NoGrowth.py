#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""


## This class is the super class of all mortality concepts, containing all
# required methods.
class NoGrowth:

    def __init__(self, args, case):
        print("Initiate mortality of type `" + case + "`.")

    ## This function checks if the conditions for death are met.
    # @param args: growth concept object
    def setSurvive(self, plant_module):
        self._survive = 1
        if plant_module.grow <= 0:
            self._survive = 0
            print("\t Tree died (NoGrowth).")

    ## This function returns the mortality status of a tree
    # as 0 (dead) or 1 (alive)
    def getSurvive(self):
        return self._survive

    ## This function calculates the number of time steps per year
    def getStepsPerYear(self, args):
        return (3600 * 24 * 365.25) / args.time

    ## This function initiates variables that are not yet in available in
    # the selected growth concept but are required for the mortality concept.
    # The function is called by the growth concept.
    def setMortalityVariables(self, plant_module, growth_concept_information):
        pass

    ## This function sets variables that are not yet in available in
    # the selected growth concept but are required for the mortality concept.
    # The function is called by the growth concept.
    def getMortalityVariables(self, plant_module, growth_concept_information):
        return growth_concept_information

    ## This function returns the name of the mortality concept
    def getConceptName(self):
        return type(self).__name__
