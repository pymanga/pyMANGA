from PopulationLib.Dispersal import Dispersal
import numpy as np


class Random:
    def __init__(self, xml_args):
        self.xml_args = xml_args

    def getTags(self):
        tags = {
            "prj_file": self.xml_args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "n_individuals"],
            "optional": ["n_recruitment_per_step"]
        }
        return tags

    def getPlantAttributes(self, initial_group):
        if initial_group:
            number_of_plants = self.n_individuals
        else:
            number_of_plants = self.n_recruitment_per_step
        positions = self.getRandomPositions(number_of_plants=number_of_plants)
        geometry = np.full(len(positions["x"]), False)
        return positions, geometry

    def getRandomPositions(self, number_of_plants):
        xi, yi = [], []
        for i in range(number_of_plants):
            r_x, r_y = (np.random.rand(2))
            xi.append(self.x_1 + self.l_x * r_x)
            yi.append(self.y_1 + self.l_y * r_y)
        plant_positions = {"x": xi, "y": yi}
        return plant_positions
