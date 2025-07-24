#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity


class SaltFeedbackBucketHighPerformanceComputing(FixedSalinity):
    """
    SaltFeedbackBucket High Performance Computing below-ground resource concept.
    """

    def __init__(self, args):
        self.getInputParameters(args)
        self._t_ini = 0
        super().makeGrid() 
        self.getBorderValues()
        self.getInflowSalinity()
        self.getInflowMixingRate()
        self.assignInitialCellSalinity()

    def assignInitialCellSalinity(self):
        """
        Assign initial cell salinity, either from a provided file or the inflow salinity.
        """
        if hasattr(self, "initial_salinity_file"):
            self.sal_cell = np.loadtxt(self.initial_salinity_file, usecols=range(len(self.my_grid[0][0])))
        else:
            self.sal_cell = self.sal_cell_inflow

    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini, t_end)
        self.timesteplength = t_end - t_ini
        self.vol_sink_cell = np.zeros(np.shape(self.my_grid[0]))
        self.plant_cells = []
        self.plants = []

    def addPlant(self, plant):
        xp, yp = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        gci = plant.getGrowthConceptInformation()
        self.plants.append(plant)

        rrp = geometry["r_root"]
        self._r_salinity.append(parameter["r_salinity"])
        self._h_stem.append(geometry["h_stem"])
        self._r_crown.append(geometry["r_crown"])
        self._psi_leaf.append(parameter["leaf_water_potential"])
        self._xe.append(xp)

        try:
            plant_water_uptake = gci["bg_resources"]  # m³ water per time step
        except KeyError:
            plant_water_uptake = 0

        if rrp < self.mesh_size:
            rrp = self.mesh_size

        self.calculatePlantSink(xp, yp, rrp, plant_water_uptake)

    def calculatePlantSink(self, x, y, r_root, bg_resources):
        """
        Assign plant water uptake to affected grid cells.
        """
        idx = self.getAffectedCellsIdx(x, y, r_root)
        self.plant_cells.append(idx)
        if bg_resources != 0:
            no_cells = len(idx[0])
            sink_per_cell = bg_resources / (self.cell_area * no_cells) / self.timesteplength
            self.vol_sink_cell[idx] += sink_per_cell

    def calculateBelowgroundResources(self):
        self.getBorderValues()
        self.getInflowSalinity()
        self.getInflowMixingRate()
        self.calculateCellSalinity()

        salinity_plant = self.getPlantSalinity()
        self.calculatePlantResources(salinity_plant)

        for i, plant in zip(range(0, len(self._xe)), self.plants):
            gci = plant.getGrowthConceptInformation()
            gci['salinity'] = salinity_plant[i]
            plant.setGrowthConceptInformation(gci)

    def getInflowSalinity(self):
        """
        Calculate salinity of inflowing water of each cell.
        """
        if len(self.my_grid[0]) == 1:
            self.sal_cell_inflow = np.array([0.5 * (self._salinity[0] + self._salinity[1])])
        else:
            x_dif = self.x_2 - self.x_1
            self.sal_cell_inflow = (self.my_grid[0] - self.x_1) / x_dif * \
                                   (self._salinity[1] - self._salinity[0]) + self._salinity[0]

    def calculateCellSalinity(self):
        """
        Calculate salinity in each cell based on fresh water extraction and mixing with inflowing water.
        """
        ht = np.exp(- self.r_mix_inflow / self.depth * self.timesteplength)
        self.sal_cell = self.sal_cell * ht + (self.vol_sink_cell + self.r_mix_inflow) / \
                        self.r_mix_inflow * self.sal_cell_inflow * (1 - ht)
        self.writeGridSalinity(t_end=self._t_end, tsl=self.timesteplength)

    def getPlantSalinity(self):
        """
        Calculate pore-water salinity below each plant (mean of affected cells).
        """
        salinity_plant = np.zeros(len(self.plant_cells))
        for pc in range(len(self.plant_cells)):
            affected_cells = self.plant_cells[pc]
            salinity_plant[pc] = np.mean(self.sal_cell[affected_cells])
        return salinity_plant

    def writeGridSalinity(self, t_end, tsl):
        """
        Write cell salinity to a text file if required.
        """
        if hasattr(self, "save_file"):
            if t_end == 0 or t_end % (self.save_salinity_ts * tsl) == 0:
                np.savetxt(self.save_file + "_" + str(t_end) + '.txt', self.sal_cell)

    def getAffectedCellsIdx(self, xp, yp, rrp):
        """
        Identify grid cells affected by a plant.
        """
        distance = np.sqrt((self.my_grid[0] - xp) ** 2 + (self.my_grid[1] - yp) ** 2)
        return np.where(distance < rrp)

    def getBorderValues(self):
        """
        Determine the boundary salinity and mixing rates.
        """
        if hasattr(self, "t_variable"):
            self.getSalinityTimeseries()
        elif hasattr(self, "amplitude"):
            if hasattr(self, "medium"):
                if "water" in self.medium.lower():
                    self.getMixingRateSine()
                if "salt" in self.medium.lower():
                    self.getSalinitySine()
            else:
                self.getSalinitySine()

    def readMixingRateTag(self):
        """
        Read and parse <r_mix> mixing rate.
        """
        if isinstance(self.r_mix, float):
            self.r_mix = [self.r_mix, self.r_mix]
        else:
            if len(self.r_mix.split()) == 2:
                try:
                    self.r_mix = self.r_mix.split()
                    self.r_mix[0] = float(eval(self.r_mix[0]))
                    self.r_mix[1] = float(eval(self.r_mix[1]))
                except NameError:
                    print("Error: Mix rate tag <r_mix> not properly defined.")
                    exit()
            else:
                print("Error: Mix rate tag <r_mix> not properly defined.")
                exit()
        self.left_bc_r_mix = self.r_mix[0]
        self.right_bc_r_mix = self.r_mix[1]

    def getInflowMixingRate(self):
        """
        Calculate the mixing rate for each cell.
        """
        if len(self.my_grid[0]) == 1:
            self.r_mix_inflow = np.array([0.5 * (self.r_mix[0] + self.r_mix[1])])
        else:
            x_dif = self.x_2 - self.x_1
            self.r_mix_inflow = (self.my_grid[0] - self.x_1) / x_dif * \
                                (self.r_mix[1] - self.r_mix[0]) + self.r_mix[0]

    def getMixingRateSine(self):
        """
        Apply a sine-based variation to mixing rate.
        """
        s0 = self.amplitude * np.sin(self._t_ini / self.stretch + self.offset)
        left = s0 + self.left_bc_r_mix
        self.r_mix[0] = np.random.normal(size=1, loc=left, scale=self.noise)
        self.r_mix[0] = self.r_mix[0] if self.r_mix[0] > 0 else 0
        right = s0 + self.right_bc_r_mix
        self.r_mix[1] = np.random.normal(size=1, loc=right, scale=self.noise)
        self.r_mix[1] = self.r_mix[1] if self.r_mix[1] > 0 else 0

    def getInputTags(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "salinity", "x_1", "x_2", "y_1", "y_2",
                         "x_resolution", "y_resolution", "r_mix"],
            "optional": ["sine", "amplitude", "stretch", "offset", "noise",
                         "medium", "save_salinity_ts", "save_file",
                         "depth", "initial_salinity_file"]
        }
        return tags

    def getInputParameters(self, args):
        tags = self.getInputTags(args)
        super(FixedSalinity, self).getInputParameters(**tags)
        self.setInputParameters()

    def setInputParameters(self):
        super().setDefaultParameters()
        if not hasattr(self, "depth"):
            print("> Set below-ground parameter 'depth' to default: 1")
            self.depth = 1
        if hasattr(self, "sine"):
            if not hasattr(self, "medium"):
                print("> Set below-ground parameter 'medium' to default: salt")
                self.medium = "salt"
        self.readMixingRateTag()
        if hasattr(self, "save_file"):
            if not hasattr(self, "save_salinity_ts"):
                self.save_salinity_ts = 1

      