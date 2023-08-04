#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel


class FON(ResourceModel):
    def __init__(self, args):
        """
        Below-ground resource concept.
        Args:
            args: FON module specifications from project file tags
        """
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.makeGrid(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        self._fon_area = []
        self._fon_impact = []
        self._resource_limitation = []
        self._salinity_reduction = []
        self._xe = []
        self._ye = []
        self._salt_effect_d = []
        self._salt_effect_ui = []
        self._r_stem = []
        self._t_ini = t_ini
        self._t_end = t_end
        self._fon_height = np.zeros_like(self._my_grid[0])

    def addPlant(self, plant):
        if self._mesh_size > 0.25:
            print("Error: mesh not fine enough for FON!")
            print("Please refine mesh to grid size < 0.25m !")
            exit()
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self._xe.append(x)
        self._ye.append(y)
        self._salt_effect_d.append(parameter["salt_effect_d"])
        self._salt_effect_ui.append(parameter["salt_effect_ui"])
        self._r_stem.append(geometry["r_stem"])

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on competition and
        pore-water salinity below the centre of each plant.
        Sets:
            numpy array with shape(number_of_plants)
        """
        self._r_stem = np.array(self._r_stem)
        distance = (((self._my_grid[0][:, :, np.newaxis] -
                      np.array(self._xe)[np.newaxis, np.newaxis, :])**2 +
                     (self._my_grid[1][:, :, np.newaxis] -
                      np.array(self._ye)[np.newaxis, np.newaxis, :])**2)**0.5)
        my_fon = self.calculateFonFromDistance(distance=distance)
        #print(my_fon)

        fon_areas = np.zeros_like(my_fon)
        # Add a one, where plant is larger than 0
        fon_areas[np.where(my_fon > 0)] += 1
        # Count all nodes, which are occupied by plants
        # returns array of shape (nplants)
        fon_areas = fon_areas.sum(axis=(0, 1))
        fon_heigths = my_fon.sum(axis=-1)

        fon_impacts = fon_heigths[:, :, np.newaxis] - my_fon
        fon_impacts[np.where(my_fon < self._fmin)] = 0
        fon_impacts = fon_impacts.sum(axis=(0, 1))

        # tree-to-tree competition, eq. (7) Berger & Hildenbrandt (2000)
        stress_factor = fon_impacts / fon_areas
        stress_factor = np.nan_to_num(stress_factor, nan=0)
        resource_limitations = 1 - 2 * stress_factor
        resource_limitations[np.where(resource_limitations < 0)] = 0

        # salt stress factor, eq. (6) Berger & Hildenbrandt (2000)
        salinity_reductions = (1 / (1 + np.exp(
            np.array(self._salt_effect_d) *
            (np.array(self._salt_effect_ui) - self._salinity))))

        self.belowground_resources = resource_limitations * salinity_reductions

    def calculateFonFromDistance(self, distance):
        """
        Calculate the FON height of each plant at each grid point.
        Args:
            distance (int): array of distances of all mesh points to plant position
        Returns:
            numpy array with shape(x_grid_points, y_grid_points, number_of_plants)
        """
        # fon radius, eq. (1) Berger et al. 2002
        fon_radius = self._aa * self._r_stem**self._bb
        cc = -np.log(self._fmin) / (fon_radius - self._r_stem)
        height = np.exp(-cc[np.newaxis, np.newaxis, :] *
                        (distance - self._r_stem[np.newaxis, np.newaxis, :]))
        height[height > 1] = 1
        height[height < self._fmin] = 0
        return height

    def makeGrid(self, args):
        """
        Create the plant interaction grid.
        Args:
            args: FON module specifications from project file tags
        Sets:
            numpy array with shape(x_grid_points, y_grid_points)
        """
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution",
            "y_resolution", "aa", "bb", "fmin", "salinity"
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
                self._aa = float(arg.text)
            elif tag == "bb":
                self._bb = float(arg.text)
            elif tag == "fmin":
                self._fmin = float(arg.text)
            elif tag == "salinity":
                self._salinity = float(arg.text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for below-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground grid initialisation in project file."
            )
        l_x = x_2 - x_1
        l_y = y_2 - y_1
        x_step = l_x / x_resolution
        y_step = l_y / y_resolution
        self._mesh_size = np.maximum(x_step, y_step)
        xe = np.linspace(x_1 + x_step / 2.,
                         x_2 - x_step / 2.,
                         x_resolution,
                         endpoint=True)
        ye = np.linspace(y_1 + y_step / 2.,
                         y_2 - y_step / 2.,
                         y_resolution,
                         endpoint=True)
        self._my_grid = np.meshgrid(xe, ye)

