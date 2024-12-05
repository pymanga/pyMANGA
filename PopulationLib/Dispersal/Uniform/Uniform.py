import numpy as np
from ProjectLib import helpers as helpers


class Uniform:
    """
    Uniform dispersal module
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
            "required": ["type"]
        }
        myself = super(Uniform, self)
        helpers.getInputParameters(myself, **tags)

    def getPositions(self, number_of_plants, plants):
        """
        Return positions of new plants, which are drawn from a uniform distribution.
        Args:
            number_of_plants (int or dict): number of plants that will be added to the model
        Returns:
            dict
        """
        if np.isscalar(number_of_plants):
            number_of_plants = int(number_of_plants)
        else:
            inds_l = [*number_of_plants.values()]
            number_of_plants = int(sum(sum(x) if isinstance(x, list) else x for x in inds_l))

        xi, yi = [], []
        for i in range(number_of_plants):
            r_x, r_y = np.random.rand(2)
            xi.append(self.x_1 + self.l_x * r_x)
            yi.append(self.y_1 + self.l_y * r_y)
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
