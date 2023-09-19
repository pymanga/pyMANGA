#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import PopulationLib as PLib
from PopulationLib.Dispersal import Dispersal


class PlantGroup:
    def __init__(self, xml_group):
        self.xml_group = xml_group # ToDo: unify name for tag variable
        self.max_id = 0
        self.plants = []
        self.name = xml_group.find("name").text

        self.plant_model = self.xml_group.find("vegetation_model_type").text
        self.group_name = self.xml_group.find("name").text
        self.species = self.xml_group.find("species").text

        self.dispersal = Dispersal(self.xml_group)

        self.addGroup()
        self.iniPlantDynamicConcept()

    def iniPlantDynamicConcept(self):
        case = self.xml_group.find("vegetation_model_type").text
        if case == "Default":
            from PlantModelLib.Default import Default as createGD
        elif case == "Bettina":
            from PlantModelLib.Bettina import Bettina as createGD
        elif case == "Kiwi":
            from PlantModelLib.Kiwi import Kiwi as createGD
        elif case == "BettinaNetwork":
            from PlantModelLib.BettinaNetwork import BettinaNetwork as createGD
        else:
            raise KeyError("Required plant dynamic concept not implemented.")
        self.plant_dynamic_concept = createGD(self.xml_group)
        print(case + " plant dynamic concept initiated.")

    def addGroup(self):
        plant_attributes = self.dispersal.getPlantAttributes()

        # ToDo: Brauchen wir die Schleife wirklich doppelt?
        if len(plant_attributes) == 2:
            for i in range(0, len(plant_attributes["x"])):
                self.addPlant(x=plant_attributes["x"][i],
                              y=plant_attributes["y"][i],
                              xml_args=self.xml_group,
                              plant_model=self.plant_model,
                              species=self.species,
                              initial_geometry=False)
        else:
            for i in range(0, len(plant_attributes["x"])):
                # Build geometry dictionary
                geometry = {}
                for plant_attribute in plant_attributes:
                    # ToDo: Geht das schöner?
                    if plant_attribute != "x" and plant_attribute != "y":
                        geometry[plant_attribute] = plant_attributes[plant_attribute][i]
                self.addPlant(x=plant_attributes["x"][i],
                              y=plant_attributes["y"][i],
                              xml_args=self.xml_group,
                              plant_model=self.plant_model,
                              species=self.species,
                              initial_geometry=geometry)

    ## Adds a new plant instance to the plant group
    #  @param x: x-position of the new plant
    #  @param y: y-position of the new plant
    #  @param initial_geometry: controls, whether an initial geometry is
    #  parsed to the plant
    def addPlant(self, x, y, xml_args, plant_model, species, initial_geometry=False):
        self.max_id += 1
        self.plants.append(
            PLib.Plant(x,
                       y,
                       xml_args=xml_args,
                       species=species,
                       plant_id=self.max_id,
                       initial_geometry=initial_geometry,
                       plant_model=plant_model,
                       group_name=self.group_name))

    def recruitPlants(self):
        self.dispersal.recruitPlants()
        if self.dispersal.n_recruitment_per_step != 0:
            self.addGroup()

    def getPlants(self):
        return self.plants

    def getGroupName(self):
        return self.group_name

    def getNumberOfPlants(self):
        return len(self.plants)

    def removePlantsAtIndices(self, indices):
        for i in sorted(indices)[::-1]:
            self.plants.pop(i)

    def getNRecruits(self):
        return self.dispersal.n_recruitment_per_step