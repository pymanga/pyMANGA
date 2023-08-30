#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Mortality:
    def __init__(self, args):
        """
        Constructor to initialize (multiple) mortality modules,
        by calling respective initialization methods.

        Args:
            args: mortality module(s) specification from project file tags
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
                self.iniNoGrowth(args, case)
            elif case == "Random":
                self.iniRandom(args, case)
            elif case == "RandomGrowth":
                self.iniRandomGrowth(args, case)
            elif case == "Memory":
                self.iniMemory(args, case)
            else:
                raise KeyError("Required mortality not implemented. "
                               "Available concepts: `NoGrowth`, `Random`, "
                               "`RandomGrowth`, `Memory`")
            print("Mortality concept set to {}.".format(case))

    def iniNoGrowth(self, args, case):
        """
        Initialize mortality module "NoGrowth".
        Args:
            args: NoGrowth module(s) specification from project file tags
            case: "NoGrowth" (name of the module)
        """
        from .NoGrowth import NoGrowth
        self.mortality_concept.append(NoGrowth(args, case))

    def iniRandom(self, args, case):
        """
        Initialize mortality module "Random".
        Args:
            args: Random module(s) specification from project file tags
            case: "Random" (name of the module)
        """
        from .Random import Random
        self.mortality_concept.append(Random(args, case))

    def iniRandomGrowth(self, args, case):
        """
        Initialize mortality module "RandomGrowth".
        Args:
            args: RandomGrowth module(s) specification from project file tags
            case: "RandomGrowth" (name of the module)
        """
        from .RandomGrowth import RandomGrowth
        self.mortality_concept.append(RandomGrowth(args, case))

    def iniMemory(self, args, case):
        """
        Initialize mortality module "Memory".
        Args:
            args: Memory module(s) specification from project file tags
            case: "Memory" (name of the module)
        """
        from .Memory import Memory
        self.mortality_concept.append(Memory(args, case))

    def getMortConcept(self):
        """
        Get mortality object.
        Returns:
            mortality object (class)
        """
        return self.mortality_concept
