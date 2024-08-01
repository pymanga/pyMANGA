import numpy as np
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity


class SaltFeedbackBucket(FixedSalinity):
    """
    SaltFeedbackBucket below-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        self.getInputParameters(args)
        super().makeGrid()
        self.getInflowSalinity()
        self.getInflowMixingRate()
        self.sal_cell = self.sal_cell_inflow

    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini, t_end)
        self.timesteplength = t_end - t_ini
        self.vol_sink_cell = np.zeros(np.shape(self.my_grid[0]))
        self.plant_cells = []

    def addPlant(self, plant):
        xp, yp = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        gci = plant.getGrowthConceptInformation()
        rrp = geometry["r_root"]
        self._r_salinity.append(parameter["r_salinity"])
        self._h_stem.append(geometry["h_stem"])
        self._r_crown.append(geometry["r_crown"])
        self._psi_leaf.append(parameter["leaf_water_potential"])
        self._xe.append(xp)

        # If below-ground resources does not yet exist for the plant, set
        # sink term to 0
        try:
            plant_water_uptake = gci["bg_resources"]  # m³ water per time step
        except KeyError:
            plant_water_uptake = 0

        # Extrapolate root radius, if radius is smaller than mesh size
        if rrp < self._mesh_size:
            rrp = self._mesh_size

        # Assign plant water uptake to cells
        idx = self.getAffectedCellsIdx(xp, yp, rrp)
        self.plant_cells.append(idx)
        if plant_water_uptake != 0:
            no_cells = len(idx[0])
            # Calculate transpiration based on area of occupied cells in m³ per m² per time step = m/s
            sink_per_cell = plant_water_uptake / (self.cell_area * no_cells) / self.timesteplength
            self.vol_sink_cell[idx] += sink_per_cell

    def calculateBelowgroundResources(self):
        self.getBorderValues()
        self.getInflowSalinity()
        self.getInflowMixingRate()

        self.calculateCellSalinity()

        salinity_plant = self.getPlantSalinity()
        self.calculatePlantResources(salinity_plant)

    def getInflowSalinity(self):
        """
        Calculate salinity of inflowing water of each cell, such as tidal water.
        Salinity is linearly interpolated between the left and right model boundaries.
        """
        if len(self.my_grid[0]) == 1:
            # If only 1 cell exist take mean of border salinity
            self.sal_cell_inflow = np.array([0.5 * (self._salinity[0] + self._salinity[1])])
        else:
            x_dif = self.x_2 - self.x_1
            self.sal_cell_inflow = (self.my_grid[0] - self.x_1) / x_dif * (self._salinity[1] - self._salinity[0]) + self._salinity[0]

    def calculateCellSalinity(self):
        """
        Calculate salinity in each cell considering
        - extraction of fresh water by plants
        - mixing with inflowing water.
        Additionally, write cell salinity to text file.
        """
        ht = np.exp(- self.r_mix_inflow / self.depth * self.timesteplength)
        self.sal_cell = self.sal_cell * ht + (self.vol_sink_cell + self.r_mix_inflow) / \
                        self.r_mix_inflow * self.sal_cell_inflow * (1 - ht)

        self.writeGridSalinity(t_end=self._t_end, tsl=self.timesteplength)

    def getPlantSalinity(self):
        """
        Calculate pore-water salinity below each tree, taking the mean value of all affected cells.
        Returns:
            numpy array with shape(number_of_trees)
        """
        # Interpolation of salinity over space
        salinity_plant = np.zeros(len(self.plant_cells))
        for pc in range(len(self.plant_cells)):
            affected_cells = self.plant_cells[pc]
            salinity_plant[pc] = np.mean(self.sal_cell[affected_cells])
        return salinity_plant

    def writeGridSalinity(self, t_end, tsl):
        """
        Write salinity of current timestep to text file.
        If enabled write additional file including timestep.
        """
        if hasattr(self, "save_file"):
            if t_end == 0 or t_end % (self.save_salinity_ts * tsl) == 0:
                np.savetxt(self.save_file + "_" + str(t_end) + '.txt', self.sal_cell)

    def getAffectedCellsIdx(self, xp, yp, rrp):
        """
        Identify cells affected by a specific plant.
        Args:
            xp (float): x-coordinate of the plant
            yp (float): y-coordinate of the plant
            rrp (float): root radius of the plant
        Returns:
            array
        """
        distance = (((self.my_grid[0] - np.array(xp)) ** 2 +
                     (self.my_grid[1] - np.array(yp)) ** 2) ** 0.5)
        idx = np.where(distance < rrp)
        return idx

    def getBorderValues(self):
        """
        Determine the salinity and/or mixing rate at the left and right boundaries of the model.
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
        Read the mixing rate tag <r_mix> from the project file and assign the values at the left and right
        model boundary.
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
        Calculate the mixing rate of each cell.
        The rate is linearly interpolated between the left and right model boundaries.
        """
        if len(self.my_grid[0]) == 1:
            self.r_mix_inflow = np.array([0.5 * (self.r_mix[0] + self.r_mix[1])])
        else:
            x_dif = self.x_2 - self.x_1
            self.r_mix_inflow = (self.my_grid[0] - self.x_1) / x_dif * (self.r_mix[1] - self.r_mix[0]) + self.r_mix[0]

    def getMixingRateSine(self):
        """
        Calculate mixing rate of the current time step using a sine function and assign the values at the left and right
        model boundary.
        """
        s0 = self.amplitude * np.sin(self._t_ini / self.stretch + self.offset)
        left = s0 + self.left_bc_r_mix
        self.r_mix[0] = np.random.normal(size=1, loc=left, scale=self.deviation)
        self.r_mix[0] = self.r_mix[0] if self.r_mix[0] > 0 else 0

        right = s0 + self.right_bc_r_mix
        self.r_mix[1] = np.random.normal(size=1, loc=right, scale=self.deviation)
        self.r_mix[1] = self.r_mix[1] if self.r_mix[1] > 0 else 0

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "salinity", "x_1", "x_2", "y_1", "y_2",
                         "x_resolution", "y_resolution", "r_mix"],
            "optional": ["sine", "amplitude", "stretch", "offset", "noise",
                         "medium", "save_salinity_ts", "save_file",
                         "depth"]
        }
        super(FixedSalinity, self).getInputParameters(**tags)
        super().setDefaultParameters()
        if not hasattr(self, "depth"):
            print("> Set below-ground parameter 'depth' to default: 1")
            self.depth = 1
        self.readMixingRateTag()

        if hasattr(self, "save_file"):
            if not hasattr(self, "save_salinity_ts"):
                self.save_salinity_ts = 1
