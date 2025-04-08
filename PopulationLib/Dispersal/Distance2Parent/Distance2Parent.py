import numpy as np
from ProjectLib import helpers as helpers


class Distance2Parent:
    """
    Distance2Parent dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): dispersal module specifications from project file tags
        """
        self.xml_args = xml_args
        self.getInputParameters(args=xml_args)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "distribution"],
            "optional": ["scale", "loc", "high"]
        }
        myself = super(Distance2Parent, self)
        helpers.getInputParameters(myself, **tags)

        self.type = self.type.lower()

        # Set default values if not defined in project file
        if not hasattr(self, "scale"):
            self.scale = 1
            print("INFO: Default value for <dispersal><FixedRate><scale> is used. Default: 1")
        if not hasattr(self, "loc"):
            self.loc = 0
            print("INFO: Default value for <dispersal><FixedRate><loc> is used. Default: 0")
        if not hasattr(self, "high"):
            self.high = 1
            print("INFO: Default value for <dispersal><FixedRate><high> is used. Default: 1")

    def getPositions(self, number_of_plants, plants):
        """
        Return positions of new plants, which are drawn from a user-defined distribution.
        Args:
            number_of_plants (int or list of int): number of plants that will be added to the model
            plants (dict): plant object, see ``pyMANGA.PopulationLib.PopManager.Plant``
        Returns:
            dict
        """
        if np.isscalar(number_of_plants):
            print("ERROR: it seems <production><per_individual> is not defined.")
            exit()
        number_of_plants = number_of_plants["per_individual"]

        self.xi, self.yi = [], []
        for i in range(len(plants)):
            plant = plants[i]
            xp, yp = plant.getPosition()
            n = int(number_of_plants[i])
            dist2parent = self.getDistances(number_of_plants=n)
            angle = np.random.uniform(low=0, high=2 * np.pi, size=n)
            self.xi.append(xp + dist2parent * np.sin(angle))
            self.yi.append(yp + dist2parent * np.cos(angle))

        # Flatten lists
        x = np.concatenate(self.xi) if self.xi else np.array([])
        y = np.concatenate(self.yi) if self.yi else np.array([])

        x1, x2 = float(self.x_1), float(self.x_2)
        y1, y2 = float(self.y_1), float(self.y_2)
        # Drop seeds that are outside the model domain
        idx = np.where(np.logical_or.reduce((x < x1, x > x2, y < y1, y > y2)))

        x = np.delete(x, idx)
        y = np.delete(y, idx)

        plant_positions = {"x": x, "y": y}
        return plant_positions

    def getDistances(self, number_of_plants):
        """
        Return distances between seedlings and parent plant.
        Args:
            number_of_plants (int): number of plants that will be added to the model
        Returns:
            list
        """
        try:
            if self.distribution in "normal":
                return np.random.normal(loc=self.loc, scale=self.scale, size=number_of_plants)

            if self.distribution in "uniform":
                return np.random.uniform(size=number_of_plants, high=self.high)

            if self.distribution in "exponential":
                return np.random.exponential(scale=self.scale, size=number_of_plants)

            if self.distribution in "gamma":
                return np.random.gamma(shape=self.loc, scale=self.scale, size=number_of_plants)

            if self.distribution in "weibull":
                return np.random.weibull(a=self.scale, size=number_of_plants)

            if self.distribution in "lognormal":
                return np.random.lognormal(mean=self.loc, sigma=self.scale, size=number_of_plants)

        except AttributeError:
            print("ERROR: A parameter defining the probability density function is missing. "
                  "Check the documentation of <dispersal>.")
            exit()

    def setModelDomain(self, x1, x2, y1, y2):
        """
        Adds model domain boundaries to the object.
        Args:
            x1 (float): x-coordinate of left bottom border of grid
            x2 (float): x-coordinate of right bottom border of grid
            y1 (float): y-coordinate of left top border of grid
            y2 (float): y-coordinate of right top border of grid
        """
        helpers.setModelDomain(self, x1, x2, y1, y2)