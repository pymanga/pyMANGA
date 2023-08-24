#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import PopulationLib as PLib

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class PlantGroup:

    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.plants = []
        self.max_id = 0

    ## Adds a new plant instance to the plant group
    #  @param x: x-position of the new plant
    #  @param y: y-position of the new plant
    #  @param initial_geometry: controls, whether an initial geometry is
    #  parsed to the plant
    def addPlant(self, x, y, xml_args, plant_model, initial_geometry=False):
        self.max_id += 1
        self.plants.append(
            PLib.Plant(x,
                       y,
                       xml_args=xml_args,
                       species=self.species,
                       plant_id=self.max_id,
                       initial_geometry=initial_geometry,
                       plant_model=plant_model,
                       group_name=self.name))

    def getPlants(self):
        return self.plants

    def getNumberOfPlants(self):
        return len(self.plants)

    def removePlantsAtIndices(self, indices):
        for i in sorted(indices)[::-1]:
            self.plants.pop(i)
