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
        self.case = args.find("type").text
        if self.case == "NONE":
            self.iniNONE(args)
        elif self.case == "OneTreeOneFile":
            self.iniOneTreeOneFile(args)
        elif self.case == "OneTimestepOneFile":
            self.iniOneTimestepOneFile(args)
        elif self.case == "OneTimestepOneFilePerGroup":
            self.iniOneTimestepOneFilePerGroup(args)
        elif self.case == "OneFile":
            self.iniOneFile(args)
        else:
            raise KeyError("Required tree_output of type '" + self.case +
                           "' not implemented!")
        print(self.case + " tree output sucesscully initiated.")

    ## Constructor for no output generation.
    def iniNONE(self, args):
        from .NONE import NONE
        self.output = NONE(args)

    ## Constructor for output which generates one file per tree.
    def iniOneTreeOneFile(self, args):
        from .OneTreeOneFile import OneTreeOneFile
        self.output = OneTreeOneFile(args)

    ## Constructor for output which generates one file per timestep.
    def iniOneTimestepOneFile(self, args):
        from .OneTimestepOneFile import OneTimestepOneFile
        self.output = OneTimestepOneFile(args)

    ## Constructor for output which generates one file per group per timestep.
    def iniOneTimestepOneFilePerGroup(self, args):
        from .OneTimestepOneFilePerGroup import OneTimestepOneFilePerGroup
        self.output = OneTimestepOneFilePerGroup(args)

    ## Constructor for output which generates one file per simulation.
    def iniOneFile(self, args):
        from .OneFile import OneFile
        self.output = OneFile(args)

    ## Dummy for write output function
    def writeOutput(self, tree_groups, time):
        self.output.writeOutput(tree_groups, time)

    ## Returns output type:
    def getOutputType(self):
        return self.case

    ## This function returns the output directory
    def getOutputDir(self):
        return self.output.getOutputDir()
