#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Saltmarsh:

    def __init__(self, args, case):
        """
        Mortality module and super class of other mortality modules containing required constructors.
        Args:
            args: module specification from project file tags. No required.
            case: "NoGrowth" (module name)
        """

    def setSurvive(self, plant_module):
        """
        Determine if plant survives based on memory period and average growth during this period.
        Set attribute survival variable to 0 if plant died. Default is 1 if plant lived.
        Args:
            plant_module (class): "PlantModel" object
        Sets:
            survival status (bool)
        """
        self._survive = 1
        if plant_module.grow <= 0:
            if plant_module.sickly == True:


            self._survive = 0
            print("\t Plant died (NoGrowth).")

    def getSurvive(self):
        """
        Get survival status of a plant.
        Returns:
            survival status (bool), 0 = plant died, 1 = plant lived.
        """
        return self._survive

    def getStepsPerYear(self, plant_module):
        """
        Calculate the number of time steps per year.
        Args:
            plant_module (class): "PlantModel" object
        Returns:
            float
        """
        return (3600 * 24 * 365.25) / plant_module.time

    def setMortalityVariables(self, plant_module, growth_concept_information):
        """
        Constructor for child classes.
        Initiate variables that are not yet in available in the selected growth module but are required
        in this mortality module.
        Args:
            plant_module (class): "PlantModel" object
            growth_concept_information (dict): dictionary containing growth information of the respective plant
        Returns:
            pass
        """
        pass

    def getMortalityVariables(self, plant_module, growth_concept_information):
        """
        Constructor for child classes.
        Get relevant plant attributes required for mortality concept.
        Args:
            plant_module (class): "PlantModel" object
            growth_concept_information (dict): dictionary containing growth information of the respective plant
        Returns:
            dictionary with updated growth concept information
        """
        return growth_concept_information

    def getConceptName(self):
        """
        Return name of mortality module.
        Returns:
            string
        """
        return type(self).__name__

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
                        super(NoGrowth, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(NoGrowth, self).__setattr__(tag, str(arg.text))
            try:
                required_tags.remove(tag)
            except ValueError:
                pass

            for i in range(0, len(optional_tags)):
                if tag == optional_tags[i]:
                    try:
                        super(NoGrowth, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(NoGrowth, self).__setattr__(tag, str(arg.text))

        if len(required_tags) > 0:
            string = ""
            for tag in required_tags:
                string += tag + " "
            raise KeyError(
                "Missing input parameters (in project file) for mortality module initialisation: " + string)
