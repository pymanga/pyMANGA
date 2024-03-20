#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ResourceLib import ResourceModel


class Default(ResourceModel):
    """
    Default below-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args: below-ground module specifications from project file tags
        """
        case = args.find("type").text

    def prepareNextTimeStep(self, t_ini, t_end):
        self.plants = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addPlant(self, plant):
        self.plants.append(1)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant.
        In Default this is 1.
        Returns:
            numpy array of shape(number_of_trees)
        """
        self.belowground_resources = self.plants

    def getOGSAccessible(self):
        """
        Check whether module is optimized for external use.
        Returns:
            bool
        """
        return True

    def setExternalInformation(self, **args):
        """
        Set arguments that can be accessed externally.
        Args:
            **args: to be specified
        """
        self.external_information = args

    def getExternalInformation(self):
        """
        Get arguments for external use.
        Args:
            **args: to be specified
        """
        return self.external_information
