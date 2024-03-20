#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

        cases = cases.split()
        for case in cases:
            if not case or case == "NoGrowth":
                self.iniNoGrowth(args)
            elif case == "Random":
                self.iniRandom(args)
            elif case == "RandomGrowth":
                self.iniRandomGrowth(args)
            elif case == "Memory":
                self.iniMemory(args)
            else:
                raise KeyError("Required mortality not implemented. "
                               "Available concepts: `NoGrowth`, `Random`, "
                               "`RandomGrowth`, `Memory`")
            print("Plant mortality: {}.".format(case))

    def iniNoGrowth(self, args):
        """
        Initialize mortality module "NoGrowth".
        Args:
            args: NoGrowth module(s) specification from project file tags
        """
        from .NoGrowth import NoGrowth
        self.mortality_concept.append(NoGrowth(args))

    def iniRandom(self, args):
        """
        Initialize mortality module "Random".
        Args:
            args: Random module(s) specification from project file tags
        """
        from .Random import Random
        self.mortality_concept.append(Random(args))

    def iniRandomGrowth(self, args):
        """
        Initialize mortality module "RandomGrowth".
        Args:
            args: RandomGrowth module(s) specification from project file tags
        """
        from .RandomGrowth import RandomGrowth
        self.mortality_concept.append(RandomGrowth(args))

    def iniMemory(self, args):
        """
        Initialize mortality module "Memory".
        Args:
            args: Memory module(s) specification from project file tags
        """
        from .Memory import Memory
        self.mortality_concept.append(Memory(args))

    def getMortConcept(self):
        """
        Get mortality object.
        Returns:
            mortality object (class)
        """
        return self.mortality_concept
