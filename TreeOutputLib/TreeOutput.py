#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""


## Parent class for tree output
class TreeOutput:
    ## Constructor for tree output calling different constructors depending on
    #  choosen case.
    def __init__(self, args):
        ## String defining case of output
        case = args.find("type").text
        if case == "NONE":
            self.iniNONE(args)
        else:
            raise KeyError("Required tree_output not implemented")
        print(case + " tree output sucesscully initiated.")

    ## Constructor for no output generation.
    def iniNONE(self, args):
        from .NONE import NONE
        self.output = NONE(args)

    ## Dummy for write output function
    def writeOutput(self, tree_groups, time):
        pass
