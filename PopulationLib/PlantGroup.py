#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PopulationLib as PLib
from PopulationLib.Dispersal import Dispersal


class PlantGroup:
    """
    Module defining structure of a group of plants.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args: plant group module specifications from project file tags
        """
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
        """
        Initialize plant module selected in the project-file.
        """
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
        """
        Add new plants to the model.
        Args:
            initial_group (bool): indicate whether this is model initialization (true) or a later time step (false)
        """
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
        """
        Return list with plants.
        Returns:
            list
        """
        return self.plants

    def getGroupName(self):
        """
        Return name of the group.
        Returns:
            string
        """
        return self.group_name

    def getNumberOfPlants(self):
        """
        Return number of trees in the group.
        Returns:
            numeric
        """
        return len(self.plants)

    def removePlantsAtIndices(self, indices):
        """
        Remove dead plants from group.
        Args:
            indices (int): indice(s) of dead plant(s)
        """
        for i in sorted(indices)[::-1]:
            self.plants.pop(i)

    def getNRecruits(self):
        """
        Return number of plants that should be added to the model in each time step.
        Returns:
            numeric
        """
        return self.dispersal.n_recruitment_per_step