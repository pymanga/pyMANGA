#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PopulationLib.InitialPop import InitialPop
from PopulationLib.Production import Production
from PopulationLib.Dispersal import Dispersal
from PopulationLib.Dispersal_v310 import Dispersal_v310
from ProjectLib import helpers as helpers
from PopulationLib.PopManager.Plant import Plant


class PlantGroup:
    """
    Module defining structure of a group of plants.
    This method has been restructured with version v3.2.0.
    Backward compatibility is maintained by retaining deprecated objects and methods, indicated by '_v310_'.
    """

    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): group module specifications from project file tags
        """
        self.xml_args = xml_args  # ToDo: unify name for tag variable
        self.max_id = 0
        self.plants = []
        self.positions, self.geometry, self.network = {}, {}, {}
        self.number_of_seeds = None

        self.iniPlantDynamicConcept()

        # Check if pyMANGA <= v3.1.0 needs to be used
        try:
            self.iniDomain()
            self.iniDispersal()
            self.iniInitialPopulation()
            self.iniProduction()
            self.use_v310 = False
        except AttributeError:
            self.dispersal_v310 = Dispersal_v310(self.xml_args)
            self.recruitPlants_v310(initial_group=True)
            self.use_v310 = True
            print("..............................................................................")
            print("... CAUTION ..................................................................")
            print("... This method is deprecated ................................................")
            print("... pyMANGA v3.1.0 is used ...................................................")
            print("... If you want to use a newer version of pyMANGA, update the control file ...")
            print("..............................................................................")

    def iniPlantDynamicConcept(self):
        """
        Initialize plant module selected in the project-file.
        """
        try:
            self.plant_model = self.xml_args.find("vegetation_model_type").text
            self.group_name = self.xml_args.find("name").text
            self.species = self.xml_args.find("species").text
        except AttributeError:
            print("Error: Missing input parameters (in project file) for population initialization (i.e., "
                  "'vegetation_model_type', 'name', 'species').")
            exit()

        # Class needs to be imported on demand to avoid circular import
        from ProjectLib.Project import MangaProject
        case = self.xml_args.find("vegetation_model_type").text
        module_dir = 'PlantModelLib.'
        self.plant_dynamic_concept = MangaProject.importModule(self=self,
                                                               module_name=case,
                                                               modul_dir=module_dir,
                                                               prj_args=self.xml_args)
        print("Plant dynamics: " + case + ".")

    def iniDomain(self):
        """
        Initialize the model domain, i.e. set domain boundaries in submodules.
        """
        tags = {
            "prj_file": self.xml_args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2"]
        }
        myself = super(PlantGroup, self)
        helpers.getInputParameters(myself, **tags)

    def iniInitialPopulation(self):
        """
        Initialize the initial population module.
        """
        initial_population = InitialPop(self.xml_args.find("initial_population"))
        try:
            initial_population.setModelDomain(x1=self.x_1, x2=self.x_2,
                                              y1=self.y_1, y2=self.y_2)
        except AttributeError:
            pass
        positions, geometry, network = initial_population.getPlantAttributes()
        self.planting(positions, geometry, network)

    def iniProduction(self):
        """
        Initialize the seedling production module.
        """
        self.production = Production(self.xml_args.find("production"))
        try:
            self.production.setModelDomain(x1=self.x_1, x2=self.x_2,
                                           y1=self.y_1, y2=self.y_2)
        except AttributeError:
            pass

    def iniDispersal(self):
        """
        Initialize the seedling dispersal module.
        """
        self.dispersal = Dispersal(self.xml_args.find("dispersal"))
        self.dispersal.setModelDomain(x1=self.x_1, x2=self.x_2,
                                      y1=self.y_1, y2=self.y_2)

    def setNumberOfSeeds(self):
        """
        Set the number of new seeds or seedlings produced.
        """
        self.number_of_seeds = self.production.getNumberSeeds(plants=self.plants)

    def recruitPlants(self):
        """
        Add new plants to the model.
        The number of seeds or seedlings depends on the selected <production> module,
        and the position depends on the selected <dispersal> module.
        """
        if self.use_v310:
            self.recruitPlants_v310()
        else:
            self.setNumberOfSeeds()
            if self.number_of_seeds:
                positions = self.dispersal.getPositions(number_of_plants=self.number_of_seeds,
                                                        plants=self.plants)
                geometry = np.full(len(positions["x"]), False)
                network = {}
                self.planting(positions, geometry, network)

    def planting(self, positions, geometry, network):
        """
        Add new plants to the model, by calling Plant object.
        Args:
            positions (dict): plant positions
            geometry (dict): plant geometries
            network (dict): plant network characteristics
        """
        for i in range(0, len(positions["x"])):
            # If geometry and network are defined, use these values
            # Else fill dictionaries with 0
            if isinstance(geometry, dict):
                plant_geometry = {}
                for key, value in geometry.items():
                    plant_geometry[key] = value[i]
            else:
                plant_geometry = geometry[i]
            if isinstance(network, dict):
                plant_network = {}
                for key, value in network.items():
                    plant_network[key] = value[i]
            else:
                plant_network = network[i]
            self.max_id += 1
            self.plants.append(Plant(other=self,
                                     x=positions["x"][i],
                                     y=positions["y"][i],
                                     initial_geometry=plant_geometry,
                                     initial_network=plant_network))

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
        if self.use_v310:
            return self.dispersal_v310.n_recruitment_per_step
        else:
            return self.number_of_seeds

    def recruitPlants_v310(self, initial_group=False):
        """
        This function is deprecated.
        Add new plants to the model.
        Args:
            initial_group (bool): indicate whether this is model initialization (true) or a later time step (false)
        """
        positions, geometry, network = self.dispersal_v310.getPlantAttributes(initial_group=initial_group)
        for i in range(0, len(positions["x"])):
            if isinstance(geometry, dict):
                plant_geometry = {}
                for key, value in geometry.items():
                    plant_geometry[key] = value[i]
            else:
                plant_geometry = geometry[i]
            if isinstance(network, dict):
                plant_network = {}
                for key, value in network.items():
                    plant_network[key] = value[i]
            else:
                plant_network = network[i]
            self.max_id += 1
            self.plants.append(Plant(other=self,
                                     x=positions["x"][i],
                                     y=positions["y"][i],
                                     initial_geometry=plant_geometry,
                                     initial_network=plant_network))
