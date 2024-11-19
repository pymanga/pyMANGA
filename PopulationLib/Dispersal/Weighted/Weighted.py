import numpy as np
import pandas as pd
from ProjectLib import helpers as helpers


class Weighted:
    """
    Weighted dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): dispersal module specifications from project file tags
        """
        self.xml_args = xml_args
        self.getInputParameters(args=xml_args)
        self.readWeightsFile()

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "weight_file"]
        }
        myself = super(Weighted, self)
        helpers.getInputParameters(myself, **tags)

    def readWeightsFile(self):
        """
        Read grid and weights from csv-file (user input).
        """
        try:
            weight_file = pd.read_csv(self.weight_file, delimiter=";|,|\t", engine='python')
        except pd.errors.ParserError:
            weight_file = pd.read_csv(self.weight_file, delimiter=";", engine='python')

        if not {'x', 'y', 'weight'}.issubset(weight_file.columns):
            print("Error: Wrong column names in weight map file (population > distribution > weight_file).\n"
                  "Required column names: x, y, weight (without quotes).")
            exit()

        self.grid_x = weight_file['x'].to_numpy()
        self.grid_y = weight_file['y'].to_numpy()
        self.weights = weight_file['weight'].to_numpy()
        self.no_weights = len(self.weights)

        self.x_r = np.mean(np.diff(weight_file['x'].unique()))
        self.y_r = np.mean(np.diff(weight_file['y'].unique()))
        if np.max(self.weights) > 1:
            print("WARNING: dispersal weights are > 1.")

    def getPositions(self, number_of_plants, plants):
        """
        Return positions of new plants, which are drawn from a weighted uniform distribution.
        Credits: https://stackoverflow.com/a/15205104
        Credits: http://www.sciencedirect.com/science/article/pii/S002001900500298X
        Args:
            number_of_plants (int or list of int): number of plants that will be added to the model
        Returns:
            dict
        """
        # Get total number of new plants
        if np.isscalar(number_of_plants):
            number_of_plants = int(number_of_plants)
        else:
            number_of_plants = int(np.sum(number_of_plants))

        # Create N random numbers, with N = number of grid cells
        r = np.random.random(self.no_weights) ** (1 / self.weights)
        # Sort numbers and keep K numbers, with K = number of new plants
        idx = np.argsort(-r)[:number_of_plants]

        # Get random position around each grid node
        xi = np.array([np.random.uniform(i - self.x_r, i + self.x_r) for i in self.grid_x[idx]])
        yi = np.array([np.random.uniform(i - self.y_r, i + self.y_r) for i in self.grid_y[idx]])

        # If the new position is outside the domain of the model, place it on the boundary of the model
        xi = np.where(xi < self.x_1, self.x_1, xi)
        xi = np.where(xi > self.l_x, self.l_x, xi)
        yi = np.where(yi < self.y_1, self.y_1, yi)
        yi = np.where(yi > self.l_y, self.l_y, yi)

        # Add xy-coordinates to dictionary
        plant_positions = {"x": xi, "y": yi}
        return plant_positions

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
