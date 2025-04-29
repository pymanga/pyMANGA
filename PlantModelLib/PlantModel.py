#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. include:: ./PlantModel.md
"""


class PlantModel:
    """
    Dummy class for all plant models.
    """

    def iniMortalityConcept(self, args):
        """
        Initialize selected mortality modules
        Args:
            args (lxml.etree): mortality module specifications from project file tags
        """
        from PlantModelLib import Mortality
        M = Mortality.Mortality(args)
        self.mortality_concepts = M.getMortConcept()
        self.mortality_concept_names = []
        for concept in self.mortality_concepts:
            self.mortality_concept_names.append(concept.getConceptName())

    def getMortalityConceptNames(self):
        """
        Return list with selected mortality module names.
        Returns:
            list
        """
        return self.mortality_concept_names

    def setMortalityVariables(self, growth_concept_information):
        """
        Call all selected mortality modules and initiates variables that are not yet in available in the
        selected growth module.
        Args:
            growth_concept_information (dict): collection of growth parameters
        """
        for mortality_concept in self.mortality_concepts:
            mortality_concept.setMortalityVariables(
                plant_module=self,
                growth_concept_information=growth_concept_information)

    def getMortalityVariables(self, growth_concept_information):
        """
        Call all selected mortality modules and retrieve required plant growth parameters.
        Args:
            growth_concept_information (dict): collection of growth parameters
        Returns:
            dict
        """
        for mortality_concept in self.mortality_concepts:
            growth_concept_information = \
                mortality_concept.getMortalityVariables(
                    plant_module=self,
                    growth_concept_information=growth_concept_information)
        return growth_concept_information

    def setTreeKiller(self):
        """
        Call all selected mortality modules and retrieve survival status of a plant.
        If survival status is zero (plant died) in one of the modules, the plant dies.
        Returns:
            numeric
        """
        survive = []
        for mortality_concept in self.mortality_concepts:
            mortality_concept.setSurvive(plant_module=self)
            survive.append(mortality_concept.getSurvive())

        if 0 in survive:
            self.survive = 0

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        """
        Manage growth procedures for a timestep --- read tree geometry and parameters,
        schedule computations, and update tree geometry and survival.
        Args:
            tree (dict): tree object
            aboveground_resources (float): aboveground resource growth reduction factor
            belowground_resources (float): belowground resource growth reduction factor
        """
        pass

    def getInputParameters(self, **tags):
        """
        Read module tags from project file.
        Args:
            tags (dict): dictionary containing tags found in the project file as well as required and optional tags of
            the module under consideration.
        """
        try:
            prj_file_tags = tags["prj_file"]
        except KeyError:
            prj_file_tags = []
            print("WARNING: Module attributes are missing.")
        try:
            required_tags = tags["required"]
        except KeyError:
            required_tags = []
        try:
            optional_tags = tags["optional"]
        except KeyError:
            optional_tags = []

        for arg in prj_file_tags.iterdescendants():
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
