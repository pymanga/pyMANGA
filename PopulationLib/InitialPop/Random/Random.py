import numpy as np
from ProjectLib import helpers as helpers
from PopulationLib.Dispersal.Uniform import Uniform


class Random:
    """
    Random dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        self.getInputParameters(args=xml_args)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "n_individuals"]
        }
        myself = super(Random, self)
        helpers.getInputParameters(myself, **tags)

    def getPlantAttributes(self):
        """
        Return group dictionaries (i.e., plant positions, geometries and network parameters).
        Geometry and network are empty dictionaries.
        Returns:
            three dicts
        """
        positions = self.getPositions()
        geometry = np.full(len(positions["x"]), False)
        network = {}
        return positions, geometry, network

    def getPositions(self):
        """
        Handler to calculate positions of plants.
        Args:
            number_of_plants (int): number of plants that will be added to the model
        Returns:
            dict
        """
        plant_positions = Uniform.getPositions(self=self,
                                               number_of_plants=self.n_individuals,
                                               plants={})
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
