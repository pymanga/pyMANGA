from PopulationLib.Dispersal import Dispersal
import numpy as np


class Random:
    def __init__(self, xml_group):
        print("Population: Random.")
        self.tags_group = xml_group

    def getTags(self):
        tags = {
            "prj_file": self.tags_group,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "n_individuals"],
            "optional": ["n_recruitment_per_step"]
        }
        return tags

    def setTags(self, others):
        # ToDo: DAS MUSS WEG
        self.x_1 = others.x_1
        self.x_2 = others.x_2
        self.y_1 = others.y_1
        self.y_2 = others.y_2
        self.l_x = others.l_x
        self.l_y = others.l_y
        try:
            self.n_recruitment_per_step = others.n_recruitment_per_step
        except:
            pass

    def initializeGroup(self, others):
        self.plant_attributes = self.getRandomPositions(x_1=others.x_1,
                                                        y_1=others.y_1,
                                                        l_x=others.l_x,
                                                        l_y=others.l_y,
                                                        number_of_plants=others.n_individuals)

    def recruitPlants(self, others):
        # TODO Das ist falsch, da return from randomBlabla ein dict ist
        self.xi, self.yi = self.getRandomPositions(x_1=others.x_1,
                                                   y_1=others.y_1,
                                                   l_x=others.l_x,
                                                   l_y=others.l_y,
                                                   number_of_plants=others.n_recruitment_per_step)

    def getRandomPositions(self, x_1, y_1, l_x, l_y, number_of_plants):
        xi, yi = [], []
        for i in range(number_of_plants):
            r_x, r_y = (np.random.rand(2))
            xi.append(x_1 + l_x * r_x)
            yi.append(y_1 + l_y * r_y)
        plant_attributes = {"x": xi,
                            "y": yi}
        return plant_attributes
