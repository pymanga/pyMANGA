#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import os
from ResourceLib import ResourceModel


class FixedSalinity(ResourceModel):
    def __init__(self, args):
        """
        Below-ground resource concept.
        Args:
            args: FixedSalinity module specifications from project file tags
        """
        case = args.find("type").text
        self.variant = None
        self.getInputParameters(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        self._h_stem = []
        self._r_crown = []
        self._psi_leaf = []
        self._xe = []
        self._t_ini = t_ini
        self._t_end = t_end
        self._salt_effect_d = []
        self._salt_effect_ui = []

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self._xe.append(x)
        self._h_stem.append(geometry["h_stem"])
        self._r_crown.append(geometry["r_crown"])
        self._psi_leaf.append(parameter["leaf_water_potential"])

        if self.variant == "forman":
            self._salt_effect_d.append(parameter["salt_effect_d"])
            self._salt_effect_ui.append(parameter["salt_effect_ui"])

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on pore-water salinity below the
        center of each plant.
        Sets:
            numpy array of shape(number_of_trees)
        """
        salinity_plant = self.getPlantSalinity()

        if self.variant is None or self.variant == "bettina":
            psi_zero = np.array(self._psi_leaf) + (2 * np.array(self._r_crown) +
                                                   np.array(self._h_stem)) * 9810
            psi_sali = np.array(psi_zero) + 85000000 * salinity_plant
            self.belowground_resources = psi_sali / psi_zero
        if self.variant == "forman":
            # eq. requires salinity in ppt not kg/kg
            self.belowground_resources = (1 / (1 + np.exp(
                np.array(self._salt_effect_d) *
                (np.array(self._salt_effect_ui) - (salinity_plant/10**3)))))

    def getPlantSalinity(self):
        """
        Calculate pore-water salinity below each tree, interpolating over space and time.
        Returns:
            numpy array with shape(number_of_trees)
        """
        self._xe = np.array(self._xe)
        if hasattr(self, "t_variable"):
            self.getSalinityTimeseries()
        elif hasattr(self, "amplitude"):
            self.getSalinitySine()
        # Interpolation of salinity over space
        salinity_plant = ((self._xe - self._min_x) /
                         (self._max_x - self._min_x) *
                         (self._salinity[1] - self._salinity[0]) +
                         self._salinity[0])

        return salinity_plant

    def getSalinitySine(self):
        left = self.amplitude * np.sin(self._t_ini / self.stretch + self.offset) + self.left_bc
        self._salinity[0] = np.random.normal(size=1, loc=left, scale=self.deviation)
        self._salinity[0] = self._salinity[0] if self._salinity[0] > 0 else 0

        right = self.amplitude * np.sin(self._t_ini / self.stretch + self.offset) + self.right_bc
        self._salinity[1] = np.random.normal(size=1, loc=right, scale=self.deviation)
        self._salinity[1] = self._salinity[1] if self._salinity[1] > 0 else 0

    def getSalinityTimeseries(self):
        # The values for the salinity of the current time step are
        # explicitly given
        if self._t_ini in self._salinity_over_t[:, 0]:
            self._salinity = self._salinity_over_t[np.where(
                self._salinity_over_t[:, 0] == self._t_ini)[0], 1:][0]

        # The values for the salinity of the current time step are not
        # explicitly given and have to be interpolted
        elif self._t_ini not in self._salinity_over_t[:, 0]:

            try:
                # Check if there is a value for salinity before and
                # after the current time step
                ts_after = min(np.where(
                    self._salinity_over_t[:, 0] > self._t_ini)[0])
                ts_before = max(np.where(
                    self._salinity_over_t[:, 0] < self._t_ini)[0])

                # Interpolation of salinity values over time

                # salinity on left bc
                salinity_left = (self._salinity_over_t[ts_before, 1] +
                                 ((self._t_ini -
                                   self._salinity_over_t[ts_before, 0]) *
                                  (self._salinity_over_t[ts_after, 1] -
                                   self._salinity_over_t[ts_before, 1])) /
                                 (self._salinity_over_t[ts_after, 0] -
                                  self._salinity_over_t[ts_before, 0]))

                # salinity on right bc
                salinity_right = (self._salinity_over_t[ts_before, 2] +
                                  ((self._t_ini -
                                    self._salinity_over_t[ts_before, 0]) *
                                   (self._salinity_over_t[ts_after, 2] -
                                    self._salinity_over_t[ts_before, 2])) /
                                  (self._salinity_over_t[ts_after, 0] -
                                   self._salinity_over_t[ts_before, 0]))

                self._salinity = [salinity_left, salinity_right]

            except:
                # If a value is missing before or after the current
                # time step, the last or first available one is used.
                if self._salinity_over_t[0, 0] > self._t_ini:
                    self._salinity = [self._salinity_over_t[0, 1],
                                      self._salinity_over_t[0, 2]]

                elif self._salinity_over_t[0, 0] > self._t_ini:
                    self._salinity = [self._salinity_over_t[-1, 1],
                                      self._salinity_over_t[-1, 2]]

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "min_x", "max_x", "salinity"],
            "optional": ["variant", "sine", "amplitude", "stretch", "offset", "deviation"]
        }
        super().getInputParameters(**tags)
        self._salinity = self.salinity
        self._min_x = self.min_x
        self._max_x = self.max_x
        self.readSalinityTag()
        try:
            self.variant.lower()
        except AttributeError:
            pass

        if hasattr(self, "sine"):
            if not hasattr(self, "amplitude"):
                print("> Set sine parameter 'amplitude' to default: 0")
                self.amplitude = 0
            if not hasattr(self, "stretch"):
                print("> Set sine parameter 'stretch' to default: 58*3600*24")
                self.stretch = 58
            if not hasattr(self, "deviation"):
                print("> Set sine parameter 'deviation' to deviation: 0")
                self.deviation = 0
            if not hasattr(self, "offset"):
                print("> Set sine parameter 'offset' to offset: 0")
                self.offset = 0

    def readSalinityTag(self):
        # Two constant values over time for seaward and
        # landward salinity
        if len(self._salinity.split()) == 2:
            self._salinity = self._salinity.split()
            self._salinity[0] = float(eval(self._salinity[0]))
            self._salinity[1] = float(eval(self._salinity[1]))
            self.left_bc = self._salinity[0]
            self.right_bc = self._salinity[1]

        # Path to a file containing salinity values that vary over time
        elif os.path.exists(self._salinity) is True:

            # Reading salinity values from a csv-file
            self._salinity_over_t = np.loadtxt(
                self._salinity, delimiter=';', skiprows=1)

            # Check if csv separation has worked
            try:
                assert self._salinity_over_t.shape[1] == 3

            except:
                raise (KeyError("Problems occurred when reading" +
                                " the salinity values from the file." +
                                " Please check the file for correct" +
                                " formatting."))

            self.t_variable = True

        else:
            raise (KeyError("Wrong definition of salinity in the " +
                            "belowground competition definition. " +
                            "Please read the " +
                            "corresponding section in the " +
                            "documentation!"))
