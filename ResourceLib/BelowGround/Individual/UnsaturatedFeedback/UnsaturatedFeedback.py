import numpy as np
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity


class UnsaturatedFeedback(FixedSalinity):
    """
    UnsaturatedFeedback below-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        # ToDo: option to save cell salinity as in SaltFeedbackBucket
        # ToDo: Error messages if temporal or spatial limits are not met
        # ToDo: Test with different cell sizes
        self.getInputParameters(args)
        self._t_ini = 0

        # ToDo: make this user input
        self.porosity = 0.45
        self.field_capacity = 0.2
        self.h_lay = 0.1
        self.hygroscopic_water = 0.05
        self.salinity_tide = 35/1000

        self.setElevation()
        self.makeGridFromMap()
        self.setPrecipitation()
        self.setTidalLevel()
        self.setCellConductivity()

        self.iniCellSalinity()
        self.iniCellMoisture()

        self.meteo_counter = 0

    def prepareNextTimeStep(self, t_ini, t_end):
        self.t_end = t_end
        super().prepareNextTimeStep(t_ini, t_end)
        self.delta_t_vegetation = t_end - t_ini
        self.no_hydro_iter = int(self.delta_t_vegetation / self.delta_t_hydro)

        self.plant_cells = []
        self.cell_ETR = np.zeros(np.shape(self.my_grid[0]))
        self.cell_salinity_accum = 0

    def addPlant(self, plant):
        print(">> addPlant")
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

        # Plant water uptake per hydro time step
        plant_water_uptake = plant_water_uptake / self.no_hydro_iter

        # Extend root radius, if radius is smaller than mesh size
        if rrp < self.mesh_size:
            rrp = self.mesh_size

        # Calculate sink term (i.e. plant water uptake per cell)
        self.calculatePlantSink(xp, yp, rrp, plant_water_uptake)

    def calculateBelowgroundResources(self):
        self.calculateHydro()
        salinity_plant = self.getPlantSalinity()
        self.calculatePlantResources(salinity_plant)

        # if self.t_end == 0 or self.t_end % (self.save_salinity_ts * self.delta_t_vegetation) == 0:
        if self.t_end == 0 or self.t_end % (24 * self.delta_t_vegetation) == 0:
            np.savetxt("cell_salinity_lay_0" + "_" + str(self.t_end) + '.txt', self.cell_salinity[0])
            np.savetxt("cell_salinity_lay_1" + "_" + str(self.t_end) + '.txt', self.cell_salinity[1])
            np.savetxt("cell_salinity_lay_2" + "_" + str(self.t_end) + '.txt', self.cell_salinity[2])

    def calculateHydro(self):
        for t in range(self.no_hydro_iter):
            print("--------------- HYDRO LOOP", t)
            # Infiltration at the surface
            inf_rate, c_inf = self.infiltration()

            # Seepage at the first layer
            seep_out = self.seepage(nth_layer=0, inf_rate=inf_rate, c_inf=c_inf)

            # Seepage at other layers
            if self.n_layers > 1:
                for i in range(1, int(self.n_layers)):
                    self.seepage(nth_layer=i,
                                 inf_rate=seep_out / self.delta_t_hydro,
                                 c_inf=self.cell_salinity[i - 1])
            self.updateSalinity()

            # Increase meteo data index
            self.meteo_counter += 1
            if self.meteo_counter > self.meteo_max - 1:
                if self.repeat_meteo:
                    self.meteo_counter = 0
                else:
                    print("WARNING: Running time of the model exceed provided meteorological data."
                          "\npyMANGA execution stopped.")
                    exit()

    def setElevation(self):
        print(">> setElevation")
        # size x*y cells
        self.cell_elevation = np.loadtxt(self.elevation_map).transpose()
        print(np.shape(self.cell_elevation))

    def makeGridFromMap(self):
        x_res = np.shape(self.cell_elevation)[0]
        y_res = np.shape(self.cell_elevation)[1]
        print("x_res", x_res, "y_res", y_res)
        self.cell_size = [float(i) for i in self.cell_size.split()]
        self.mesh_size = np.max(self.cell_size)
        print("cell_size", self.cell_size)

        xe = np.linspace(self.cell_size[0] / 2.,
                         self.cell_size[0] * (x_res - 1 / 2),
                         int(x_res),
                         endpoint=True)
        ye = np.linspace(self.cell_size[1] / 2.,
                         self.cell_size[1] * (y_res - 1 / 2),
                         int(y_res),
                         endpoint=True)
        self.my_grid = np.meshgrid(ye, xe)
        self.cell_area = self.cell_size[0] * self.cell_size[1]
        print("cell_area", self.cell_area)
        print("shape my_grid", np.shape(self.my_grid))

    def setPrecipitation(self):
        print(">> setPrecipitation")
        # shape (2, no. time steps)
        # [0]: time step in seconds
        # [1]: precipitation rate
        self.precipitation_rate = np.loadtxt(self.precipitation_rate).transpose()

    def setTidalLevel(self):
        print(">> setTidalLevel")
        # shape (2, no. time steps)
        # [0]: time step in seconds
        # [1]: tidal level
        self.tidal_level = np.loadtxt(self.tidal_level).transpose()
        self.meteo_max = len(self.tidal_level[0])
        print(np.shape(self.tidal_level))

    def setCellConductivity(self):
        # ToDo: read from map?
        self.cell_hydr_conductivity = np.full(shape=np.shape(self.cell_elevation),
                                              fill_value=2e-05)

    def iniCellMoisture(self):
        # ToDo: update based on water uptake
        # ToDo: What are the initial conditions?
        s = np.shape(self.cell_elevation)
        self.cell_moisture = np.array([np.full(shape=s, fill_value=0.2),
                                       np.full(shape=s, fill_value=0.2),
                                       np.full(shape=s, fill_value=0.2)])

    def iniCellSalinity(self):
        s = np.shape(self.cell_elevation)
        self.cell_salinity = np.array([np.full(shape=s, fill_value=35 / 10 ** 3),
                                       np.full(shape=s, fill_value=35 / 10 ** 3),
                                       np.full(shape=s, fill_value=35 / 10 ** 3)])
        print(">> cell_salinity", np.shape(self.cell_salinity))

    def updateSalinity(self):
        print(">> updateSalinity - evap_saltfred")
        n_lay = np.shape(self.cell_salinity)[0]
        sal_before = self.cell_salinity
        # Salinity in each cell and layer
        sal = self.cell_salinity * self.cell_moisture
        # ETR in each cell and layer in m³ per time step
        # Assuming homogeneous uptake in each layer
        h = np.array(self.cell_ETR / n_lay)
        ETR_lay = np.repeat(h[np.newaxis, :, :], n_lay, axis=0)

        h2o = np.maximum(((1 - self.cell_salinity) * self.cell_moisture - ETR_lay / self.h_lay / self.porosity), (1 - self.cell_salinity) * self.hygroscopic_water)
        self.cell_moisture = h2o + sal
        self.cell_salinity = sal / self.cell_moisture
        self.cell_salinity_accum += self.cell_salinity

    def infiltration(self):
        print(">> infiltration")
        tide_level = self.tidal_level[1][self.meteo_counter]
        prep_rate = self.precipitation_rate[1][self.meteo_counter]

        PI = np.empty(shape=np.shape(self.cell_elevation))
        c_inf = np.empty(shape=np.shape(self.cell_elevation))
        hinx = tide_level - self.cell_elevation > 0
        PI[np.where(hinx)] = self.cell_hydr_conductivity[np.where(hinx)]
        c_inf[np.where(hinx)] = self.salinity_tide
        # precipitation (m/s)
        PI[np.where(hinx == False)] = prep_rate / 3.6e+6
        c_inf[np.where(hinx == False)] = 0
        # infiltration rate (m/s)
        inf_rate = np.asarray([PI, self.cell_hydr_conductivity]).min(0)
        return [inf_rate, c_inf]

    def seepage(self, nth_layer, inf_rate, c_inf):
        print(">> seepage, layer", nth_layer)
        theta = self.cell_moisture[nth_layer]
        print("\tinf_rate", np.shape(inf_rate), "c_inf", np.shape(c_inf))
        # moisture above field capacity (-)
        theta_F = theta - self.field_capacity
        # split time to below/above field cap.
        dt_ = np.full(fill_value=self.delta_t_hydro, shape=np.shape(theta))
        hinx = theta_F < 0
        if sum(inf_rate[hinx]) != 0:
            dt_[hinx] = dt_[hinx] + (theta_F[hinx] * self.h_lay / inf_rate[hinx])
        if len(dt_[hinx]) == 0:
            dt_[hinx] = max(dt_[hinx], 0)
            theta_F[hinx] = 0
        # decay rate [s]
        K = self.h_lay * (self.porosity - self.field_capacity) / self.cell_hydr_conductivity
        # seepage, from soil moisture [m]
        seep0 = self.h_lay * theta_F * (1 - np.exp(-dt_ / K))
        # seepage, from infiltrated water [m]
        seep1 = inf_rate * (K * np.exp(-dt_ / K) + dt_ - K)
        # seepage, total [m]
        seep = seep0 + seep1
        # soil moisture increase (-)
        theta_plus = inf_rate * self.delta_t_hydro / self.h_lay
        # soil moisture loss (-)
        theta_minus = seep / self.h_lay
        c_lay = (theta * self.cell_salinity[nth_layer] + theta_plus * c_inf) / (theta + theta_plus)
        theta += theta_plus - theta_minus

        # ToDo: Does this make sense?
        theta[theta < 0] = 0
        c_lay[c_lay < 0] = 0

        self.cell_moisture[nth_layer] = theta
        self.cell_salinity[nth_layer] = c_lay
        return seep

    def calculatePlantSink(self, x, y, r_root, bg_resources):
        print(">> calculatePlantSink")
        # Assign plant water uptake to cells
        idx = self.getAffectedCellsIdx(x, y, r_root)
        self.plant_cells.append(idx)
        if bg_resources != 0:
            no_cells = len(idx[0])
            # Calculate transpiration based on area of occupied cells in m³ per m² per time step
            sink_per_cell = bg_resources / (self.cell_area * no_cells)
            self.cell_ETR[idx] += sink_per_cell

    def getPlantSalinity(self):
        """
        Calculate pore-water salinity below each tree, taking the mean value of all affected cells.
        Returns:
            numpy array with shape(number_of_trees)
        """
        print(">> getPlantSalinity")
        # Average cell salinity during vegetation time step
        avg_cell_salinity = self.cell_salinity_accum / self.no_hydro_iter
        # Interpolation of salinity over space
        salinity_plant = np.zeros(len(self.plant_cells))
        for pc in range(len(self.plant_cells)):
            affected_cells = self.plant_cells[pc]
            salinity_plant[pc] = np.mean([avg_cell_salinity[i][affected_cells] for i in range(len(avg_cell_salinity))])
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
        print(">> getAffectedCellsIdx")
        # ToDo: careful: x-y vertauscht im Vergleich zum SaltFeedbackBucket
        distance = (((self.my_grid[1] - np.array(xp)) ** 2 +
                     (self.my_grid[0] - np.array(yp)) ** 2) ** 0.5)
        idx = np.where(distance < rrp)
        return idx

    def getInputTags(self, args):
        tags = {
            "prj_file": args,
            "required": ["type",
                         "elevation_map",
                         "cell_size", "n_layers",
                         "precipitation_rate",
                         "tidal_level",
                         "delta_t_hydro"],
            "optional": ["repeat_meteo"]
        }
        return tags

    def getInputParameters(self, args):
        tags = self.getInputTags(args)
        super(FixedSalinity, self).getInputParameters(**tags)

        self.delta_t_hydro = int(self.delta_t_hydro)
        if not hasattr(self, "repeat_meteo"):
            self.repeat_meteo = True
            print(">> <Belowground><UnsaturatedFeedback><repeat_meteo> set to default value:", self.repeat_meteo)
