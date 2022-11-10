#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: ronny.peters@tu-dresden.de
"""
import numpy as np
from TreeModelLib import TreeModel


class SimpleAsymmetricZOI(TreeModel):
    ## SimpleAsymmetricZOI case for aboveground competition concept. Asymmetric
    #  Zone Of Influence with highest tree at a meshpoint gets all the light at
    #  this meshpoint (BETTINA geometry of a tree assumed).\n
    #  @param Tags to define SimpleAsymmetricZOI: see tag documentation
    #  @date: 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate aboveground competition of type " + case + ".")
        self.makeGrid(args)

    ## This function returns the AbovegroundResources calculated in the
    #  subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateAbovegroundResources(self):
        #Array to save value of highest tree with shape = (res_x, res_y)
        canopy_height = np.zeros_like(self.my_grid[0])
        #Array to safe index of highest tree with shape = (res_x, res_y)
        highest_tree = np.full_like(self.my_grid[0], fill_value=-99999)
        #Array to safe number of wins per tree with shape = (n_trees)
        wins = np.zeros_like(self.xe)
        #Array to safe number of grid_points per tree with shape = (n_trees)
        crown_areas = np.zeros_like(self.xe)
        #Iteration over trees to identify highest tree at gridpoint
        for i in range(len(self.xe)):
            distance = (((self.my_grid[0] - np.array(self.xe)[i])**2 +
                         (self.my_grid[1] - np.array(self.ye)[i])**2)**0.5)
            # As the geometry is "complex", my_height is position dependent
            my_height, canopy_bools = self.calculateHeightFromDistance(
                np.array([self.h_stem[i]]), np.array([self.r_crown[i]]),
                distance)
            crown_areas[i] = np.sum(canopy_bools)
            indices = np.where(np.less(canopy_height, my_height))
            canopy_height[indices] = my_height[indices]
            highest_tree[indices] = i
        #Check for each tree, at which gridpoint it is the highest plant
        for i in range(len(self.xe)):
            wins[i] = len(np.where(highest_tree == i)[0])
        self.aboveground_resources = wins / crown_areas

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
    #  @param Tags to define plot size and spatial resolution: see tag documentation
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
                raise ValueError(
                    "Tag " + tag +
                    " not specified for above-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for above-ground grid initialisation in project file."
            )
        l_x = self._x_2 - self._x_1
        l_y = self._y_2 - self._y_1
        x_step = l_x / x_resolution
        y_step = l_y / y_resolution
        self.min_r_crown = np.max([x_step, y_step]) * 1 / 2**0.5
        xe = np.linspace(self._x_1 + x_step / 2.,
                         self._x_2 - x_step / 2.,
                         x_resolution,
                         endpoint=True)
        ye = np.linspace(self._y_1 + y_step / 2.,
                         self._y_2 - y_step / 2.,
                         y_resolution,
                         endpoint=True)
        self.my_grid = np.meshgrid(xe, ye)

    ## This functions prepares arrays for the competition
    #  concept. In the SimpleAssymmetricZOI concept, trees geometric measures
    #  are saved in simple lists and the timestepping is updated. Two numpy
    #  arrays similar to the mesh array for canopy height and tree ID of highest tree
    #  at corresponding mesh point are initialised. \n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini=t_ini, t_end=t_end)
        self.xe = []
        self.ye = []
        self.h_stem = []
        self.r_crown = []

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their current implementation for the next timestep.
    #  @param tree
    def addTree(self, tree):
        x, y, geometry, parameter = super().addTree(tree=tree)

        if geometry["r_crown"] < self.min_r_crown:
            print("Error: mesh not fine enough for crown dimensions!")
            print(
                "Please refine mesh or increase initial crown radius above " +
                str(self.min_r_crown) + "m !")
            exit()
        if not ((self._x_1 < x < self._x_2) and (self._y_1 < y < self._y_2)):
            raise ValueError("""It appears as a tree is located outside of the
                             domain, where AC is defined. Please check domains 
                             in project file!!""")
        self.xe.append(x)
        self.ye.append(y)
        self.h_stem.append(geometry["h_stem"])
        self.r_crown.append(geometry["r_crown"])
