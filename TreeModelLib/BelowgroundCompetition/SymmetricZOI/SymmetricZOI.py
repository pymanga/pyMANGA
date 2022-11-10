#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2022-Today
@author: marie-christin.wimmler@tu-dresden.de based on SimpleAsymmetricZOI
by ronny.peters@tu-dresden.de
"""

import numpy as np
from TreeModelLib import TreeModel


class SymmetricZOI(TreeModel):
    ## SymmetricZOI case for below ground competition concept. Symmetric
    #  Zone Of Influence with trees occupying the same node of the grid share
    #  the below-ground resource of this node equally (BETTINA geometry of a
    #  tree assumed). See Peters 2017: ODD protocol of the model BETTINA IBM\n
    #  @param Tags to define SimpleAsymmetricZOI: see tag documentation
    #  @date: 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.makeGrid(args)

    ## This functions prepares arrays for the competition
    #  concept. In the SymmetricZOI concept, trees geometric measures
    #  are saved in simple lists and the timestepping is updated. \n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini=t_ini, t_end=t_end)
        self.xe = []
        self.ye = []
        self.r_root = []

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their current implementation for the next timestep.
    #  @param tree
    def addTree(self, tree):
        x, y, geometry, parameter = super().addTree(tree)

        if geometry["r_root"] < self.min_r_root:
            print("Error: mesh not fine enough for crown dimensions!")
            print("Please refine mesh or increase initial root radius above " +
                  str(self.min_r_root) + "m !")
            exit()
        if not ((self._x_1 < x < self._x_2) and (self._y_1 < y < self._y_2)):
            raise ValueError("""It appears as a tree is located outside of the
                             domain, where BC is defined. Please check domains 
                             in project file!!""")
        self.xe.append(x)
        self.ye.append(y)
        self.r_root.append(geometry["r_root"])

    ## This function returns the BelowgroundResources calculated in the
    #  subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        # Numpy array of shape [res_x, res_y, n_trees]
        distance = (((self.my_grid[0][:, :, np.newaxis] -
                      np.array(self.xe)[np.newaxis, np.newaxis, :])**2 +
                     (self.my_grid[1][:, :, np.newaxis] -
                      np.array(self.ye)[np.newaxis, np.newaxis, :])**2)**0.5)
        # Array of shape distance [res_x, res_y, n_trees], indicating which
        # cells are occupied by tree root plates
        root_radius = np.array(self.r_root)
        trees_present = root_radius[np.newaxis, np.newaxis, :] > distance

        # Count all nodes, which are occupied by trees
        # returns array of shape [n_trees]
        # BETTINA ODD 2017: variable 'countbelow'
        tree_counts = trees_present.sum(axis=(0, 1))

        # Calculate reciprocal of cell-own variables (array to count wins)
        # BETTINA ODD 2017: variable 'compete_below'
        # [res_x, res_y]
        trees_present_reci = 1. / trees_present.sum(axis=-1)

        # Sum up wins of each tree = trees_present_reci[tree]
        n_trees = len(trees_present[0, 0, :])
        tree_wins = np.zeros(n_trees)
        for i in range(n_trees):
            tree_wins[i] = np.sum(trees_present_reci[np.where(
                trees_present[:, :, i])])

        self.belowground_resources = tree_wins / tree_counts

    ## This function reads x- and y-domain and mesh resolution
    #  from project file and creates the mesh.\n
    #  @param Tags to define plot size and spatial resolution: see tag
    #  documentation
    def makeGrid(self, args):
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution",
            "y_resolution"
        ]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "x_resolution":
                x_resolution = int(arg.text)
            if tag == "y_resolution":
                y_resolution = int(arg.text)
            elif tag == "x_1":
                self._x_1 = float(arg.text)
            elif tag == "x_2":
                self._x_2 = float(arg.text)
            elif tag == "y_1":
                self._y_1 = float(arg.text)
            elif tag == "y_2":
                self._y_2 = float(arg.text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                print("WARNING: Tag " + tag +
                      " not specified for below-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground grid initialisation in "
                "project file.")
        l_x = self._x_2 - self._x_1
        l_y = self._y_2 - self._y_1
        x_step = l_x / x_resolution
        y_step = l_y / y_resolution
        self.min_r_root = np.max([x_step, y_step]) * 1 / 2**0.5
        xe = np.linspace(self._x_1 + x_step / 2.,
                         self._x_2 - x_step / 2.,
                         x_resolution,
                         endpoint=True)
        ye = np.linspace(self._y_1 + y_step / 2.,
                         self._y_2 - y_step / 2.,
                         y_resolution,
                         endpoint=True)
        self.my_grid = np.meshgrid(xe, ye)
