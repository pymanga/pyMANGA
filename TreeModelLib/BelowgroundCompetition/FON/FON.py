#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition


class FON(BelowgroundCompetition):
    def __init__(self, args):
        ## SimpleTest case for belowground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @param: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.makeGrid(args)

    def calculateBelowgroundResources(self):
        ## This function returns the BelowgroundResources calculated in the
        #  subsequent timestep. In the SimpleTest concept, for each tree a one
        #  is returned
        #  @return: np.array with $N_tree$ scalars
        for i in range(len(self.xe)):
            distance = ((self.my_grid[0] - self.xe[i])**2 + (self.my_grid[1]-self.ye[i])**2)**0.5
            my_fon = self.calculateFonFromDistance(self.r_stem[i],distance)
            self.fon_area.append(sum(sum(my_fon > 0)))
            self.fon_height = self.fon_height + my_fon
        for i in range(len(self.xe)):
            distance = ((self.my_grid[0] - self.xe[i])**2 + (self.my_grid[1]-self.ye[i])**2)**0.5
            my_fon = self.calculateFonFromDistance(self.r_stem[i],distance)
            impact = self.fon_height - my_fon
            impact[my_fon < self.fmin] = 0
            self.fon_impact.append(sum(sum(impact)))
            self.resource_limitation.append(1 - 2 * self.fon_impact[i]/self.fon_area[i])
            if self.resource_limitation[i] < 0:
                self.resource_limitation[i] = 0
        for i in range(len(self.xe)):
            self.salinity_reduction.append(1/(1 +
                 np.exp( self.salt_effect_d[i]*
                 ( self.salt_effect_ui[i]-self.salinity))))
        self.belowground_resources = np.multiply(self.resource_limitation,self.salinity_reduction)
        

    def calculateFonFromDistance(self,rst,distance):
        fon_radius = self.aa * rst ** self.bb
        cc = -np.log(self.fmin)/(fon_radius-rst)
        height = np.exp(-cc * (distance-rst))
        height[height > 1] = 1
        height[height < self.fmin] = 0
        return height

    def makeGrid(self,args):
        missing_tags = [
           "type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution",
           "aa", "bb", "fmin", "salinity"
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
            elif tag == "aa":
                self.aa = float(arg.text)
            elif tag == "bb":
                self.bb = float(arg.text)
            elif tag == "fmin":
                self.fmin = float(arg.text)
            elif tag == "salinity":
                self.salinity = float(arg.text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError("Tag " + tag +
                                 " not specified for below-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground grid initialisation in project file.")
        l_x = x_2 - x_1
        l_y = y_2 - y_1
        x_step = l_x / x_resolution
        y_step = l_y / y_resolution
        self.mesh_size = np.maximum(x_step, y_step) 
        xe = np.linspace(x_1+x_step/2.,x_2-x_step/2., x_resolution ,endpoint=True) 
        ye = np.linspace(y_1+y_step/2.,y_2-y_step/2., y_resolution ,endpoint=True) 
        self.my_grid = np.meshgrid(xe,ye)

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the competition concept for the competition
        #  concept. In the SimpleTest concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @param: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.trees = []
        self.fon_area = []
        self.fon_impact = []
        self.resource_limitation = []
        self.salinity_reduction = []
        self.xe = []
        self.ye = []
        self.salt_effect_d = []
        self.salt_effect_ui = []
        self.r_stem = []
        self.t_ini = t_ini
        self.t_end = t_end
        self.fon_height = np.zeros_like(self.my_grid[0])

    def addTree(self, x, y, geometry, parameter):
        ## Before being able to calculate the resources, all tree enteties need
        #  to be added with their current implementation for the next timestep.
        #  Here, in the SimpleTest case, each tree is represented by a one. In
        #  general, an object containing all necessary information should be
        #  stored for each tree
        #  @param: position, geometry, parameter
        self.trees.append(1)
        if self.mesh_size > 0.25:
             print("Error: mesh not fine enough for FON!")
             print("Please refine mesh to grid size < 0.25m !")
             exit()
        self.xe.append(x)
        self.ye.append(y)
        self.salt_effect_d.append(parameter["salt_effect_d"])
        self.salt_effect_ui.append(parameter["salt_effect_ui"])
        self.r_stem.append(geometry["r_stem"])

