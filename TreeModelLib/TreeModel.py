#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""


class TreeModel:

    def getAbovegroundResources(self):
        return self.aboveground_resources

    def getBelowgroundResources(self):
        return self.belowground_resources

    ## This function initializes and returns the names of all selected
    # mortality concepts
    # @param args: xml project file
    def iniMortalityConcept(self, args):
        from TreeModelLib.GrowthAndDeathDynamics import Mortality
        M = Mortality.Mortality(args)
        self.mortality_concept = M.getMortConcept()
        self.mortality_concept_names = []
        for concept in self.mortality_concept:
            self.mortality_concept_names.append(concept.getConceptName())
        return self.mortality_concept_names

    ## This function calls getMortalityVariables() of all selected mortality
    # concepts and initiates variables that are not yet in available in the
    # selected growth concept but are required for the mortality concept.
    # @param growth_concept_information: growth_concept_information dictionary
    def getMortalityVariables(self, growth_concept_information):
        for mortality_concept in self.mortality_concept:
            mortality_concept.getMortalityVariables(
                self, growth_concept_information)

    ## This function calls setMortalityVariables() of all selected mortality
    # concepts and sets variables that are not yet in available in the
    # selected growth concept but are required for the mortality concept.
    # @param growth_concept_information: growth_concept_information dictionary
    def setMortalityVariables(self, growth_concept_information):
        for mortality_concept in self.mortality_concept:
            growth_concept_information = \
                mortality_concept.setMortalityVariables(
                    self, growth_concept_information)
        return growth_concept_information

    ## This function calls getSurvival() of all selected mortality
    # concepts and checks if the conditions for death are met.
    def getSurvival(self):
        survive = []
        for mortality_concept in self.mortality_concept:
            survive.append(mortality_concept.getSurvival(self))

        if 0 in survive:
            self.survive = 0
