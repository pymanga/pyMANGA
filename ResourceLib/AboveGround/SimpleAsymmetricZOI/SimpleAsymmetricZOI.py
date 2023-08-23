#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: ronny.peters@tu-dresden.de
"""
import numpy as np
from ResourceLib import ResourceModel


class SimpleAsymmetricZOI(ResourceModel):
    ## SimpleAsymmetricZOI case for aboveground competition concept. Asymmetric
    #  Zone Of Influence with the highest plant at a meshpoint gets all the light at
    #  this meshpoint (BETTINA geometry of a plant assumed).\n
    #  @param Tags to define SimpleAsymmetricZOI: see tag documentation
    #  @date: 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate aboveground competition of type " + case + ".")
        self.getInputParameters(args)
        self.makeGrid(args)

    ## This function returns the AbovegroundResources calculated in the
    #  subsequent timestep.\n
    #  @return: np.array with $N_plant$ scalars
    def calculateAbovegroundResources(self):
        #Array to save value of highest plant with shape = (res_x, res_y)
        canopy_height = np.zeros_like(self.my_grid[0])
        #Array to safe index of highest plant with shape = (res_x, res_y)
        highest_plant = np.full_like(self.my_grid[0], fill_value=-99999)
        #Array to safe number of wins per plant with shape = (n_plants)
        wins = np.zeros_like(self.xe)
        #Array to safe number of grid_points per plant with shape = (n_plants)
        crown_areas = np.zeros_like(self.xe)
        #Iteration over plants to identify highest plant at gridpoint
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
            highest_plant[indices] = i
        #Check for each plant, at which gridpoint it is the highest plant
        for i in range(len(self.xe)):
            wins[i] = len(np.where(highest_plant == i)[0])
        self.aboveground_resources = wins / crown_areas

    ## This function calculates the plant height at a (mesh-)point depending
    #  on the distance from the plant position.\n
    #  @param stem_height - stem height (shape: (n_plants))\n
    #  @param crown_radius - crown radius (shape: (n_plants))\n
    #  @param distance - distance from the stem position(shape: (x_res, y_res))
    def calculateHeightFromDistance(self, stem_height, crown_radius, distance):
        bools = crown_radius > distance
        idx = np.where(bools)
        height = np.zeros_like(distance)
        #Here, the curved top of the plant is considered..
        height[idx] = stem_height + (4 * crown_radius**2 -
                                     distance[idx]**2)**0.5
        return height, bools

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"]
        }
        super().getInputParameters(**tags)
        self._x_1 = self.x_1
        self._x_2 = self.x_2
        self._y_1 = self.y_1
        self._y_2 = self.y_2
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)

    ## This function reads x- and y-domain and mesh resolution
    #  from project file and creates the mesh.\n
    #  @param Tags to define plot size and spatial resolution: see tag documentation
    def makeGrid(self, args):
        l_x = self._x_2 - self._x_1
        l_y = self._y_2 - self._y_1
        x_step = l_x / self.x_resolution
        y_step = l_y / self.y_resolution
        self.min_r_crown = np.max([x_step, y_step]) * 1 / 2**0.5
        xe = np.linspace(self._x_1 + x_step / 2.,
                         self._x_2 - x_step / 2.,
                         self.x_resolution,
                         endpoint=True)
        ye = np.linspace(self._y_1 + y_step / 2.,
                         self._y_2 - y_step / 2.,
                         self.y_resolution,
                         endpoint=True)
        self.my_grid = np.meshgrid(xe, ye)

    ## This functions prepares arrays for the competition
    #  concept. In the SimpleAssymmetricZOI concept, plants geometric measures
    #  are saved in simple lists and the timestepping is updated. Two numpy
    #  arrays similar to the mesh array for canopy height and plant ID of the highest plant
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

    ## Before being able to calculate the resources, all plant entities need
    #  to be added with their current implementation for the next timestep.
    #  @param plant
    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()

        if geometry["r_crown"] < self.min_r_crown:
            print("Error: mesh not fine enough for crown dimensions!")
            print(
                "Please refine mesh or increase initial crown radius above " +
                str(self.min_r_crown) + "m !")
            exit()
        if not ((self._x_1 < x < self._x_2) and (self._y_1 < y < self._y_2)):
            raise ValueError("""It appears as a plant is located outside of the
                             domain, where AC is defined. Please check domains 
                             in project file!!""")
        self.xe.append(x)
        self.ye.append(y)
        self.h_stem.append(geometry["h_stem"])
        self.r_crown.append(geometry["r_crown"])
