#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2020-Today
@author: ronny.peters@tu-dresden.de
"""
import numpy as np
from TreeModelLib import TreeModel


class FixedSalinity_t_var(TreeModel):
    ## Fixed salinity in belowground competition concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.GetSalinity(args)
        print('________')
        print('ini')
        print('________')
        if not hasattr(self, 'n'):
            self.n = 0

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        salinity_tree = self.getTreeSalinity()
        psi_zero = np.array(self._psi_leaf) + (2 * np.array(self._r_crown) +
                                               np.array(self._h_stem)) * 9810
        psi_sali = np.array(psi_zero) + 85000000 * salinity_tree
        self.belowground_resources = psi_sali / psi_zero

    ## This function returns a list of salinity values for each tree,
    # obtained by interpolation along a defined gradient
    def getTreeSalinity(self):
        self._xe = np.array(self._xe)
        salinity_tree = ((self._xe - self._min_x) /
                         (self._max_x - self._min_x) *
                         (self.salinity[self.n][2] -
                         self.salinity[self.n][1]) +
                         self.salinity[self.n][1])
        return salinity_tree
        print('________')
        print('getTreeSalinity')
        print('________')
        print(self.n)
        print(self.salinity[self.n][1])
        print(self.salinity[self.n][2])

    ## This function reads salinity from the control file.\n
    def GetSalinity(self, args):
        missing_tags = ["salinity_file", "type", "max_x", "min_x"]

        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "salinity_file":
                salinity_file = arg.text
                # MARKER Fehlermeldung
                self.salinity = np.loadtxt(salinity_file, delimiter=';', skiprows=1)
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

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        self._xe.append(x)
        self._h_stem.append(geometry["h_stem"])
        self._r_crown.append(geometry["r_crown"])
        self._psi_leaf.append(parameter["leaf_water_potential"])

    ## This functions prepares the computation of water uptake
    #  by porewater salinity. Only tree height aund leaf
    #  water potential is needed\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self._h_stem = []
        self._r_crown = []
        self._psi_leaf = []
        self._xe = []
        self.n += 1
