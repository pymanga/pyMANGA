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

    def updatePositions(self, positions):
        """
        Updates the dictionary of plant positions.
        If a random number is lower than the weight, the plant can establish.
        Args:
            positions (dict): dictionary of xy positions of newly produced plants
        Returns:
            dict
        """
        # Extract xy positions as arrays
        xpos = np.array(positions["x"])
        ypos = np.array(positions["y"])
        establish = []
        # Iterate over all newly produced plants
        for i in range(len(xpos)):
            # Find the closest grid cell
            closest_x = np.abs(self.grid_x - xpos[i]).argmin()
            xidx = np.where(self.grid_x == self.grid_x[closest_x])
            closest_y = np.abs(self.grid_y - ypos[i]).argmin()
            yidx = np.where(self.grid_y == self.grid_y[closest_y])
            idx = np.intersect1d(xidx, yidx)

            # Check if weight is larger than a random uniform number
            r = np.random.uniform(size=1)
            establish.append(r <= self.weights[idx].item())

        establish = np.array(establish).flatten()
        # Keep only plants that 'survived' establishment
        if len(establish) == 0:
            plant_positions = {"x": [], "y": []}
        else:
            plant_positions = {"x": xpos[establish], "y": ypos[establish]}
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
