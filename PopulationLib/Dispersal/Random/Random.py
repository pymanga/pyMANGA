import numpy as np


class Random:
    """
    Random dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        self.xml_args = xml_args

    def getTags(self, tags):
        """
        Return tags to search for in the project file
        Returns:
            dict
        """
        tags["required"] += ["type", "n_individuals"]
        return tags

    def getPlantAttributes(self, initial_group, plants):
        if initial_group:
            number_of_plants = self.n_individuals
        else:
            number_of_plants = self.n_recruitment_per_step
        positions = self.getPositions(number_of_plants=number_of_plants)
        geometry = np.full(len(positions["x"]), False)
        network, parameter = {}, {}
        return positions, geometry, network, parameter

    def getPositions(self, number_of_plants):
        """
        Handler to calculate positions of plants.
        Args:
            number_of_plants (int): number of plants that will be added to the model
        Returns:
            dict
        """
        if hasattr(self, "weights"):
            # Helper to call method from outside
            getWeightedPositions = getattr(Random, "getWeightedPositions")
            plant_positions = getWeightedPositions(self, number_of_plants)
        else:
            # Helper to call method from outside
            getRandomPositions = getattr(Random, "getRandomPositions")
            plant_positions = getRandomPositions(self, number_of_plants)

        return plant_positions

    def getWeightedPositions(self, number_of_plants):
        """
        Return positions of new plants, which are drawn from a weighted uniform distribution.
        Credits: https://stackoverflow.com/a/15205104
        Credits: http://www.sciencedirect.com/science/article/pii/S002001900500298X
        Args:
            number_of_plants (int): number of plants that will be added to the model
        Returns:
            dict
        """
        r = np.random.random(len(self.weights)) ** (1 / self.weights)
        idx = np.argsort(r)[:number_of_plants]

        xi = np.array([np.random.uniform(i - self.x_r, i + self.x_r) for i in self.grid_x[idx]])
        yi = np.array([np.random.uniform(i - self.x_r, i + self.x_r) for i in self.grid_y[idx]])

        xi = np.where(xi < self.x_1, self.x_1, xi)
        xi = np.where(xi > self.l_x, self.l_x, xi)
        yi = np.where(yi < self.y_1, self.y_1, yi)
        yi = np.where(yi > self.l_y, self.l_y, yi)

        plant_positions = {"x": xi, "y": yi}
        return plant_positions

    def getRandomPositions(self, number_of_plants):
        """
        Return positions of new plants, which are drawn from a uniform distribution.
        Args:
            number_of_plants (int): number of plants that will be added to the model
        Returns:
            dict
        """
        xi, yi = [], []
        for i in range(number_of_plants):
            r_x, r_y = np.random.rand(2)
            xi.append(self.x_1 + self.l_x * r_x)
            yi.append(self.y_1 + self.l_y * r_y)
        plant_positions = {"x": xi, "y": yi}
        return plant_positions
