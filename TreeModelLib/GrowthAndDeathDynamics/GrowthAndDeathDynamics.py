#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GrowthAndDeathDynamics(object):
    ## Concept for tree growth and death dynamics
    #  @VAR case: tree dynamic concept to be used for the model
    #  @date: 2019 - Today
    #  @author: jasper.bathmann@ufz.de

    def __init__(self, args):
        case = args.find("type").text
        if case == "SimpleTest":
            self.iniSimpleTest(args)
        else:
            raise KeyError("Required growth and death not implemented.")
        print(case + " growth and death dynamics initiated.")

    def iniSimpleTest(self, args):
        from .SimpleTest import SimpleTest
        self.concept = SimpleTest.SimpleTest(args)

    def progressTree(self, tree, aboveground_resources, belowground_resources):
        self.concept.progressTree(tree, aboveground_resources,
                                  belowground_resources)

    def prepareNextTimeStep(self, t_ini, t_end):
        self.concept.prepareNextTimeStep(t_ini, t_end)
