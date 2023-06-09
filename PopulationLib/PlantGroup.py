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
    def addPlant(self, x, y, initial_geometry=False):
        self.max_id += 1
        self.plants.append(
            PLib.Plant(x,
                      y,
                      self.species,
                      self.max_id,
                      initial_geometry,
                      group_name=self.name))

    def getPlants(self):
        return self.plants

    def getNumberOfPlants(self):
        return len(self.plants)

    def removePlantsAtIndices(self, indices):
        for i in sorted(indices)[::-1]:
            self.plants.pop(i)
