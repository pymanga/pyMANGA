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
        #for i in range(len(self.xe)):
        distance = (((self.my_grid[0][:, :, np.newaxis] -
                      np.array(self.xe)[np.newaxis, np.newaxis, :])**2 +
                     (self.my_grid[1][:, :, np.newaxis] -
                      np.array(self.ye)[np.newaxis, np.newaxis, :])**2)**0.5)
        my_height, canopy_bools = self.calculateHeightFromDistance(
            np.array(self.h_stem), np.array(self.r_crown), distance)
        #Define empty array of dimensions res_x, res_y, n_trees
        crown_areas = np.zeros_like(my_height)
        #Add a one, where tree is larger than 0
        crown_areas[np.where(canopy_bools)] += 1
        #Count all nodes, which are occupied by trees
        #returns array of shape (ntrees)
        crown_areas = crown_areas.sum(axis=(0, 1))

        # look for largest tree
        canopy_height = np.max(my_height, axis=-1)
        canopy_height[np.where(np.less(canopy_height, 0))] = 0

        #define array to count wins
        wins = np.zeros_like(my_height)
        #indicate, where tree is highest
        wins[np.where(np.equal(my_height, canopy_height[:, :,
                                                        np.newaxis]))] += 1

        #Account for shared wins
        cumwins = wins.sum(axis=-1)
        cumwins[np.where(cumwins == 0)] = -1e-4
        wins = wins / cumwins[:, :, np.newaxis]
        wins[np.where(wins < 0)] = 0
        #Count number of wins
        wins = wins.sum(axis=(0, 1))
        self.aboveground_resources = wins / crown_areas

    ## This function calculates the tree height at a (mesh-)point depending
    #  on the distance from the tree position.\n
    #  @param stem_height - stem height\n
    #  @param crown_radius - crown radius\n
    #  @param distance - distance from the stem position
    def calculateHeightFromDistance(self, stem_height, crown_radius, distance):
        bools = crown_radius[np.newaxis, np.newaxis, :] > distance
        idx = np.where(bools)
        height = np.full_like(distance, fill_value=-99999)
        height[idx] = stem_height[idx[2]] + (4 * crown_radius[idx[2]]**2 -
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
        self.xe = []
        self.ye = []
        self.h_stem = []
        self.r_crown = []
        self.t_ini = t_ini
        self.t_end = t_end

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their current implementation for the next timestep.
    #  @param tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()

        if geometry["r_crown"] < self.min_r_crown:
            print("Error: mesh not fine enough for crown dimensions!")
            print(
                "Please refine mesh or increase initial crown radius above " +
                str(self.min_r_crown) + "m !")
            exit()
        if not ((self._x_1 < x < self._x_2) and 
                (self._y_1 < y < self._y_2)):
            raise ValueError("""It appears as a tree is located outside of the
                             domain, where AC is defined. Please check domains 
                             in project file!!""")
        self.xe.append(x)
        self.ye.append(y)
        self.h_stem.append(geometry["h_stem"])
        self.r_crown.append(geometry["r_crown"])
