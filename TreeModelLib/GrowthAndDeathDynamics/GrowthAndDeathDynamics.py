#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TreeModelLib import TreeModel


class GrowthAndDeathDynamics(TreeModel):
    ## Concept for tree growth and death dynamics
    #  @VAR case: tree dynamic concept to be used for the model
    #  @date: 2019 - Today
    #  @author: jasper.bathmann@ufz.de

    def __init__(self, args):
        case = args.find("type").text
        if case == "SimpleTest":
            self.iniSimpleTest(args)
        elif case == "SimpleBettina":
            self.iniSimpleBettina(args)
        else:
            raise KeyError("Required growth and death not implemented.")
        print(case + " growth and death dynamics initiated.")

    def iniSimpleTest(self, args):
        from .SimpleTest import SimpleTest
        self.concept = SimpleTest(args)
  
    def iniSimpleBettina(self, args):
        from .SimpleBettina import SimpleBettina
        self.concept = SimpleBettina(args)

    def getConceptType(self):
        return "growth and death dynamics"
