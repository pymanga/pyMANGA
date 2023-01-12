#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2022-Today
@author: marie-christin.wimmler@tu-dresden.de based on SimpleAsymmetricZOI
by ronny.peters@tu-dresden.de
"""

import numpy as np
from os import path
from TreeModelLib import TreeModel
from TreeModelLib.GrowthAndDeathDynamics import SimpleBettina


class SoilWaterContent(TreeModel):
    ## SymmetricZOI case for below ground competition concept. Symmetric
    #  Zone Of Influence with trees occupying the same node of the grid share
    #  the below-ground resource of this node equally (BETTINA geometry of a
    #  tree assumed). See Peters 2017: ODD protocol of the model BETTINA IBM\n
    #  @param Tags to define SimpleAsymmetricZOI: see tag documentation
    #  @date: 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        # Grid initialization
        self.makeGrid(args)
        self.initializeSoil(args.find("soil_properties"))
        self.initializePrecipitation(args.find("precipitation"))

    def initializeSoil(self, args):
        # Model initialization
        ## Saturated water content [m**3/m**3]
        self._omega_s = float(args.find("omega_s").text)
        ## Residual water content [m**3/m**3]
        self._omega_r = float(args.find("omega_r").text)
        ## Scaling of matric potential [1/hPA]
        self._alpha = float(args.find("alpha").text)
        ## Measure for pore-size distribution
        self._n = float(args.find("n").text)
        ## Suction pressure [hPa]
        self._psi_matrix = float(args.find("psi_matrix").text)
        ## Soil water content [m**3]
        self._soil_water_content = np.ones_like(self.my_grid[1])
        self._soil_water_content = (
            self._omega_r + (self._omega_s - self._omega_r) / (
                1 + (-self._alpha * self._psi_matrix / 100)**self._n)**(
                    1 - 1 / self._n))

    ## This function prepares the precipitation submodel based on information
    #  provided in the pymanga-config file.
    def initializePrecipitation(self, args):
        file_name = path.join(path.abspath("./"),
                              args.find("data_file").text.strip())
        column_number = int(args.find("precipitation_column_number").text)
        delta_t_per_row = float(args.find("delta_t_per_row").text)

        precipitation = (np.loadtxt(
            file_name, delimiter=";", skiprows=1, usecols=column_number-1))

        # Empty array
        precipitation_data = np.zeros((len(precipitation),2))
        # Times in first col
        precipitation_data[:,0] = delta_t_per_row * np.arange(len(precipitation))
        # Precipitation in second col
        precipitation_data[:,1] = precipitation
        ## Precipitation data [time in [s], precipitation in [mm]]
        self._precipitation_data = precipitation_data

    ## This functions prepares arrays for the competition
    #  concept. In the SymmetricZOI concept, trees geometric measures
    #  are saved in simple lists and the timestepping is updated. \n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self.xe = []
        self.ye = []
        self.r_root = []
        self.r_crown = []
        self.h_stem = []
        self.t_ini = t_ini
        self.t_end = t_end
        self.trees = []
        exit()
        
    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their current implementation for the next timestep.
    #  @param tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()

        if geometry["r_root"] < self.min_r_root:
            print("Error: mesh not fine enough for root dimensions!")
            print("Please refine mesh or increase initial root radius above " +
                  str(self.min_r_root) + "m !")
            exit()
        if not ((self._x_1 < x < self._x_2) and (self._y_1 < y < self._y_2)):
            raise ValueError("""It appears as a tree is located outside of the
                             domain, where BC is defined. Please check domains
                             in project file!!""")
        self.xe.append(x)
        self.ye.append(y)
        self.trees.append(tree)

    ## This function returns the BelowgroundResources calculated in the
    #  subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        for tree in self.trees:
            self.extractRelevantInformation(
                geometry=tree.getGeometry(),
                parameter=tree.getParameter())

    def extractRelevantInformation(self, geometry, parameter):
        SimpleBettina.extractRelevantInformation(
            self=self, geometry=geometry, parameter=parameter)

    def flowLength(self):
        SimpleBettina.flowLength(self=self)

    def treeVolume(self):
        SimpleBettina.treeVolume(self=self)

    def rootSurfaceResistance(self):
        SimpleBettina.rootSurfaceResistance(self=self)

    def xylemResistance(self):
        SimpleBettina.xylemResistance(self=self)

    def deltaPsi(self):
        return SimpleBettina.deltaPsi(self=self)

# =============================================================================
#
#         # Numpy array of shape [res_x, res_y, n_trees]
#         distance = (((self.my_grid[0][:, :, np.newaxis] -
#                       np.array(self.xe)[np.newaxis, np.newaxis, :])**2 +
#                      (self.my_grid[1][:, :, np.newaxis] -
#                       np.array(self.ye)[np.newaxis, np.newaxis, :])**2)**0.5)
#         # Array of shape distance [res_x, res_y, n_trees], indicating which
#         # cells are occupied by tree root plates
#         root_radius = np.array(self.r_root)
#         trees_present = root_radius[np.newaxis, np.newaxis, :] > distance
#
#         # Count all nodes, which are occupied by trees
#         # returns array of shape [n_trees]
#         # BETTINA ODD 2017: variable 'countbelow'
#         tree_counts = trees_present.sum(axis=(0, 1))
#
#         # Calculate reciprocal of cell-own variables (array to count wins)
#         # BETTINA ODD 2017: variable 'compete_below'
#         # [res_x, res_y]
#         trees_present_reci = 1. / trees_present.sum(axis=-1)
#
#         # Sum up wins of each tree = trees_present_reci[tree]
#         n_trees = len(trees_present[0, 0, :])
#         tree_wins = np.zeros(n_trees)
#         for i in range(n_trees):
#             tree_wins[i] = np.sum(trees_present_reci[np.where(
#                 trees_present[:, :, i])])
#
#         self.belowground_resources = tree_wins / tree_counts
#
# =============================================================================
    ## This function calculates the tree height at a (mesh-)point depending
    #  on the distance from the tree position.\n
    #  @param stem_height - stem height (shape: (n_trees))\n
    #  @param crown_radius - crown radius (shape: (n_trees))\n
    #  @param distance - distance from the stem position(shape: (x_res, y_res))
    def calculateHeightFromDistance(self, stem_height, crown_radius, distance):
        bools = crown_radius > distance
        idx = np.where(bools)
        height = np.zeros_like(distance)
        #Here, the curved top of the tree is considered..
        height[idx] = stem_height + (4 * crown_radius**2 -
                                     distance[idx]**2)**0.5
        return height, bools


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
