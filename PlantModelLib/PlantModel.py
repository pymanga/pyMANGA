#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de, mcwimmler
"""


class PlantModel:

    def getAbovegroundResources(self):
        return self.aboveground_resources

    def getBelowgroundResources(self):
        return self.belowground_resources

    ## This function initializes and returns the names of all selected
    # mortality concepts
    # @param args: xml project file
    def iniMortalityConcept(self, args):
        from PlantModelLib import Mortality
        M = Mortality.Mortality(args)
        self.mortality_concepts = M.getMortConcept()
        self.mortality_concept_names = []
        for concept in self.mortality_concepts:
            self.mortality_concept_names.append(concept.getConceptName())

    def getMortalityConceptNames(self):
        return self.mortality_concept_names

    ## This function calls setMortalityVariables() of all selected mortality
    # concepts and initiates variables that are not yet in available in the
    # selected growth concept but are required for the mortality concept.
    # @param growth_concept_information: growth_concept_information dictionary
    def setMortalityVariables(self, growth_concept_information):
        for mortality_concept in self.mortality_concepts:
            mortality_concept.setMortalityVariables(
                plant_module=self,
                growth_concept_information=growth_concept_information)

    ## This function calls getMortalityVariables() of all selected mortality
    # concepts and return variables that are not yet in available in the
    # selected growth concept but are required for the mortality concept.
    # @param growth_concept_information: growth_concept_information dictionary
    def getMortalityVariables(self, growth_concept_information):
        for mortality_concept in self.mortality_concepts:
            growth_concept_information = \
                mortality_concept.getMortalityVariables(
                    plant_module=self,
                    growth_concept_information=growth_concept_information)
        return growth_concept_information

    ## This function calls setSurvive() of all selected mortality
    # concepts and checks if the conditions for death are met.
    def setTreeKiller(self):
        survive = []
        for mortality_concept in self.mortality_concepts:
            mortality_concept.setSurvive(plant_module=self)
            survive.append(mortality_concept.getSurvive())

        if 0 in survive:
            self.survive = 0

    def getInputParameters(self, args, required_tags=None, optional_tags=None):
        """
        Read module tags from project file.
        Args:
            args (lxml.etree._Element): module specifications from project file tags
            required_tags (array): list of tags that need to be read from the project file
            optional_tags (array): list of tags that can be specified in the project file
        """
        if optional_tags is None:
            optional_tags = []
        if required_tags is None:
            required_tags = []
        for arg in args.iterdescendants():
            tag = arg.tag
            for i in range(0, len(required_tags)):
                if tag == required_tags[i]:
                    try:
                        super(PlantModel, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(PlantModel, self).__setattr__(tag, str(arg.text))
            try:
                required_tags.remove(tag)
            except ValueError:
                pass

            for i in range(0, len(optional_tags)):
                if tag == optional_tags[i]:
                    try:
                        super(PlantModel, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(PlantModel, self).__setattr__(tag, str(arg.text))

        if len(required_tags) > 0:
            string = ""
            for tag in required_tags:
                string += tag + " "
            raise KeyError(
                "Missing input parameters (in project file) for plant module initialisation: " + string)
