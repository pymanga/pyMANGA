#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ResourceLib import ResourceModel


class Default(ResourceModel):
    """
    Default above-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args: Default module specifications from project file tags
        """
        case = args.find("type").text

    def calculateAbovegroundResources(self):
        """
        Set growth reduction factor for each plant to 1 (i.e., no limitation).
        Sets:
            numpy array of shape(number_of_trees)
        """
        self.aboveground_resources = self.plants

    def prepareNextTimeStep(self, t_ini, t_end):
        self.plants = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addPlant(self, plant):
        self.plants.append(1)
