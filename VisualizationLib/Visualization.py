#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""


class Visualization:
    def __init__(self, args):
        self.case = args.find("type").text
        if self.case == "SimplePyplot":
            self.iniSimplePyplot(args)
        else:
            raise KeyError("Required visualization type not implemented.")
        print(self.case + " visualization successfully initiated.")

    def iniSimplePyplot(self, args):
        from .SimplePyplot import SimplePyplot
        self.visualization = SimplePyplot(args)

    def update(self):
        try:
            self.visualization.update()
        except AttributeError:
            self.raiseAttributeError("update")

    def raiseAttributeError(self, string):
        raise AttributeError("Function '" + string + "' is " +
                             "required for " + self.getVisualizationType() +
                             " visualization but not implemented!")

    def getVisualizationType(self):
        return self.case
