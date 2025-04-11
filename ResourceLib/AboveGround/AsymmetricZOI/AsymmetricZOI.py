#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel


class AsymmetricZOI(ResourceModel):
    """
    AsymmetricZOI above-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): above-ground module specifications from project file tags
        """
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()

    def calculateAbovegroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on the asymmetric zone of influence concept.
        Sets:
            numpy array of shape(number_of_trees)
        """
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
                np.array([self.h_stem[i]]), np.array([self.r_ag[i]]),
                distance)
            crown_areas[i] = np.sum(canopy_bools)
            indices = np.where(np.less(canopy_height, my_height))
            canopy_height[indices] = my_height[indices]
            highest_plant[indices] = i
        #Check for each plant, at which gridpoint it is the highest plant
        for i in range(len(self.xe)):
            wins[i] = len(np.where(highest_plant == i)[0])

        self.aboveground_resources = wins / crown_areas

        nan_indices = np.where(np.isnan(self.aboveground_resources))[0]
        if len(nan_indices) > 0:
            print(f"ERROR: NaN detected in aboveground_resources for plants at indices: {nan_indices}")
            exit()
    def calculateHeightFromDistance(self, stem_height, crown_radius, distance):
        """
        Calculate plant heights at each mesh point (node) based on the distance between plant and node.
        Args:
            stem_height (array): stem heights (shape: n_plants)
            crown_radius (array): crown radii (shape: n_plants)
            distance (array): distance between node and stem positions (shape: x_res, y_res)

        Returns:
            array, array (shape: x_res, y_res)
        """
        min_distance = np.min(distance)
        # If crown radius < mesh size, set it to mesh size
        crown_radius[np.where(crown_radius < min_distance)] = min_distance

        bools = crown_radius >= distance
        idx = np.where(bools)
        height = np.zeros_like(distance)
        #Here, the curved top of the plant is considered..
        if self.curved_crown:
            height[idx] = stem_height + (4 * crown_radius ** 2 -
                                         distance[idx] ** 2) ** 0.5
        else:
            height[idx] = stem_height + 2 * crown_radius
        return height, bools

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"],
            "optional": ["allow_interpolation", "curved_crown"]
        }
        super().getInputParameters(**tags)
        self._x_1 = self.x_1
        self._x_2 = self.x_2
        self._y_1 = self.y_1
        self._y_2 = self.y_2
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)

        self.allow_interpolation = super().makeBoolFromArg("allow_interpolation")

        if not hasattr(self, "curved_crown"):
            self.curved_crown = True
            print("INFO: set above-ground parameter curved_crown to default: ", self.curved_crown)
        else:
            self.curved_crown = super().makeBoolFromArg("curved_crown")

    def prepareNextTimeStep(self, t_ini, t_end):
        self.xe = []
        self.ye = []
        self.h_stem = []
        self.r_ag = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        # ToDo: resolve when all geometries are renamed
        try:
            r_ag = geometry["r_crown"]
            h_stem = geometry["h_stem"]
        except KeyError:
            r_ag = geometry["r_ag"]
            h_stem = geometry["height"] - 2*r_ag
        if r_ag < (self.mesh_size * 1 / 2**0.5):
            if not hasattr(self, "allow_interpolation") or not self.allow_interpolation:
                print("Error: mesh not fine enough for crown dimensions!")
                print(
                    "Please refine mesh or increase initial crown radius above " +
                    str(self.mesh_size) + "m !")
                exit()

        self.xe.append(x)
        self.ye.append(y)
        self.h_stem.append(h_stem)
        self.r_ag.append(r_ag)
