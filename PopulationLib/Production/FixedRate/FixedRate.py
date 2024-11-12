from ProjectLib import helpers as helpers


class FixedRate:
    """
    FixedRate production module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): production module specifications from project file tags
        """
        self.getInputParameters(args=xml_args)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "n_individuals"],
            "optional": ["per_individual", "per_ha"]
        }
        myself = super(FixedRate, self)
        helpers.getInputParameters(myself, **tags)

        if not hasattr(self, "per_individual"):
            self.per_individual = False
            print("INFO: Default value for <production><FixedRate><per_individual> is used. Default: ",
                  self.per_individual)
        if not hasattr(self, "per_ha"):
            self.per_ha = False
            print("INFO: Default value for <production><FixedRate><per_ha> is used. Default: ",
                  self.per_ha)
        if self.per_individual and self.per_ha:
            print("ERROR in Production module.")
            print("Both parameters, per_individual and per_ha are set True but only one can be True.")
            exit()

    def getSeedsPerPlant(self, no_plants):
        """
        Create array with the number of seeds/seedlings per plant in the previous timestep.
        Args:
            no_plants (int): number of plants in previous timestep
        Returns:
            array of length = number of plants in previous timestep
        """
        return [self.n_individuals] * no_plants

    def getSeedsPerHa(self):
        """
        Calculate number of seeds/seedlings per hectare based on defined spatial domain for the respective group.
        Returns:
            int
        """
        domain_ha = (self.l_x * self.l_y) / 10000
        return domain_ha * self.n_individuals

    def getNumberSeeds(self, plants):
        """
        Get number of seeds/seedlings produced in the current timestep.
        Args:
            plants (dict): plant object, see ``pyMANGA.PopulationLib.PopManager.Plant``
        Returns:
            int or array of length = number of plants in previous timestep
        """
        if self.per_individual:
            return self.getSeedsPerPlant(no_plants=len(plants))
        elif self.per_ha:
            return self.getSeedsPerHa()
        else:
            return self.n_individuals

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

