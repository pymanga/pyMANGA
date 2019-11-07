#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BelowgroundCompetition(object):
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

    def addTree(self, x, y, geometry, parameter):
        self.concept.addTree(x, y, geometry, parameter)

    def getBelowgroundResources(self):
        return self.belowground_resources

    def calculateBelowgroundResources(self):
        self.belowground_resources = (
            self.concept.calculateBelowgroundResources())

    def prepareNextTimeStep(self, t_ini, t_end):
        self.concept.prepareNextTimeStep(t_ini, t_end)
