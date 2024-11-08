#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PopulationLib.PopManager.PlantGroup import PlantGroup


class Population:
    """
    Module defining structure of the whole population, consisting of plant groups.
    """
    def __init__(self, args):
        """
        Args:
            xml_args (lxml.etree._Element): group module specifications from project file tags
        """
        self.plant_groups = {}
        self.plants = []
        for arg in args.iter("group"):
            self.addPlantGroup(arg)

    def addPlantGroup(self, args):
        """
        Add a group to the dictionary containing all groups.
        Args:
            args: plant group module specifications from project file tags
        """
        plant_group = PlantGroup(xml_args=args)
        self.plant_groups[plant_group.group_name] = plant_group

    def getPlantGroups(self):
        """
        Return dictionary containing all groups.
        Returns:
            dict
        """
        return self.plant_groups

    def getPlantGroup(self, name):
        """
        Return dictionary containing a specific group.
        Args:
            name (str): name of the group
        Returns:
            dict
        """
        return self.plant_groups[name]
