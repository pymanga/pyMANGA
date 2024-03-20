#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from PlantModelLib import PlantModel


class Default(PlantModel):
    """
    Default plant model.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): plant module specifications from project file tags
        """
        case = args.find("vegetation_model_type").text

    def prepareNextTimeStep(self, t_ini, t_end):
        self.plants = []
        self.t_ini = t_ini
        self.t_end = t_end

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        growth_concept_information = tree.getGrowthConceptInformation()

        tree.setGeometry(geometry)
        tree.setSurvival(1)

        growth_concept_information["bg_factor"] = belowground_resources
        growth_concept_information["ag_factor"] = aboveground_resources

