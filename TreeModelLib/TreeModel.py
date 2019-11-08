#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""


class TreeModel:
    def prepareNextTimeStep(self, t_ini, t_end):
        try:
            self.concept.prepareNextTimeStep(t_ini, t_end)
        except AttributeError:
            self.raiseAttributeError("prepareNextTimeStep")

    def addTree(self, x, y, geometry, parameter):
        try:
            self.concept.addTree(x, y, geometry, parameter)
        except AttributeError:
            self.raiseAttributeError("addTree")

    def progressTree(self, tree, aboveground_resources, belowground_resources):
        try:
            self.concept.progressTree(tree, aboveground_resources,
                                      belowground_resources)
        except AttributeError:
            self.raiseAttributeError("progressTree")

    def raiseAttributeError(self, string):
        raise AttributeError("Function '" + string + "' is " +
                             "required for " + self.getConceptType() +
                             " but not implemented!")
