#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
from ResourceLib import ResourceModel


class FixedSalinity(ResourceModel):
    """
    FixedSalinity below-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        case = args.find("type").text
        self.getInputParameters(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        self.plants = []
        self._h_stem = []
        self._r_crown = []
        self._psi_leaf = []
        self._xe = []
        self._t_ini = t_ini
        self._t_end = t_end
        self._r_salinity = []
        self._salt_effect_d = []
        self._salt_effect_ui = []

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self.plants.append(plant)

        self._xe.append(x)
        self._r_salinity.append(parameter["r_salinity"])
        # The following parameters depend on the salinity response function of the plant
        # (see species file)
        try:
            self._salt_effect_d.append(parameter["salt_effect_d"])
            self._salt_effect_ui.append(parameter["salt_effect_ui"])
        except KeyError:
            self._salt_effect_d.append(None)
            self._salt_effect_ui.append(None)

        try:
            self._h_stem.append(geometry["h_stem"])
            self._r_crown.append(geometry["r_crown"])
            self._psi_leaf.append(parameter["leaf_water_potential"])
        except KeyError:
            self._psi_leaf.append(None)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on pore-water salinity below the
        center of each plant.
        Sets:
            numpy array of shape(number_of_trees)
        """
        salinity_plant = self.getPlantSalinity()
        self.calculatePlantResources(salinity_plant)

        for i, plant in zip(range(0, len(self._xe)), self.plants):
            growth_concept_information = {'salinity': salinity_plant[i]}
            plant.setGrowthConceptInformation(growth_concept_information)

    def calculatePlantResources(self, salinity_plant):
        # find indices with r_salinity = bettina or forman
        idx_f = np.where(np.array(self._r_salinity) == "forman")
        idx_b = np.where(np.array(self._r_salinity) == "bettina")
        self.belowground_resources = np.zeros(len(salinity_plant))
        if "bettina" in self._r_salinity:
            psi_zero = np.array(self._psi_leaf)[idx_b] + (2 * np.array(self._r_crown)[idx_b] +
                                                   np.array(self._h_stem)[idx_b]) * 9810
            psi_sali = np.array(psi_zero) + 85000000 * salinity_plant[idx_b]
            self.belowground_resources[idx_b] = psi_sali / psi_zero
        if "forman" in self._r_salinity:
            # eq. requires salinity in ppt not kg/kg
            exp = np.array(self._salt_effect_d)[idx_f] * \
                  (np.array(self._salt_effect_ui)[idx_f] - salinity_plant[idx_f]*10**3)
            exp = np.array(exp, dtype=np.float32)
            self.belowground_resources[idx_f] = 1 / (1 + np.exp(exp))

    def getPlantSalinity(self):
        """
        Calculate pore-water salinity below each tree, interpolating over space and time.
        Returns:
            numpy array with shape(number_of_trees)
        """
        self.getBorderSalinity()
        # Interpolation of salinity over space
        salinity_plant = ((self._xe - self._min_x) /
                         (self._max_x - self._min_x) *
                         (self._salinity[1] - self._salinity[0]) +
                         self._salinity[0])

        if hasattr(self, "distribution"):
            salinity_plant = self.getSalinityDistribution(salinity_plant)

        return salinity_plant

    def getBorderSalinity(self):
        """
        Determine the salinity at the left and right boundaries of the model.
        """
        self._xe = np.array(self._xe)
        if hasattr(self, "t_variable"):
            self.getSalinityTimeseries()
        elif hasattr(self, "amplitude"):
            self.getSalinitySine()

    def getSalinityDistribution(self, salinity_plant):
        """
        Add stochasticity to the salinity below each plant (in each time step).
        Stochasticity is added based on the selected probability distribution.
        Args:
            salinity_plant (array): salinity below each plant
        Returns:
            numpy array with shape(number_of_trees)
        """
        # Normal distribution
        if self.type.startswith("norm"):
            if self.relative:
                # Standard deviation is provided as relative value
                salinity_plant_new = [np.random.normal(i, i * self.deviation) for i in salinity_plant]
            else:
                # Standard deviation is provided as absolute value
                salinity_plant_new = [np.random.normal(i, self.deviation) for i in salinity_plant]
        # Uniform distribution
        elif self.type.startswith("uni"):
            salinity_plant_new = np.random.uniform(self._salinity[0], self._salinity[1], len(salinity_plant))
        # Poisson distribution
        else:
            print("Error: Distribution parameter 'type =", self.type, "' does not exist. Check possible inputs for"
                  " below-ground resource module `FixedSalinity`.")
            exit()
        salinity_plant_new = np.array(salinity_plant_new)
        salinity_plant_new[salinity_plant_new < 0] = 0

        return salinity_plant_new

    def getSalinitySine(self):
        """
        Calculate salinity of the current time step using a sine function.
        Set salinity at the current time step at the left and right model boundary.
        """
        s0 = self.amplitude * np.sin(self._t_ini / self.stretch + self.offset)
        left = s0 + self.left_bc
        self._salinity[0] = np.random.normal(size=1, loc=left, scale=self.noise)
        self._salinity[0] = self._salinity[0] if self._salinity[0] > 0 else 0

        right = s0 + self.right_bc
        self._salinity[1] = np.random.normal(size=1, loc=right, scale=self.noise)
        self._salinity[1] = self._salinity[1] if self._salinity[1] > 0 else 0

    def getSalinityTimeseries(self):
        """
        Get salinity of the current time step from user-defined time series (csv-file).
        If current time step is not in the time series, interpolate salinity values between
        previous and next time step.
        Set salinity at the current time step at the left and right model boundary.
        """
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
        self.checkSalinityInput()

    def checkSalinityInput(self):
        if any(self._salinity) > 1:
            print("ERROR: Salinity over 1000 ppt. Are you sure the salinity is in the correct unit (i.e., kg/kg, not ppt)?")
            exit()

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "min_x", "max_x", "salinity"],
            "optional": ["sine", "amplitude", "stretch", "offset", "noise",
                         "distribution", "type", "deviation", "relative"]
        }
        super().getInputParameters(**tags)
        self.setDefaultParameters()
        self.checkSalinityInput()

    def setDefaultParameters(self):
        self._salinity = self.salinity
        try:
            self._min_x = self.min_x
            self._max_x = self.max_x
        except AttributeError:
            pass
        self.readSalinityTag()
        self.relative = super().makeBoolFromArg("relative")

        if hasattr(self, "sine"):
            if not hasattr(self, "amplitude"):
                print("> Set sine parameter 'amplitude' to default: 0")
                self.amplitude = 0
            if not hasattr(self, "stretch"):
                print("> Set sine parameter 'stretch' to default: 58*3600*24")
                self.stretch = 58*3600*24
            if not hasattr(self, "noise"):
                print("> Set sine parameter 'noise' to noise: 0")
                self.noise = 0
            if not hasattr(self, "offset"):
                print("> Set sine parameter 'offset' to offset: 0")
                self.offset = 0

        if hasattr(self, "distribution"):
            if not hasattr(self, "type"):
                print("> Set distribution parameter 'type' to default: normal")
                self.distribution = "normal"
            if not hasattr(self, "deviation"):
                print("> Set distribution parameter 'deviation' to default: 0.005 (5 ppt)")
                self.deviation = 5/1000
            if not hasattr(self, "relative"):
                print("> Set distribution parameter 'relative' to default: false")
                self.relative = False

    def readSalinityTag(self):
        """
        Read salinity tag in project file.
        Assign variables depending on user input (numeric or path to csv).
        """
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
            salinity_over_t = pd.read_csv(self._salinity, delimiter=";|,|\t", engine='python')
            self._salinity_over_t = salinity_over_t.to_numpy()
            # Check if csv separation has worked
            try:
                assert self._salinity_over_t.shape[1] == 3
            except AssertionError:
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
