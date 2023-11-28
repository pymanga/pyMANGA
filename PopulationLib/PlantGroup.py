#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import PopulationLib as PLib
from PopulationLib.Dispersal import Dispersal
from PopulationLib.Dispersal.Random import Random


class PlantGroup:
    def __init__(self, xml_args):
        self.xml_args = xml_args # ToDo: unify name for tag variable
        self.plant_model = self.xml_args.find("vegetation_model_type").text
        self.group_name = self.xml_args.find("name").text
        self.species = self.xml_args.find("species").text
        self.max_id = 0
        self.plants = []

        self.dispersal = Dispersal(self.xml_args)

        self.recruitPlants(initial_group=True)
        self.iniPlantDynamicConcept()

    def iniPlantDynamicConcept(self):
        case = self.xml_args.find("vegetation_model_type").text
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
        self.plant_dynamic_concept = createGD(self.xml_args)
        print("Plant dynamics: " + case + ".")

    def recruitPlants(self, initial_group=False):
        positions, geometry = self.dispersal.getPlantAttributes(initial_group=initial_group)
        for i in range(0, len(positions["x"])):
            if isinstance(geometry, dict):
                plant_geometry = {}
                for key, value in geometry.items():
                    plant_geometry[key] = value[i]
            else:
                plant_geometry = geometry[i]
            self.max_id += 1
            self.plants.append(
                PLib.Plant(other=self,
                           x=positions["x"][i],
                           y=positions["y"][i],
                           initial_geometry=plant_geometry))

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