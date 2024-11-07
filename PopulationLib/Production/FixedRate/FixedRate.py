import numpy as np
from ProjectLib import helpers as helpers


class FixedRate:
    """
    Random dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        print(">>> FixedRate init")
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

    def getSeedsPerPlant(self, no_plants):
        return [self.n_individuals] * no_plants

    def getSeedsPerHa(self):
        domain_ha = (self.l_x * self.l_y) / 10000
        return domain_ha * self.n_individuals

    def getNumberSeeds(self, plants):
        if self.per_individual:
            return self.getSeedsPerPlant(no_plants=len(plants))
        elif self.per_ha:
            return self.getSeedsPerHa()
        else:
            return self.n_individuals

    def setModelDomain(self, x1, x2, y1, y2):
        print(">>> Uniform setModelDomain")
        helpers.setModelDomain(self, x1, x2, y1, y2)

