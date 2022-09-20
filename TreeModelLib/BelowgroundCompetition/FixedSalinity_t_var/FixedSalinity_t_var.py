#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2020-Today
@author: vollhueter
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition.FixedSalinity import FixedSalinity


class FixedSalinity_t_var(FixedSalinity):
    ## Fixed salinity in belowground competition concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        super().__init__(args)
        if not hasattr(self, 'n'):
            self.n = 0

    ## This function returns a list of salinity values for each tree,
    # obtained by interpolation along a defined gradient which is defined
    # for each time step
    def getTreeSalinity(self):
        self._salinity = self._salinity_over_t[self.n][1:]
        return super().getTreeSalinity()

    ## This function reads salinity from the control file.\n
    def GetSalinity(self, args):
        missing_tags = ["salinity_file", "type", "max_x", "min_x"]

        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "salinity_file":
                self._salinity_over_t = np.loadtxt(arg.text, delimiter=';', skiprows=1)
            if tag == "min_x":
                self._min_x = float(args.find("min_x").text)
            if tag == "max_x":
                self._max_x = float(args.find("max_x").text)

            elif tag == "type":
                case = args.find("type").text
            try:
                missing_tags.remove(tag)
            except ValueError:
                print("WARNING: Tag " + tag + " not specified for " + case +
                      " below-ground " + "initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground initialisation in project file."
            )

    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only tree height aund leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini, t_end)
        self.n += 1
