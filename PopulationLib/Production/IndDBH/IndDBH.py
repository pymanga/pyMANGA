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
        """
        Convert the formula for calculating individual production, given as a string in the project file,
        into an evaluable formula.
        """
        self.production_function = string_to_function(self.formula)

    def isProductionTime(self):
        """
        Verification that seed production is taking place in the current time step.
        Returns:
            bool
        """
        self.prod_counter += 1
        if self.prod_counter % self.production_nth_timestep == 0:
            return True
        else:
            return False

    def getNumberOfSeeds(self, plants):
        """
        Calculate the total number of seeds produced in the system, based on the individual plant dbh.
        Args:
            plants (dict): dictionary of all plants and there attributes
        Returns:
            integer
        """
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
