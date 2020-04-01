#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2020-Today
@author: ronny.peters@tu-dresden.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition


class FixedSalinity(BelowgroundCompetition):
    def __init__(self, args):
        ## Fixed salinityin belowground competition concept. 
        #  @param: Tags to define FixedSalinity: type, salinity
        #  @date: 2020 - Today
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.GetSalinity(args)

    def calculateBelowgroundResources(self):
        psi_zero = np.array(self._psi_leaf) + (2 * np.array(self._r_crown) + np.array(self._h_stem)) * 9810
        psi_sali = np.array(psi_zero) + 85000000 * np.array(self._salinity)
        self.belowground_resources = psi_sali / psi_zero
  

    def GetSalinity(self, args):
        missing_tags = [
            "salinity", "type"
        ]

        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "salinity":
                self.salinity = float(arg.text)
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

    def addTree(self, x, y, geometry, parameter):
        self._h_stem.append(geometry["h_stem"])
        self._r_crown.append(geometry["r_crown"])
        self._psi_leaf.append(parameter["leaf_water_potential"])
        self._salinity.append(self.salinity)

    def prepareNextTimeStep(self, t_ini, t_end):
        self._h_stem = []
        self._r_crown = []
        self._psi_leaf = []
        self._salinity = [] 

