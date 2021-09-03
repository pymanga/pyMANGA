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

    def addTree(self, tree):
        try:
            self.concept.addTree(tree)
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

    def getOGSAccessible(self):
        try:
            self.concept.getOGSAccessible()
        except AttributeError:
            self.raiseAttributeError("getOGSAccessible")

    ## Setter for external information
    def setExternalInformation(self, **args):
        try:
            self.concept.setExternalInformation(**args)
        except AttributeError:
            self.raiseAttributeError("setExternalInformation")

    ## Getter for external information
    def getExternalInformation(self):
        try:
            return self.concept.getExternalInformation()
        except AttributeError:
            self.raiseAttributeError("getExternalInformation")

    def getAbovegroundResources(self):
        return self.aboveground_resources

    def getBelowgroundResources(self):
        return self.belowground_resources
