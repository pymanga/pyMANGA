#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree


class AbovegroundCompetition(object):
    ## Concept for aboveground competition
    #  @VAR case: aboveground competition concept to be used for the model.
    #  @date: 2019 - Today
    #  @author: jasper.bathmann@ufz.de

    def __init__(self, args):
        case = args.find("type").text
        if case == "SimpleTest":
            self.iniSimpleTest(args)
        else:
            raise KeyError("Required aboveground competition not implemented.")
        print(case + " aboveground competition successfully initiated.")

    def iniSimpleTest(self, args):
        from .SimpleTest import SimpleTest
        self.concept = SimpleTest.SimpleTest(args)

    def addTree(self, x, y, geometry, parameter):
        self.concept.addTree(x, y, geometry, parameter)

    def getAbovegroundResources(self):
        return self.aboveground_resources

    def calculateAbovegroundResources(self):
        self.aboveground_resources = (
            self.concept.calculateAbovegroundResources())

    def prepareNextTimeStep(self, t_ini, t_end):
        self.concept.prepareNextTimeStep(t_ini, t_end)
