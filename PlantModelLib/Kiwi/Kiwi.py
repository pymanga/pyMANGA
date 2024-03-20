#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: ronny.peters@tu-dresden.de
"""
from PlantModelLib import PlantModel


class Kiwi(PlantModel):
    """
    Kiwi plant model.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): plant module specifications from project file tags
        """
        case = args.find("vegetation_model_type").text
        super().iniMortalityConcept(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        self.time = t_end - t_ini

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        growth_concept_information = tree.getGrowthConceptInformation()
        parameter = tree.getParameter()
        # Define variables that are only required for specific Mortality
        # concepts
        super().setMortalityVariables(growth_concept_information)
        self.survive = 1

        # dbh and height are in cm as in Berger & Hildenbrandt 2000
        dbh = geometry["r_stem"] * 200

        height = (137 + parameter["b2"] * dbh - parameter["b3"] * dbh**2)
        self.grow = (
            parameter["max_growth"] * dbh *
            (1 - (dbh * height) / (parameter["max_dbh"] * parameter["max_height"]))
            /
            (274 + 3 * parameter["b2"] * dbh - 4 * parameter["b3"] * dbh**2) *
            belowground_resources * aboveground_resources)
        dbh = dbh + self.grow * self.time / (3600 * 24 * 365.25)

        # Scaling dbh to zone of influence (ZOI) based on eq. 1 in
        # Berger & Hildenbrandt 2000
        # r_zoi is used as proxy for root and crown plate radius in resource modules
        r_zoi = parameter["a_zoi_scaling"] * (dbh/2/100)**0.5

        # Update tree dictionaries
        geometry["r_stem"] = dbh / 200          # in m
        geometry["r_root"] = r_zoi              # in m
        geometry["r_crown"] = r_zoi             # in m
        geometry["height"] = height / 100       # in m
        geometry["h_stem"] = height / 100 - 2*r_zoi      # in m

        growth_concept_information["growth"] = self.grow
        growth_concept_information["bg_factor"] = belowground_resources
        growth_concept_information["ag_factor"] = aboveground_resources
        try:
            growth_concept_information["age"] += self.time
        except KeyError:
            growth_concept_information["age"] = self.time

        tree.setGeometry(geometry)
        tree.setGrowthConceptInformation(growth_concept_information)

        # Mortality
        # Write dbh in volume variable to be used in mortality concept `Memory`
        self.volume = dbh
        # Check if trees survive based on selected mortality concepts
        super().setTreeKiller()
        # Get Mortality-related variables
        super().getMortalityVariables(growth_concept_information)

        if self.survive == 1:
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)
