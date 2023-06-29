import numpy as np
from PopulationLib import PlantGroup


class Random(PlantGroup):
    def __init__(self, args):
        """
        Dispersal concept model.
        Args:
            args:  Random module specifications from project file tags.
        """
        pass

    def initializePopulation(self, args):
        """
        Function initializing tree population of size n_individuals within given rectangular domain.
        Args:
            args: arguments specified in project file. Please see tag

        sets:
            multiple float
        """
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "n_individuals"
        ]
        #  Set default value
        self.n_recruitment = 0
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "n_individuals":
                n_individuals = int(arg.text)
            elif tag == "x_1":
                self.x_1 = float(arg.text)
            elif tag == "x_2":
                x_2 = float(arg.text)
            elif tag == "y_1":
                self.y_1 = float(arg.text)
            elif tag == "y_2":
                y_2 = float(arg.text)
            elif tag == "n_recruitment_per_step":
                self.n_recruitment = int(arg.text)
            if tag != "n_recruitment_per_step":
                try:

                    missing_tags.remove(tag)
                except ValueError:
                    raise ValueError(
                        "Tag " + tag +
                        " not specified for random plant planting!")

        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for random plant planting in project file.")
        self.l_x = x_2 - self.x_1
        self.l_y = y_2 - self.y_1
        x_i, y_i = [], []
        for i in range(n_individuals):
            r_x, r_y = (np.random.rand(2))
            x_i.append(self.x_1 + self.l_x * r_x)
            y_i.append(self.y_1 + self.l_y * r_y)
        self.x_i = x_i
        self.y_i = y_i

    def recruitPlants(self):
        """
        Randomly recruiting trees within given domain.
        Returns: random x and y of n_recruitment in the corresponding domain.
        """
        for i in range(self.n_recruitment):
            r_x, r_y = (np.random.rand(2))
            x_i = self.x_1 + self.l_x * r_x
            y_i = self.y_1 + self.l_y * r_y
            self.addTree(x_i, y_i)