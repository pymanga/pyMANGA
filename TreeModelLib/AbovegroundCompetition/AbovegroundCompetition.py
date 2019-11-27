#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TreeModelLib import TreeModel


class AbovegroundCompetition(TreeModel):
    ## Concept for aboveground competition
    #  @param case: aboveground competition concept to be used for the model.
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
        self.concept = SimpleTest(args)

    def getAbovegroundResources(self):
        return self.aboveground_resources

    def calculateAbovegroundResources(self):
        self.concept.calculateAbovegroundResources()
        self.aboveground_resources = self.concept.getAbovegroundResources()

    def getConceptType(self):
        return "aboveground competition concept"
