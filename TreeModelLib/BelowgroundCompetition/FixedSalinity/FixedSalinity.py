#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2020-Today
@author: ronny.peters@tu-dresden.de and vollhueter
"""
import numpy as np
import os
from TreeModelLib import TreeModel

class FixedSalinity(TreeModel):
    ## Fixed salinity in belowground competition concept.
    #  @param: Tags to define FixedSalinity: type, salinity
    #  @date: 2020 - Today
    def __init__(self, args):
        time = args[1]
        self.t_start = float(time.find("t_start").text)
        self.t_end = float(time.find("t_end").text)
        self.delta_t = float(time.find("delta_t").text)

        args = args[0]
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.GetSalinity(args)

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
        if hasattr(self, 'n'):
            self._salinity = self._salinity_over_t[self.n][1:]
            self.n += 1
            print(self._salinity)  # MARKER print for testing
        salinity_tree = ((self._xe - self._min_x) /
                         (self._max_x - self._min_x) *
                         (self._salinity[1] - self._salinity[0]) +
                         self._salinity[0])
        return salinity_tree

    ## This function reads salinity from the control file.\n
    def GetSalinity(self, args):
        missing_tags = ["salinity", "type", "max_x", "min_x"]

        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "salinity":
                if len(arg.text.split()) == 2:
                    print('In the control file, two values were given for ' +
                          'salinity at the landward and seaward boundary ' +
                          'conditions. These are constant over time and are ' +
                          'linearly interpolated over x length.')
                    self._salinity = arg.text.split()
                    self._salinity[0] = float(self._salinity[0])
                    self._salinity[1] = float(self._salinity[1])

                elif os.path.exists(arg.text) is True:
                    print('In the control file a path to a csv file with ' +
                          'values of the salt concentration over time was ' +
                          'found.')
                    n_ts = (self.t_end - self.t_start) / self.delta_t
                    ts = np.arange(0, n_ts)
                    salt = np.loadtxt(arg.text, delimiter=';', skiprows=1)

                    # test whether time series of time steps is continuous
                    # and starts with time step 0
                    if (sum(np.diff(sorted(salt[:, 0])) == 1
                            ) >= salt.shape[0] - 1) and salt[0, 0] == 0:

                        # test whether values are given for each time step
                        if salt.shape[0] < n_ts:
                            # if so, the last given value is set for all
                            # remaining time steps until the end.
                            n = n_ts - salt.shape[0]
                            self._salinity_over_t = np.concatenate(
                                [salt, (salt[-1, :] * np.ones((int(n), 3)))])

                        else:
                            # For every time step datas for salinity exist
                            self._salinity_over_t = salt

                    else:
                        # time series of time steps is not continuous,
                        # interpolation needed
                        salt_1 = np.interp(ts, salt[:, 0], salt[:, 1])
                        salt_2 = np.interp(ts, salt[:, 0], salt[:, 2])
                        self._salinity_over_t = np.array([ts, salt_1,
                                                          salt_2]).T
                    self.n = 0

                else:
                    raise (KeyError('Wrong definition of salinity in the ' +
                                    'control file. Please read the ' +
                                    'corresponding section in the ' +
                                    'documentation!'))

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
                "are not given for below-ground initialisation " +
                'in project file.')

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
