#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import PopulationLib as PLib
from PopulationLib.Dispersal import Dispersal
from PopulationLib.Plant import Plant


class PlantGroup:

    def addGroup(self, xml_group):
        print("-----------------")
        print("PlantGroup")

        plant_model = xml_group.find("vegetation_model_type").text
        self.group_name = xml_group.find("name").text
        species = xml_group.find("species").text

        dispersal = Dispersal(xml_group)
        xi, yi = dispersal.getPositions()

        for x, y in zip(xi, yi):
            self.addPlant(x=x, y=y,
                          xml_args=xml_group,
                          #group_name=self.group_name,
                          plant_model=plant_model,
                          species=species,
                          initial_geometry=False)

    ## Adds a new plant instance to the plant group
    #  @param x: x-position of the new plant
    #  @param y: y-position of the new plant
    #  @param initial_geometry: controls, whether an initial geometry is
    #  parsed to the plant
    def addPlant(self, x, y, xml_args, plant_model, species, initial_geometry=False):
        print("\t\t\taddPlant")
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
        print("...........")
        print(self.plants)

    def getPlants(self):
        return self.plants

    def getGroupName(self):
        return self.group_name

    def getNumberOfPlants(self):
        return len(self.plants)

    def removePlantsAtIndices(self, indices):
        for i in sorted(indices)[::-1]:
            self.plants.pop(i)
