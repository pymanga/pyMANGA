from PopulationLib.Dispersal import Dispersal
import numpy as np


class Random:
    def __init__(self, xml_group):
        self.tags_group = xml_group

    def getTags(self):
        tags = {
            "prj_file": self.tags_group,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "n_individuals"],
            "optional": ["n_recruitment_per_step"]
        }
        return tags

    def initializeGroup(self, others):
        self.plant_attributes = self.getRandomPositions(others=others,
                                                        number_of_plants=others.n_individuals)

    def recruitPlants(self, others):
        self.xi, self.yi = self.getRandomPositions(others=others,
                                                   number_of_plants=others.n_recruitment_per_step)

    def getRandomPositions(self, others, number_of_plants):
        xi, yi = [], []
        for i in range(number_of_plants):
            r_x, r_y = (np.random.rand(2))
            xi.append(others.x_1 + others.l_x * r_x)
            yi.append(others.y_1 + others.l_y * r_y)
        plant_attributes = {"x": xi,
                            "y": yi}
        return plant_attributes
