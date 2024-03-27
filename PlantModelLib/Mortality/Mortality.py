#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ProjectLib.Project import MangaProject


class Mortality:
    """
    Constructor to initialize (multiple) mortality modules,
    by calling respective initialization methods.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): mortality module specifications from project file tags
        """
        self.mortality_concept = []
        self.survive = 1

        # Check if mortality concept is defined in project xml
        # Otherwise use default concept
        default_case = "NoGrowth"
        try:
            cases = args.find("mortality").text
        except AttributeError:
            cases = default_case
            print("WARNING: Default Mortality concept '" + default_case +
                  "' is used.")

        # Get names of individual modules
        modules = cases.split()
        # Iterate through module list
        for module in modules:
            # Find belowground resource subfolde
            module_dir = 'PlantModelLib.Mortality.'
            my_instance = MangaProject.importModule(self=self,
                                                    module_name=module,
                                                    modul_dir=module_dir,
                                                    prj_args=args)
            self.mortality_concept.append(my_instance)
            print("Plant mortality: {}.".format(module))

    def getMortConcept(self):
        """
        Get mortality object.
        Returns:
            mortality object (class)
        """
        return self.mortality_concept
