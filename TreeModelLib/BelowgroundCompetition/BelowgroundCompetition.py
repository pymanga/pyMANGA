#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TreeModelLib import TreeModel


class BelowgroundCompetition(TreeModel):
    ## Concept for belowground competition
    #  @VAR case: belowground competition concept to be used for the model.
    #  @date: 2019 - Today
    #  @author: jasper.bathmann@ufz.de

    def __init__(self, args):
        case = args.find("type").text
        if case == "SimpleTest":
            self.iniSimpleTest(args)
        else:
            raise KeyError("Required belowground competition not implemented.")
        print(case + " belowground competition successfully initiated.")

    def iniSimpleTest(self, args):
        from .SimpleTest import SimpleTest
        self.concept = SimpleTest(args)

    def getBelowgroundResources(self):
        return self.belowground_resources

    def calculateBelowgroundResources(self):
        self.concept.calculateBelowgroundResources()
        self.belowground_resources = self.concept.getBelowgroundResources()

    def getConceptType(self):
        return "belowground competition concept"
