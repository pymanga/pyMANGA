import numpy as np
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity


class SaltFeedbackBucket(FixedSalinity):
    def __init__(self, args):
        try:
            self.getInputParameters(args)
            self.cell_height = 1
        except KeyError:
            self.setDebugParameters()

        super().makeGrid()
        self.getCellVolume()

        self.getInflowSalinity()
        self.getInflowMixingRate()
        self.sal_cell = self.sal_cell_inflow
        self.writeGridSalinity(t_end=0, tsl=0)

    def setDebugParameters(self):
        print("\t>>>>>>>>>>>>> Debug mode")
        self.x_2 = 2
        self.y_2 = 2
        self.x_resolution = 1
        self.y_resolution = 1

        self.cell_height = 1
        self.f_mix = 0.5  # 10 %
        self.q_cell = 0.3  # m³/d
        self._salinity = [35 / 1000, 35 / 1000]

        self._psi_leaf = -7.86 * 10 ** 6
        self._r_crown = 3
        self._h_stem = 3

        self._r_salinity = "bettina"

    def getInflowSalinity(self):
        if len(self.my_grid[0]) == 1:
            # If only 1 cell exist take mean of border salinity
            self.sal_cell_inflow = np.array([0.5 * (self._salinity[0] + self._salinity[1])])
        else:
            x_dif = self.x_2 - self.x_1
            self.sal_cell_inflow = (self.my_grid[0] - self.x_1) / x_dif * (self._salinity[1] - self._salinity[0]) + self._salinity[0]

    def prepareNextTimeStep(self, t_ini, t_end):
        super().prepareNextTimeStep(t_ini, t_end)
        self.timesteplength = t_end - t_ini
        # ToDo: Ist vol_cell eher relatives Volumen ohne Einheit: - * m³/d * tsl/s*d
        self.vol_water_cell = self.vol_cell * self.q_cell * self.timesteplength / 3600 / 24
        self.vol_sink_cell = np.zeros(np.shape(self.my_grid[0]))
        self.plant_cells = []
        self.no_plants = 0

    def addPlant(self, plant):
        self.no_plants += 1
        try:
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

        except AttributeError:
            print("\t>>>>>>>>>>>>> Debug mode")
            xp, yp = 0.5, .5
            rrp = 1
            # Example uptake 10 L per day
            plant_water_uptake = 10 / 10**3      # m³ water per time step

        if rrp < self._mesh_size:
            #print("\t> Interpolate root radius")
            rrp = self._mesh_size

        idx = self.getAffectedCellsIdx(xp, yp, rrp)
        self.plant_cells.append(idx)
        if plant_water_uptake != 0:
            no_cells = len(idx[0])
            sink_per_cell = plant_water_uptake / no_cells
            self.vol_sink_cell[idx] += sink_per_cell

    def calculateBelowgroundResources(self):
        self.readGridSalinity()
        self.getBorderSalinity()
        self.getInflowSalinity()

        self.calculateCellSalinity()

        salinity_plant = self.getPlantSalinity()
        self.calculatePlantResources(salinity_plant)

    def calculateCellSalinity(self):
        # Load in kg = kg/kg * m**3 * 10**3kg/m**3 = kg
        # Calculate salinity load in each cell
        # cell salinity * V_cell
        m_cell = self.sal_cell * self.vol_water_cell #* 10**3

        # Calculate cell volume after plant water uptake
        # m³ = m³ - m³
        vol_cell_remain = self.vol_water_cell - self.vol_sink_cell

        # Calculate salinity in cell
        # kg/kg = kg / m³ / 10**3kg/m**3 =  kg/kg
        sal_cell_new = m_cell / vol_cell_remain #/ 10**3

        # Mixing
        vol_out = self.f_mix_inflow * self.vol_water_cell
        m_out = self.sal_cell_inflow * vol_out #* 10**3
        v_remain = self.vol_water_cell - vol_out
        m_remain = sal_cell_new * v_remain #* 10**3

        m_cell = m_remain + m_out

        self.sal_cell = m_cell / self.vol_water_cell #/ 10**3

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

    def readGridSalinity(self):
        self.sal_cell = np.loadtxt('grid_salinity.txt', usecols=range(len(self.my_grid[0][0])))

    def writeGridSalinity(self, t_end, tsl):
        np.savetxt('grid_salinity.txt', self.sal_cell)

        if hasattr(self, "save_salinity_ts"):
            if t_end == 0 or t_end % (self.save_salinity_ts * tsl) == 0:
                print(">>>>>>>>>>>>>>>>>>")
                np.savetxt('grid_salinity_' + str(t_end) + '.txt', self.sal_cell)

    def getAffectedCellsIdx(self, xp, yp, rrp):
        distance = (((self.my_grid[0] - np.array(xp)) ** 2 +
                     (self.my_grid[1] - np.array(yp)) ** 2) ** 0.5)
        idx = np.where(distance < rrp)
        return idx

    def getCellVolume(self):
        self.vol_cell = (self.x_2 / self.x_resolution) * self.y_2 / self.y_resolution * self.cell_height
        print("> Domain volume:", self.x_2*self.y_2, "m**3, cell volume", self.vol_cell, "m**3")

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "salinity", "x_1", "x_2", "y_1", "y_2",
                         "x_resolution", "y_resolution", "q_cell", "f_mix"],
            "optional": ["sine", "amplitude", "stretch", "offset", "noise",
                         "medium", "save_salinity_ts"]
        }
        super(FixedSalinity, self).getInputParameters(**tags)
        super().setDefaultParameters()

        self.readMixingRateTag()

    def getBorderSalinity(self):
        self._xe = np.array(self._xe)
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

    def getMixingRateSine(self):
        """
        Calculate salinity of the current time step using a sine function.
        Set salinity at the current time step at the left and right model boundary.
        """
        s0 = self.amplitude * np.sin(self._t_ini / self.stretch + self.offset)
        left = s0 + self.left_bc
        self.f_mix[0] = np.random.normal(size=1, loc=left, scale=self.deviation)
        self.f_mix[0] = self.f_mix[0] if self.f_mix[0] > 0 else 0

        right = s0 + self.right_bc
        self.f_mix[1] = np.random.normal(size=1, loc=right, scale=self.deviation)
        self.f_mix[1] = self.f_mix[1] if self.f_mix[1] > 0 else 0


    def readMixingRateTag(self):
        if isinstance(self.f_mix, float):
            self.f_mix = [self.f_mix, self.f_mix]

        else:
            if len(self.f_mix.split()) == 2:
                self.f_mix = self.f_mix.split()
                self.f_mix[0] = float(eval(self.f_mix[0]))
                self.f_mix[1] = float(eval(self.f_mix[1]))

    def getInflowMixingRate(self):
        if len(self.my_grid[0]) == 1:
            self.f_mix_inflow = np.array([0.5 * (self.f_mix[0] + self.f_mix[1])])
        else:
            x_dif = self.x_2 - self.x_1
            self.f_mix_inflow = (self.my_grid[0] - self.x_1) / x_dif * (self.f_mix[1] - self.f_mix[0]) + self.f_mix[0]


if __name__ == '__main__':
    # Build xml tree snippet
    from lxml import etree

    root = etree.Element("belowground")
    etree.SubElement(root, "type").text = "SaltFeedbackBucket"

    resource = SaltFeedbackBucket(args=root)
    resource.prepareNextTimeStep(t_ini=0, t_end=3600 * 24 * 100)
    resource.addPlant(plant={})
    resource.calculateBelowgroundResources()


