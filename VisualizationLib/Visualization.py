#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""


## Parent class for Visualization
class Visualization:
    ## Constructor for project visualization.
    #  Depending on project-arguments the different constructors are called.
    #  @param args the visualization arguments taken from input
    def __init__(self, args):
        self.case = args.find("type").text
        if self.case == "SimplePyplot":
            self.iniSimplePyplot(args)
        if self.case == "ComplexPyplot":
            self.iniComplexPyplot(args)
        elif self.case == "NONE":
            self.case = "No"
            self.iniNONE(args)
        else:
            raise KeyError("Required visualization type not implemented.")
        print(self.case + " visualization successfully initiated.")

    ## Initiatiates visualization of type Pyplot
    def iniSimplePyplot(self, args):
        from .SimplePyplot import SimplePyplot
        self.visualization = SimplePyplot(args)

    def iniComplexPyplot(self, args):
        from .ComplexPyplot import ComplexPyplot
        self.visualization = ComplexPyplot(args)

    ## Initiates visualization of type NONE
    def iniNONE(self, args):
        from .NONE import NONE
        self.visualization = NONE(args)

    ## Template for update.
    #  All children of this class require this function.
    def update(self, plant_groups, time):
        self.visualization.update(plant_groups, time)

    ## Returns visualization type
    def getVisualizationType(self):
        return self.case

    ## Template for show
    #  All children of this class require this function.
    def show(self, time):
        self.visualization.show(time)
