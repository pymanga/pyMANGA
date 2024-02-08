#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import importlib.util
import os
import importlib


class Plant:
    def __init__(self, other, x, y,
                 initial_geometry=False):
        self.x = x
        self.y = y
        self.plant_id = other.max_id
        self.species = other.species
        self.args = other.xml_args
        self.survival = 1
        self.group_name = other.group_name
        self.plant_model = other.plant_model

        species_file_exists = os.path.isfile(os.path.join("PopulationLib", "Species", self.species, self.species + ".py"))
        if species_file_exists:
            module_name = 'PopulationLib.Species.' + self.species
            module = importlib.import_module(module_name)
            self.geometry, self.parameter = module.createPlant()
        elif "/" in self.species:
            try:
                spec = importlib.util.spec_from_file_location("", self.species)
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                self.geometry, self.parameter = foo.createPlant()
            except FileNotFoundError:
                raise FileNotFoundError("The file " + self.species +
                                        " does not exist.")
            except AttributeError:
                raise AttributeError("The file " + self.species + " is not " +
                                     "correctly defining a plant species. "
                                     "Please review the file.")
        else:
            raise KeyError("Species " + self.species + " unknown!")
        if initial_geometry:
            self.geometry.update(initial_geometry)
        self.growth_concept_information = {}

        ## This initialization is only required if networks (root grafts) are
        # simulated
        self.iniNetwork()

    def getPosition(self):
        return self.x, self.y

    def getGeometry(self):
        return self.geometry

    def setGeometry(self, geometry):
        self.geometry = geometry

    def getGrowthConceptInformation(self):
        return self.growth_concept_information

    def setGrowthConceptInformation(self, growth_concept_information):
        self.growth_concept_information = growth_concept_information

    def getParameter(self):
        return self.parameter

    def getSurvival(self):
        return self.survival

    def setSurvival(self, survival):
        self.survival = survival

    def getId(self):
        return self.plant_id

    ## This function initializes a dictionary containing parameters required
    # to build a network of grafted plants
    def iniNetwork(self):
        self.network = {}
        ## Counter to track or define the time required for root graft
        # formation, if -1 no root graft formation takes place at the moment
        self.network['rgf'] = -1
        ## List with the names of plants (plant_name) with which an root graft
        # is currently being formed
        self.network['potential_partner'] = []
        # List with the names of plants (plant_name) with which it is connected
        self.network['partner'] = []
        self.network['groupID'] = []
        self.network['node_degree'] = 0
        self.network['water_absorbed'] = []
        self.network['water_available'] = []
        self.network['water_exchanged'] = []
        ## List with lengths of grafted roots (proportional to r_root of
        # adjacent plants
        self.network['weight_gr'] = 0
        self.network['psi_osmo'] = []
        # List with minimum grafted root radius, only for rgf variant V2
        self.network['r_gr_min'] = []
        self.network['r_gr_rgf'] = []
        self.network['l_gr_rgf'] = []
        self.network['variant'] = None

    def getNetwork(self):
        return self.network

    def setNetwork(self, network):
        self.network = network
