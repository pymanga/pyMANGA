#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel


class SymmetricZOI(ResourceModel):
    """
    SymmetricZOI below-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()

    def prepareNextTimeStep(self, t_ini, t_end):
        self.xe = []
        self.ye = []
        self.r_root = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        # ToDo: resolve when all geometries are renamed
        try:
            r_root = geometry["r_root"]
        except KeyError:
            r_root = geometry["r_bg"]
        if r_root < (self.mesh_size * 1 / 2**0.5):
            if not hasattr(self, "allow_interpolation") or not self.allow_interpolation:
                print("ERROR: mesh too course for below-ground module!")
                print("Please refine mesh or increase initial root radius above " +
                      str(self.mesh_size) + "m or allow interpolation.")
                exit()
            else:
                # Find closest node
                cx = self.find_nearest(self.my_grid[0][0], x)
                cy = self.find_nearest(np.transpose(self.my_grid[1])[0], y)
                # Distance between plant and closest node
                dist = ((cx - x) ** 2 + (cy - y) ** 2) ** 0.5
                # Set root radius to the minimum distance between plant and nearest grid cell
                if r_root < dist:
                    r_root = dist

        self.xe.append(x)
        self.ye.append(y)
        self.r_root.append(r_root)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on competition with neighboring plants.
        Sets:
            numpy array with shape(number_of_plants)
        """
        # Numpy array of shape [res_x, res_y, n_plants]
        distance = (((self.my_grid[0][:, :, np.newaxis] -
                      np.array(self.xe)[np.newaxis, np.newaxis, :])**2 +
                     (self.my_grid[1][:, :, np.newaxis] -
                      np.array(self.ye)[np.newaxis, np.newaxis, :])**2)**0.5)

        # Use a tolerance of e^-5 for checking whether a plant covers a grid cell
        allowed_error = np.exp(-20)

        # Check if distance is within the root radius +/- tolerance
        plants_present = np.array(self.r_root)[np.newaxis, np.newaxis, :] >= (distance - allowed_error)

        plants_present_1 = np.array(self.r_root)[np.newaxis, np.newaxis, :] >= distance
        print("plants_present:", plants_present)
        print("plants_present_1:", plants_present)

        difference = plants_present != plants_present_1
        print("Unterschiede (True = unterschiedlich):", difference)
        print("Anzahl Unterschiede:", np.sum(difference))

        # Count all nodes, which are occupied by plants
        # returns array of shape [n_plants]
        # BETTINA ODD 2017: variable 'countbelow'
        plant_counts = plants_present.sum(axis=(0, 1))

        # Calculate reciprocal of cell-own variables (array to count wins)
        # BETTINA ODD 2017: variable 'compete_below'
        # [res_x, res_y]
        denom = plants_present.sum(axis=-1)
        plants_present_reci = np.divide(1, denom, where=denom != 0)

        # Sum up wins of each plant = plants_present_reci[plant]
        n_plants = len(plants_present[0, 0, :])
        plant_wins = np.zeros(n_plants)

        for i in range(n_plants):
            plant_wins[i] = np.sum(plants_present_reci[np.where(
                plants_present[:, :, i])])
        self.belowground_resources = plant_wins / plant_counts

        nan_indices = np.where(np.isnan(self.belowground_resources))[0]
        if len(nan_indices) > 0:
            print(f"NaN detected in belowground_resources for plants at indices: {nan_indices}")
            for i in nan_indices:
                exit()
    def find_nearest(self, array, value):
        """
        Get the nearest value in a list
        Credit: Mateen Ulhaq https://stackoverflow.com/a/2566508
        Args:
            array (list): list of numbers
            value (float): value
        Returns:
            float
        """
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"],
            "optional": ["allow_interpolation"]
        }
        super().getInputParameters(**tags)
        self._x_1 = self.x_1
        self._x_2 = self.x_2
        self._y_1 = self.y_1
        self._y_2 = self.y_2
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)

        self.allow_interpolation = super().makeBoolFromArg("allow_interpolation")

