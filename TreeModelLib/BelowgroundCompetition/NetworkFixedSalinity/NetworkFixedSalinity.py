#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from TreeModelLib.BelowgroundCompetition.SimpleNetwork import SimpleNetwork


class NetworkFixedSalinity(SimpleNetwork):
    ## Fixed salinityin belowground competition concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.getInputParameters(args)

    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only tree height and leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        SimpleNetwork.prepareNextTimeStep(self, t_ini, t_end)

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: tree
    def addTree(self, tree):
        SimpleNetwork.addTree(self, tree)

    def calculateBelowgroundResources(self):
        # FixedSalinity start
        self.calculatePsiOsmo()
        # FixedSalinity end

        SimpleNetwork.calculateBelowgroundResources(self)

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculatePsiOsmo(self):
        self._xe = np.array(self._xe)
        salinity_tree = ((self._xe - self._min_x) /
                         (self._max_x - self._min_x) *
                         (self._salinity[1] - self._salinity[0]) +
                         self._salinity[0])
        self._psi_osmo = -85000000 * salinity_tree

    ## This function reads input parameters, e.g. salinity from the control
    # file.
    def getInputParameters(self, args):
        missing_tags = ["salinity", "type", "max_x", "min_x",
                        "variant", "f_radius"]

        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "salinity":
                self._salinity = arg.text.split()
                if len(self._salinity) != 2:
                    raise (
                        KeyError("Two salinity values need to be specified"))
                self._salinity[0] = float(self._salinity[0])
                self._salinity[1] = float(self._salinity[1])
            if tag == "min_x":
                self._min_x = float(args.find("min_x").text)
            if tag == "max_x":
                self._max_x = float(args.find("max_x").text)
            if tag == "f_radius":
                self.f_radius = float(args.find("f_radius").text)
            if tag == "variant":
                self.variant = args.find("variant").text
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for below-ground initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground initialisation in project file."
            )
        if self.variant not in ["V0", "V1", "V2"]:
            raise KeyError(
                "SimpleNetwork variant " + self.variant +
                " is not defined. Existing variants are 'V0', 'V1' and 'V2'."
            )
