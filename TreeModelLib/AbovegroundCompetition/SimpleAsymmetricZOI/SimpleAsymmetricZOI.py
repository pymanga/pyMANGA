#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib.AbovegroundCompetition import AbovegroundCompetition


class SimpleAsymmetricZOI(AbovegroundCompetition):
    def __init__(self, args):
        ## SimpleTest case for aboveground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @VAR: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        #left_boundary = args.find("left_boundary").text
        print("Initiate aboveground competition of type " + case + ".")
        self.makeGrid(args)

    def calculateAbovegroundResources(self):
        ## This function returns the AbovegroundResources calculated in the
        #  subsequent timestep. In the SimpleTest concept, for each tree a one
        #  is returned
        #  @return: np.array with $N_tree$ scalars
        for i in range(len(self.xe)):
            distance = ((self.my_grid[0] - self.xe[i])**2 + (self.my_grid[1]-self.ye[i])**2)**0.5
            my_height = self.calculateHeightFromDistance(self.h_stem[i],self.r_crown[i],distance)
            self.crown_area.append(sum(sum(my_height > 0)))
            self.winner[self.canopy_height < my_height] = i
            self.canopy_height = np.maximum(self.canopy_height, my_height)
        for i in range(len(self.xe)):
            self.tree_win.append(sum(sum(self.winner==i)))
        self.aboveground_resources = np.divide(self.tree_win,self.crown_area)
        print(self.crown_area)
        print(self.tree_win)
        print(self.aboveground_resources)
        
    def calculateHeightFromDistance(self,hst,rcr,distance):
        height = rcr-distance
        height = np.maximum(height, 0,height)
        height[height>0] = hst + (4*rcr**2 - distance[height>0]**2)**0.5
        return height

    def makeGrid(self,args):
        missing_tags = [
           "type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"
        ]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "x_resolution":
                x_resolution = int(arg.text)
            if tag == "y_resolution":
                y_resolution = int(arg.text)
            elif tag == "x_1":
                x_1 = float(arg.text)
            elif tag == "x_2":
                x_2 = float(arg.text)
            elif tag == "y_1":
                y_1 = float(arg.text)
            elif tag == "y_2":
                y_2 = float(arg.text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError("Tag " + tag +
                                 " not specified for above-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for above-ground grid initialisation in project file.")
        l_x = x_2 - x_1
        l_y = y_2 - y_1
        x_step = l_x / x_resolution
        y_step = l_y / y_resolution
        self.min_r_crown = np.mean([x_step, y_step]) * 2**0.5 
        xe = np.linspace(x_1+x_step/2.,x_2-x_step/2., x_resolution ,endpoint=True) 
        ye = np.linspace(y_1+y_step/2.,y_2-y_step/2., y_resolution ,endpoint=True) 
        self.my_grid = np.meshgrid(xe,ye)

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the competition concept for the competition
        #  concept. In the SimpleTest concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @VAR: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.trees = []
        self.crown_area = []
        self.tree_win = []
        self.xe = []
        self.ye = []
        self.h_stem = []
        self.r_crown = []
        self.t_ini = t_ini
        self.t_end = t_end
        self.canopy_height = np.zeros_like(self.my_grid[0])
        self.winner = np.full_like(self.my_grid[0],fill_value=np.nan)

    def addTree(self, x, y, geometry, parameter):
        ## Before being able to calculate the resources, all tree entities need
        #  to be added with their current implementation for the next timestep.
        #  Here, in the SimpleTest case, each tree is represented by a one. In
        #  general, an object containing all necessary information should be
        #  stored for each tree
        #  @VAR: position, geometry, parameter
        self.trees.append(1)
        if geometry["r_crown"] < self.min_r_crown:
            print("Error: mesh not fine enough for crown dimensions!")
            print("Please refine mesh or increase initial crown radius above " + str(self.min_r_crown) + "m !")
            exit()
        self.xe.append(x)
        self.ye.append(y)
        self.h_stem.append(geometry["h_stem"])
        self.r_crown.append(geometry["r_crown"])


