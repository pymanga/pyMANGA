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
    def getSurvival(self, args):
        self.survive = 1
        if args.grow <= 0:
            self.survive = 0
            print("\t\t Tree died because growth was <= 0.")
        return self.survive

    ## This function initiates variables that are not yet in available in
    # the selected growth concept but are required for the mortality concept.
    # The function is called by the growth concept.
    def getMortalityVariables(self, args, growth_concept_information):
        pass

    ## This function sets variables that are not yet in available in
    # the selected growth concept but are required for the mortality concept.
    # The function is called by the growth concept.
    def setMortalityVariables(self, args, growth_concept_information):
        return growth_concept_information

    ## This function returns the name of the mortality concept
    def getConceptName(self):
        return type(self).__name__
