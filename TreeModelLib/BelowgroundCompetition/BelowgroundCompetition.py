#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TreeModelLib import TreeModel


class BelowgroundCompetition(TreeModel):
    ## Concept for belowground competition
    #  @param case: belowground competition concept to be used for the model.
    #  @date: 2019 - Today
    #  @author: jasper.bathmann@ufz.de

    def __init__(self, args):
        case = args.find("type").text
        if case == "SimpleTest":
            self.iniSimpleTest(args)
        elif case == "OGSLargeScale3D":
            self.iniOGSLargeScale3D(args)
        elif case == "OGSWithoutFeedback":
            self.iniOGSWithoutFeedback(args)
        elif case == "FON":
            self.iniFON(args)
        elif case == "FixedSalinity":
            self.iniFixedSalinity(args)
        else:
            raise KeyError("Required belowground competition case " + case +
                           " not implemented.")
        print(case + " belowground competition successfully initiated.")

    def iniSimpleTest(self, args):
        from .SimpleTest import SimpleTest
        self.concept = SimpleTest(args)

    def iniOGSLargeScale3D(self, args):
        from .OGSLargeScale3D import OGSLargeScale3D
        self.concept = OGSLargeScale3D(args)

    def iniOGSWithoutFeedback(self, args):
        from .OGSWithoutFeedback import OGSWithoutFeedback
        self.concept = OGSWithoutFeedback(args)

    def iniFON(self, args):
        from .FON import FON
        self.concept = FON(args)

    def iniFixedSalinity(self, args):
        from .FixedSalinity import FixedSalinity
        self.concept = FixedSalinity(args)

    def getBelowgroundResources(self):
        return self.belowground_resources

    def calculateBelowgroundResources(self):
        self.concept.calculateBelowgroundResources()
        self.belowground_resources = self.concept.getBelowgroundResources()

    def getConceptType(self):
        return "belowground competition concept"
