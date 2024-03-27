import numpy as np
from ResourceLib import ResourceModel
from ProjectLib.Project import MangaProject


class Merge(ResourceModel):
    """
    Merge below-ground resource concept.
    """

    def __init__(self, args):
        """
        Below-ground resource concept.
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        case = args.find("type").text

        try:
            modules = args.find("modules").text
        except AttributeError:
            print("Error: No module specifications found.")

        self.bg_concepts = []
        # Get names of individual modules
        modules = modules.split()
        # Iterate through module list
        for module in modules:
            # Find belowground resource subfolde
            if "network" in module.lower():
                module_dir = 'ResourceLib.BelowGround.Network.'
            else:
                module_dir = 'ResourceLib.BelowGround.Individual.'
            my_instance = MangaProject.importModule(self=self,
                                                    module_name=module,
                                                    modul_dir=module_dir,
                                                    prj_args=args)
            self.bg_concepts.append(my_instance)

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
