import numpy as np
from ResourceLib import ResourceModel


class Merge(ResourceModel):
    """
    Merge below-ground resource concept.
    """
    def __init__(self, args):
        """
        Below-ground resource concept.
        Args:
            args: Merge module specifications from project file tags
        """
        case = args.find("type").text

        try:
            modules = args.find("modules").text
        except AttributeError:
            print("Error: No module specifications found.")

        self.bg_concepts = []
        modules = modules.split()
        for module in modules:
            if module == "FixedSalinity":
                from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity
                self.bg_concepts.append(FixedSalinity(args))
            elif module == "FON":
                from ResourceLib.BelowGround.Individual.FON import FON
                self.bg_concepts.append(FON(args))
            elif module == "OGS":
                from ResourceLib.BelowGround.Individual.OGS import OGS
                self.bg_concepts.append(OGS(args))
            elif module == "FON":
                from ResourceLib.BelowGround.Individual.OGSWithoutFeedback import OGSWithoutFeedback
                self.bg_concepts.append(OGSWithoutFeedback(args))
            elif module == "SymmetricZOI":
                from ResourceLib.BelowGround.Individual.SymmetricZOI import SymmetricZOI
                self.bg_concepts.append(SymmetricZOI(args))
            elif module == "Network":
                from ResourceLib.BelowGround.Network.Network import Network
                self.bg_concepts.append(Network(args))
            elif module == "NetworkFixedSalinity":
                from ResourceLib.BelowGround.Network.NetworkFixedSalinity import NetworkFixedSalinity
                self.bg_concepts.append(NetworkFixedSalinity(args))
            elif module == "NetworkOGS":
                from ResourceLib.BelowGround.Network.NetworkOGS import NetworkOGS
                self.bg_concepts.append(NetworkOGS(args))

    def prepareNextTimeStep(self, t_ini, t_end):
        for bg_concept in self.bg_concepts:
            bg_concept.prepareNextTimeStep(t_ini, t_end)

    def addPlant(self, plant):
        for bg_concept in self.bg_concepts:
            bg_concept.addPlant(plant)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each tree based on specified modules and multiplies the factor of
        all modules with each other.
        Sets:
            numpy array of shape(number_of_trees)
        """
        bg = []
        for bg_concept in self.bg_concepts:
            bg_concept.calculateBelowgroundResources()
            bg.append(bg_concept.getBelowgroundResources())
        bg = np.array(bg).transpose()
        bg = list(map(np.prod, bg))

        self.belowground_resources = bg

