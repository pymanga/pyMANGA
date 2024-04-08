import numpy as np
from ResourceLib import ResourceModel
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity
from ResourceLib.BelowGround.Individual.OGS import OGS
from ResourceLib.BelowGround.Individual.SymmetricZOI import SymmetricZOI


class SaltFeedbackBucket(FixedSalinity):
    def __init__(self, args):
        self.lx = 22
        self.ly = 22
        self.x_res = self.lx*3
        self.y_res = self.ly*3
        self.cell_height = 0.1
        self.f_mix_min = 0.01    # 10 %
        self.q_cell = 10/10**3       # m³/d
        self.salinity = [10/1000, 20/1000]

        self.expandGrid()

        self.getInflowSalinity()
        self.salinity_cell = self.salinity_inflow
        # my_grid: x, y
        self.writeGridSalinity(t=0)

    def getInflowSalinity(self):
        x_min = min(self.my_grid[0])
        x_dif = max(self.my_grid[0]) - x_min
        self.salinity_inflow = (self.my_grid[0] - x_min) / x_dif * (self.salinity[1] - self.salinity[0]) + self.salinity[0]

    def prepareNextTimeStep(self, t_ini, t_end):
        print("\tprepareNextTimeStep")
        super().prepareNextTimeStep(t_ini, t_end)
        self.timesteplength = t_end - t_ini
        self.cell_volume = self.q_cell * self.timesteplength
        self.plant_sink = np.zeros(np.shape(self.my_grid)[1])
        self.plant_cells = []
        self.no_plants = 0

    def addPlant(self, plant):
        print("\taddPlant")
        self.no_plants += 1
        try:
            xp, yp = plant.getPosition()
            geometry = plant.getGeometry()
            parameter = plant.getParameter()
            gci = plant.getGrowthConceptInformation()
            rrp = geometry["r_root"]
            self._h_stem.append(geometry["h_stem"])
            self._r_crown.append(geometry["r_crown"])
            self._psi_leaf.append(parameter["leaf_water_potential"])

            self._xe.append(xp)

            try:
                sinkp = gci["bg_resources"]  # m³ water per time step
            except KeyError:
                sinkp = 0

        except AttributeError:
            print("\t>>>>>>>>>>>>> Debug mode")
            xp, yp = 10, 5
            rrp = 3
            self._psi_leaf = -7.86*10**6
            self._r_crown = 3
            self._h_stem = 3

            # Example uptake 10 L per day
            sinkp = 10 / 10**3  # m³ water per time step

        if rrp < self.mesh_size:
            print("\t> Interpolate root radius")
            rrp = self.mesh_size

        idx = self.getAffectedCellsIdx(xp, yp, rrp)
        self.plant_cells.append(idx)

        if sinkp != 0:
            no_cells = len(idx)
            sink_per_cell = sinkp / no_cells * self.timesteplength
            #print("----------------------------------------",self.no_plants, sink_per_cell, no_cells, sinkp)

            self.plant_sink[idx] += sink_per_cell

    def calculateBelowgroundResources(self):
        print("\tcalculateBelowgroundResources")
        self.getBorderSalinity()
        self.readGridSalinity()
        print("\t\t salinity border", self.salinity)
        # Load in kg = kg/kg * m**3 * 10**3kg/m**3 = kg
        # Calculate salinity load in each cell
        # cell salinity * V_cell
        m_cell = self.salinity_cell * self.cell_volume * 10**3
        #print("\t\t m_cell", m_cell)

        # Calculate cell volume after plant water uptake
        # m³ = m³ - m³
        vol_cell = self.cell_volume - self.plant_sink
        #print("\t\t vol_cell after uptake", vol_cell)

        # Calculate salinity in cell
        # kg/kg = kg / m³ / 10**3kg/m**3 =  kg/kg
        sal_cell = m_cell / vol_cell / 10**3
        #print("\t\t sal_cell", sal_cell)
        print(max(self.salinity_cell), max(sal_cell), "--------------")
        # Mix cell with inflow water
        # Calculate volume outflow
        #idx = np.where(self.plant_sink > self.f_mix_min * self.cell_volume)
        #print(self.plant_sink, self.f_mix_min * self.cell_volume)
        vol_mix = np.full(len(m_cell), self.f_mix_min * self.cell_volume)
        # for i in idx:
        #     vol_mix[i] = self.plant_sink[i]

        # Calculate load of outflowing water
        m_out = vol_mix * sal_cell
        #print("\t\t m_out", m_out)

        # Calculate load of inflowing water
        self.getInflowSalinity()
        m_in = vol_mix * self.salinity_inflow
        #print("\t\t m_in", m_in)
        print(max(m_in), max(m_out))
        # Calculate load of mixed water
        m_cell += m_in - m_out
        #print("\t\t m_cell", m_cell)

        # Calculate new cell salinity
        # kg / m**3 / 10**3 kg/m3 = kg/kg
        salinity = m_cell / self.cell_volume / 10**3
        #print("\t\t salinity diff", salinity - self.salinity_cell)
        self.salinity_cell = salinity

        self.writeGridSalinity(t=self._t_end)

        # Plant stuff
        salinity_plant = self.getPlantSalinity()
        psi_zero = np.array(self._psi_leaf) + (2 * np.array(self._r_crown) +
                                                      np.array(self._h_stem)) * 9810
        psi_sali = np.array(psi_zero) + 85000000 * salinity_plant
        if np.isnan(psi_sali).all():
            exit()
        self.belowground_resources = psi_sali / psi_zero

    def getBorderSalinity(self):
        self._xe = np.array(self._xe)
        if hasattr(self, "t_variable"):
            self.getSalinityTimeseries()
        elif hasattr(self, "amplitude"):
            self.getSalinitySine()

        self._salinity = self.salinity

    def getPlantSalinity(self):
        """
        Calculate pore-water salinity below each tree, interpolating over space and time.
        Returns:
            numpy array with shape(number_of_trees)
        """

        # Interpolation of salinity over space
        salinity_plant = np.zeros(len(self.plant_cells))
        for pc in range(len(self.plant_cells)):
            affected_cells = self.plant_cells[pc]
            salinity_plant[pc] = np.mean(self.salinity_cell[affected_cells])
        print(salinity_plant)
        return salinity_plant

    def readGridSalinity(self):
        print("\treadGridSalinity")
        self.salinity_cell = np.loadtxt('grid_salinity.txt', usecols=[3])
        print("\t\t", np.mean(self.salinity_cell))

    def writeGridSalinity(self, t):
        t = np.full(len(self.salinity_cell), t)
        np.savetxt('grid_salinity.txt', np.c_[t, self.my_grid[0], self.my_grid[1], self.salinity_cell])

        with open("myfile.txt", "ab") as f:
            #f.write(b"\n")
            np.savetxt(f, np.c_[t, self.my_grid[0], self.my_grid[1], self.salinity_cell])

    def getAffectedCellsIdx(self, xp, yp, rrp):
        print("\tgetAffectedCells")
        xmin = xp - rrp
        xmax = xp + rrp
        ymin = yp - rrp
        ymax = yp + rrp
        #print("\t\t", xmin, xmax, ymin, ymax)

        x1 = np.where(self.my_grid[0] >= xmin)
        x2 = np.where(self.my_grid[0] <= xmax)
        idxx = np.intersect1d(x1, x2)

        y1 = np.where(self.my_grid[1] >= ymin)
        y2 = np.where(self.my_grid[1] <= ymax)
        idxy = np.intersect1d(y1, y2)
        idx = np.intersect1d(idxx, idxy)

        print("\t\t", "Affected cells", len(idx))
        return idx

    def expandGrid(self):
        print("\texpandGrid")

        xs = self.lx / self.x_res
        xe = np.arange(0, self.lx + xs, xs)

        ys = self.ly / self.y_res
        ye = np.arange(0, self.ly + ys, ys)

        self.my_grid = [(x, y) for x in xe for y in ye]
        self.my_grid = np.array(self.my_grid).transpose()
        # n = np.zeros(np.shape(self.my_grid)[1])
        # self.my_grid = np.vstack((self.my_grid, n))
        self.mesh_size = min(xs, ys)
        print("\t\tmesh size", self.mesh_size)
        #self.getCellVolume(xs, ys)

    def getCellVolume(self, xs, ys):
        self.cell_volume = xs * ys * self.cell_height
        print("\t\t", "Cell volume:", self.cell_volume, "m**3 (", self.cell_volume*10**3, "L).")


if __name__ == '__main__':
    # Build xml tree snippet
    from lxml import etree

    root = etree.Element("belowground")
    etree.SubElement(root, "type").text = "SaltFeedbackBucket"

    resource = SaltFeedbackBucket(args=root)
    resource.prepareNextTimeStep(t_ini=0, t_end=3600 * 24)
    resource.addPlant(plant={})
    resource.calculateBelowgroundResources()


