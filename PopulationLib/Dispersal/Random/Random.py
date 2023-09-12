from PopulationLib.Dispersal import Dispersal
import numpy as np


class Random:
    def __init__(self, xml_group):
        print("\t\tCase: Random")
        self.tags_group = xml_group

    def getTags(self):
        print("\t\tgetTags")
        tags = {
            "prj_file": self.tags_group,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "n_individuals"],
            "optional": ["n_recruitment_per_step"]
        }
        return tags

    def initializeGroup(self, others):
        print("\t\tinitializeGroup", others.n_individuals)
        self.xi, self.yi = self.getRandomPositions(others=others,
                                                   number_of_plants=others.n_individuals)

    def recruitPlants(self, others):
        print("\t\trecruitPlants", others.n_recruitment_per_step)
        self.xi, self.yi = self.getRandomPositions(others=others,
                                                   number_of_plants=others.n_recruitment_per_step)

    def getRandomPositions(self, others, number_of_plants):
        print("\t\tgetRandomPositions", others.n_individuals)
        xi, yi = [], []
        for i in range(number_of_plants):
            r_x, r_y = (np.random.rand(2))
            xi.append(others.x_1 + others.l_x * r_x)
            yi.append(others.y_1 + others.l_y * r_y)
        return list([xi, yi])
