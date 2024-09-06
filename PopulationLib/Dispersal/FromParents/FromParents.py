import numpy as np
from PopulationLib.Dispersal.FromFile import FromFile
from PopulationLib.Dispersal.Random import Random
from ProjectLib.Helpers import *


class FromParents(FromFile, Random):
    """
    FromParents dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        self.xml_args = xml_args
        self.prod_counter = 0
        self.inherit_parameters = False

    def getTags(self, tags):
        """
        Return tags to search for in the project file
        Returns:
            dict
        """
        tags["required"] += ["type", "filename",
                             "initial_population",
                             "formula", "production_nth_timestep"]
        tags["optional"] += ["n_individuals", "filename",
                             "inherit_parameters"]
        return tags

    def iniProductionFormula(self):
        """
        Convert the formula for calculating individual production, given as a string in the project file,
        into an evaluable formula.
        """
        self.production_function = string_to_function(self.formula)

    def isProductionTime(self):
        """
        Verification that seed production is taking place in the current time step.
        Returns:
            bool
        """
        self.prod_counter += 1
        if self.prod_counter % self.production_nth_timestep == 0:
            return True
        else:
            return False

    def getPlantAttributes(self, initial_group, plants):
        positions, geometry, network, parameter = {"x": [], "y": []}, {}, {}, {}

        if initial_group:
            self.iniProductionFormula()
            try:
                if self.initial_population.lower() == "Random".lower():
                    positions, geometry, network, parameter = Random.getPlantAttributes(self=self,
                                                                                        initial_group=True,
                                                                                        plants=plants)

                elif self.initial_population.lower() == "FromFile".lower():
                    positions, geometry, network, parameter = super(FromParents, self).getPlantAttributes(initial_group=True,
                                                                                               plants=plants)
                else:
                    print("Error: Initialization of population '" + self.initial_population +
                          "' not implemented.")
                    exit()
            except AttributeError:
                print("Error: It appears that an attribute defining the initial population is missing."
                      " Make sure that all required attributes are specified in the project file.")
                exit()

        else:
            if self.isProductionTime():
                for plant in plants:
                    dbh = 200 * plant.getGeometry()["r_stem"]
                    y = self.production_function(dbh, 0)
                    prod_fitness = 1
                    if self.inherit_parameters:
                        parameter = plant.getParameter()
                        parameter["parent"] = plant.getId()
                        try:
                            prod_fitness = plant.getParameter()["prod_fitness"]
                        except KeyError:
                            pass
                    number_of_plants = int((10 ** y - 1)*prod_fitness)
                    if number_of_plants > 0:
                        xy_parent = plant.getPosition()
                        positions = self.getChildPosition(number_of_plants=number_of_plants,
                                                          xy_parent=xy_parent)
                        geometry = np.full(len(positions["x"]), False)

        return positions, geometry, network, parameter

    def getChildPosition(self, number_of_plants, xy_parent):
        # ToDo: Einschränkung Modeldomain fehlt noch
        self.inherit_radius = 5
        xi = np.random.uniform(low=xy_parent[0]-self.inherit_radius, high=xy_parent[0]+self.inherit_radius, size=number_of_plants)
        yi = np.random.uniform(low=xy_parent[1]-self.inherit_radius, high=xy_parent[1]+self.inherit_radius, size=number_of_plants)
        return {"x": xi, "y": yi}



