#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition


class FON(BelowgroundCompetition):
    ## FON case for belowground competition concept. For details see
    #  (https://doi.org/10.1016/S0304-3800(00)00298-2). FON returns a list 
    #  of multipliers for each tree for salinity and competition.\n
    #  @param: Tags to define FON: type\n
    #  @date: 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.makeGrid(args)

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent timestep.\n  
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
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
        
    ## This function returns the fon height of a tree on the mesh.\n
    #  @param rst - FON radius\n
    #  @param distance - array of distances of all mesh points to tree position
    def calculateFonFromDistance(self,rst,distance):
        fon_radius = self.aa * rst ** self.bb
        cc = -np.log(self.fmin)/(fon_radius-rst)
        height = np.exp(-cc * (distance-rst))
        height[height > 1] = 1
        height[height < self.fmin] = 0
        return height

    ## This function initialises the mesh.\n
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

    ## This functions prepares the competition concept for the competition
    #  concept. In the FON concept, tree's allometric measures are saved
    #  in simple lists and the timestepping is updated. A mesh-like array 
    #  is prepared for storing all FON heights of the stand.\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
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

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: position, geometry, parameter
    def addTree(self, x, y, geometry, parameter):
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

