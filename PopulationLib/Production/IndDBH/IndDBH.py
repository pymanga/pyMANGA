from ProjectLib.Helper import *


class IndDBH:
    """
    Random dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): production module specifications from project file tags
        """
        self.xml_args = xml_args
        self.prod_counter = 0

    def getTags(self, tags):
        """
        Return tags to search for in the project file
        Returns:
            dict
        """
        tags["required"] += ["formula", "production_nth_timestep"]
        return tags

    def iniProductionFormula(self):
        self.production_function = string_to_function(self.formula)

    def isProductionTime(self):
        self.prod_counter += 1
        if self.prod_counter % self.production_nth_timestep == 0:
            return True
        else:
            return False

    def getNumberOfSeeds(self, plants):
        if self.isProductionTime():
            no_seeds = []
            for plant in plants:
                dbh = 200 * plant.getGeometry()["r_stem"]
                y = self.production_function(dbh, 0)
                no = 10**y - 1
                no_seeds.append(int(no))
            return sum(no_seeds)
        else:
            return 0
