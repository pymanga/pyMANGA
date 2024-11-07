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
        print(">>>>>> Random init")
        self.getInputParameters(args=xml_args)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "n_individuals"]
        }
        myself = super(Random, self)
        helpers.getInputParameters(myself, **tags)

    def getPlantAttributes(self):
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
                                               number_of_plants=self.n_individuals)
        return plant_positions

    def setModelDomain(self, x1, x2, y1, y2):
        print(">>> Random setModelDomain")
        helpers.setModelDomain(self, x1, x2, y1, y2)
