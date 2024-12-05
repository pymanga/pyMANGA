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
            "required": ["type"],
            "optional": ["per_individual", "per_ha", "per_model_area"]
        }
        myself = super(FixedRate, self)
        helpers.getInputParameters(myself, **tags)

        if not hasattr(self, "per_model_area"):
            self.per_model_area = None
            print("INFO: Default value for <production><FixedRate><per_ha> is used. Default: ",
                  self.per_model_area)
        if not hasattr(self, "per_individual"):
            self.per_individual = None
            print("INFO: Default value for <production><FixedRate><per_individual> is used. Default: ",
                  self.per_individual)
        if not hasattr(self, "per_ha"):
            self.per_ha = None
            print("INFO: Default value for <production><FixedRate><per_ha> is used. Default: ",
                  self.per_ha)
        if all([self.per_model_area, self.per_ha]):
            print("ERROR in Production module.")
            print("Both parameters, per_model_area and per_ha, are defined but only one can be used.")
            exit()

    def getNumberSeeds(self, plants):
        """
        Get number of seeds/seedlings produced in the current timestep.
        Args:
            plants (dict): plant object, see ``pyMANGA.PopulationLib.PopManager.Plant``
        Returns:
            int or array of length = number of plants in previous timestep
        """
        per_individual, per_ha, per_model_area = 0, 0, 0
        if self.per_individual:
            per_individual = self.getSeedsPerPlant(no_plants=len(plants))
        if self.per_ha:
            per_ha = self.getSeedsPerHa()
        if self.per_model_area:
            per_model_area = self.getSeedsPerModelArea()
        return {"per_individual": per_individual,
                "per_ha": per_ha,
                "per_model_area": per_model_area}

    def getSeedsPerPlant(self, no_plants):
        """
        Create array with the number of seeds/seedlings per plant in the previous timestep.
        Args:
            no_plants (int): number of plants in previous timestep
        Returns:
            array of length = number of plants in previous timestep
        """
        return [self.per_individual] * no_plants

    def getSeedsPerHa(self):
        """
        Calculate number of seeds/seedlings per hectare based on defined spatial domain for the respective group.
        Returns:
            int
        """
        domain_ha = (self.l_x * self.l_y) / 10000
        return domain_ha * self.per_ha

    def getSeedsPerModelArea(self):
        """
        Calculate number of seeds/seedlings per hectare based on defined spatial domain for the respective group.
        Returns:
            int
        """
        return self.per_model_area

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

