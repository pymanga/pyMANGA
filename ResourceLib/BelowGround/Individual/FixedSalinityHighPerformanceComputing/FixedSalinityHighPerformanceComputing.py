#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
from ResourceLib import ResourceModel


class FixedSalinityHighPerformanceComputing(ResourceModel):
    """
        FixedSalinity below-ground resource concept (optimized, with improved handling for arrays
        and removed random broadcasting overhead).
        This class computes below-ground resource factors for plants based on soil salinity.
    """
    def __init__(self, args):
        """
            Initialize the FixedSalinityHighPerformanceComputing module by reading parameters from XML.

            Args:
                args (lxml.etree._Element): XML element with below-ground module configuration.
        """
        case = args.find("type").text
        self.getInputParameters(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        """
            Prepare data structures for the next time step.

            Args:
                t_ini (float): Start time of this time step.
                t_end (float): End time of this time step.
        """
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
        """
            Add plant data for salinity calculation.

            Args:
                plant: Plant object with position, geometry, and species parameters.
        """
        x, y = plant.getPosition()   # y is not used, but kept for compatibility
        geometry = plant.getGeometry()
        parameter = plant.getParameter()

        self.plants.append(plant)
        self._xe.append(x)
        self._r_salinity.append(parameter["r_salinity"])
        self._salt_effect_d.append(parameter.get("salt_effect_d", None))
        self._salt_effect_ui.append(parameter.get("salt_effect_ui", None))
        self._h_stem.append(geometry.get("h_stem", 0))
        self._r_crown.append(geometry.get("r_crown", 0))
        self._psi_leaf.append(parameter.get("leaf_water_potential", None))

    def calculateBelowgroundResources(self):
        """
            Apply plant salinity response functions to compute below-ground resource factors.

            Args:
                salinity_plant (numpy.ndarray): Salinity values beneath each plant.
        """
        salinity_plant = self.getPlantSalinity()
        self.calculatePlantResources(salinity_plant)
        for i, plant in enumerate(self.plants):
            gci = plant.getGrowthConceptInformation()
            gci['salinity'] = salinity_plant[i]
            plant.setGrowthConceptInformation(gci)

    def calculatePlantResources(self, salinity_plant):
        arr = np.array(self._r_salinity)
        self.belowground_resources = np.zeros(len(salinity_plant))

        idx_b = np.where(arr == "bettina")
        if idx_b[0].size > 0:
            psi_zero = np.array(self._psi_leaf)[idx_b] + \
                       (2 * np.array(self._r_crown)[idx_b] +
                        np.array(self._h_stem)[idx_b]) * 9810
            psi_sali = psi_zero + 8.5e7 * salinity_plant[idx_b]
            self.belowground_resources[idx_b] = psi_sali / psi_zero

        idx_f = np.where(arr == "forman")
        if idx_f[0].size > 0:
            exp = np.array(self._salt_effect_d)[idx_f] * \
                  (np.array(self._salt_effect_ui)[idx_f] - salinity_plant[idx_f] * 1000)
            exp = np.array(exp, dtype=np.float32)    # Ensure consistent data type
            # This is the reason for the inconsistent results. 
            # In my July 23 version, I used the default float64. 
            # I just checked the original FixedSalinity version, which uses
            # exp = np.array(exp, dtype=np.float32). 
            # In the July 24 version, I chose to keep it consistent with the original FixedSalinity to check the consistency of the results and the accuracy of the calculations.
            self.belowground_resources[idx_f] = 1 / (1 + np.exp(exp))

    def getPlantSalinity(self):
        """
            Calculate the salinity for each plant based on position (x-coordinate)
            and boundary conditions.

            Returns:
                numpy.ndarray: Salinity for each plant.
        """
        self.getBorderSalinity()
        xe = np.array(self._xe)
        salinity_plant = ((xe - self._min_x) /
                         (self._max_x - self._min_x) *
                         (self._salinity[1] - self._salinity[0]) +
                         self._salinity[0])
        if hasattr(self, "distribution"):
            salinity_plant = self.getSalinityDistribution(salinity_plant)
        return salinity_plant

    def getBorderSalinity(self):
        """
            Update boundary salinity values based on current time step.
            Uses time series or sine interpolation if configured.
        """
        self._xe = np.array(self._xe)
        if hasattr(self, "t_variable"):
            self.getSalinityTimeseries()
        elif hasattr(self, "amplitude"):
            self.getSalinitySine()

    def getSalinityDistribution(self, salinity_plant):
        """
            Apply stochastic variation to salinity values based on a specified distribution.

            Args:
                salinity_plant (numpy.ndarray): Base salinity values.
            Returns:
                numpy.ndarray: Randomized salinity values.
        """
        if self.type.startswith("norm"):    
            if self.relative:
                salinity_plant_new = np.random.normal(loc=salinity_plant, scale=salinity_plant * self.deviation)
            else:
                salinity_plant_new = np.random.normal(loc=salinity_plant, scale=self.deviation)
            return np.clip(salinity_plant_new, 0, None)  # salinity >= 0
        elif self.type.startswith("uni"):
            return np.random.uniform(self._salinity[0], self._salinity[1], len(salinity_plant))
        else:
            raise ValueError(f"Error: Distribution parameter 'type = {self.type}' does not exist.")

    def getSalinitySine(self):
        """
            Calculate time-dependent salinity using a sine function and add noise if defined.
        """
        s0 = self.amplitude * np.sin(self._t_ini / self.stretch + self.offset)
        left = s0 + self.left_bc
        self._salinity[0] = max(0, np.random.normal(loc=left, scale=self.noise))
        right = s0 + self.right_bc
        self._salinity[1] = max(0, np.random.normal(loc=right, scale=self.noise))

    def getSalinityTimeseries(self):
        """
            Interpolate or retrieve salinity values from a time series for the current timestep.
        """
        ts = self._salinity_over_t[:, 0]
        if self._t_ini in ts:
            self._salinity = self._salinity_over_t[ts == self._t_ini, 1:][0]
        else:
            idx = np.searchsorted(ts, self._t_ini)
            if idx == 0:
                self._salinity = self._salinity_over_t[0, 1:]
            elif idx >= len(ts):
                self._salinity = self._salinity_over_t[-1, 1:]
            else:
                ts_before = idx - 1
                frac = (self._t_ini - ts[ts_before]) / (ts[idx] - ts[ts_before])
                sal_left = self._salinity_over_t[ts_before, 1] + frac * \
                           (self._salinity_over_t[idx, 1] - self._salinity_over_t[ts_before, 1])
                sal_right = self._salinity_over_t[ts_before, 2] + frac * \
                            (self._salinity_over_t[idx, 2] - self._salinity_over_t[ts_before, 2])
                self._salinity = [sal_left, sal_right]
        self.checkSalinityInput()

    def checkSalinityInput(self):
        """
            Check that salinity values are within valid limits (< 1 kg/kg).
        """
        if np.any(np.array(self._salinity) > 1):
            raise ValueError("ERROR: Salinity over 1000 ppt. Check units.")

    def getInputParameters(self, args):
        """
            Parse input parameters from XML.

            Args:
                args (lxml.etree._Element): XML configuration element.
        """
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
        """
            Set default parameter values when not provided by XML.
        """
        self._salinity = self.salinity
        self._min_x = getattr(self, "min_x", 0)
        self._max_x = getattr(self, "max_x", 1)
        self.readSalinityTag()
        self.relative = super().makeBoolFromArg("relative")

        if hasattr(self, "sine"):
            self.amplitude = getattr(self, "amplitude", 0)
            self.stretch = getattr(self, "stretch", 58 * 3600 * 24)
            self.noise = getattr(self, "noise", 0)
            self.offset = getattr(self, "offset", 0)

        if hasattr(self, "distribution"):
            self.distribution = getattr(self, "distribution", "normal")
            self.deviation = getattr(self, "deviation", 5 / 1000)
            self.relative = getattr(self, "relative", False)

    def readSalinityTag(self):
        """
            Parse the <salinity> tag.
            It can be defined as two constant values or as a CSV file path.
        """
        if isinstance(self._salinity, str) and len(self._salinity.split()) == 2:
            vals = self._salinity.split()
            self._salinity = [float(eval(vals[0])), float(eval(vals[1]))]
            self.left_bc, self.right_bc = self._salinity
        elif os.path.exists(self._salinity):
            salinity_over_t = pd.read_csv(self._salinity, delimiter=";|,|\t", engine='python')
            self._salinity_over_t = salinity_over_t.to_numpy()
            if self._salinity_over_t.shape[1] != 3:
                raise KeyError("Salinity file format error.")
            self.t_variable = True
        else:
            raise KeyError("Wrong salinity definition in belowground competition definition.")
