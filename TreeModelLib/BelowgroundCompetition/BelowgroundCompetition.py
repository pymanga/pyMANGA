#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BelowgroundCompetition:
    ## Concept for belowground competition
    #  @VAR case: belowground competition concept to be used for the model
    #  @date: 2019 - Today
    #  @author: jasper.bathmann@ufz.de

    def __init__(self, args):
        case = args.find("type").text
        if case == "SimpleTest":
            self.iniSimpleTest(args)
        else:
            raise KeyError("Required belowground competition not implemented.")
        print(case + " belowground competition concept initiated.")

    def iniSimpleTest(self, args):
        from .SimpleTest import SimpleTest
        self.case = args.find("type").text
