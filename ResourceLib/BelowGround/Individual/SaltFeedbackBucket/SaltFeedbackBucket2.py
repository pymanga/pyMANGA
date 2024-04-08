import numpy as np
from ResourceLib import ResourceModel
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity
from ResourceLib.BelowGround.Individual.OGS import OGS
from ResourceLib.BelowGround.Individual.SymmetricZOI import SymmetricZOI


class SaltFeedbackBucket(ResourceModel):
    def __init__(self, args):

        self.getInputParameters(args=args)
        super().makeGrid()
        # Assign initial salinity
        self.assignInitialSalinity()

    def assignInitialSalinity(self):
        if hasattr(self, "t_variable"):
            FixedSalinity.getSalinityTimeseries(self=self)
        elif hasattr(self, "amplitude"):
            FixedSalinity.getSalinitySine(self=self)

        lx = self._max_x - self._min_x
        s1 = self._salinity[0]
        s2 = self._salinity[1]
        cell_salinity = (self.my_grid[0] / lx * (s2-s1)) + s1
        self.my_grid.append(cell_salinity)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution", "min_x", "max_x", "salinity"],
            "optional": ["allow_interpolation", "sine", "amplitude", "stretch", "offset", "deviation"]
        }
        super().getInputParameters(**tags)

        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)

        self.allow_interpolation = super().makeBoolFromArg("allow_interpolation")
        self._salinity = self.salinity
        self._min_x = self.min_x
        self._max_x = self.max_x
        FixedSalinity.readSalinityTag(self=self)

        if hasattr(self, "sine"):
            if not hasattr(self, "amplitude"):
                print("> Set sine parameter 'amplitude' to default: 0")
                self.amplitude = 0
            if not hasattr(self, "stretch"):
                print("> Set sine parameter 'stretch' to default: 58*3600*24")
                self.stretch = 58*3600*24
            if not hasattr(self, "deviation"):
                print("> Set sine parameter 'deviation' to deviation: 0")
                self.deviation = 0
            if not hasattr(self, "offset"):
                print("> Set sine parameter 'offset' to offset: 0")
                self.offset = 0

        dx = abs(self.x_2 - self.x_1) / self.x_resolution
        dy = abs(self.y_2 - self.y_1) / self.y_resolution
        dh = 25     # ToDo: optional input
        self.cell_volume = dx * dy *dh

    def prepareNextTimeStep(self, t_ini, t_end):
        FixedSalinity.prepareNextTimeStep(self, t_ini, t_end)
        self._plant_constant_contribution = []
        self.xe = []
        self.ye = []
        self.r_root = []

    def addPlant(self, plant):
        print(plant)
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()

        self.xe.append(x)
        self.ye.append(y)
        self.r_root.append(geometry["r_root"])

        constant_contribution = self.getPlantWaterUseNoSalinity(parameter=parameter, geometry=geometry)
        self._plant_constant_contribution.append(constant_contribution)

        if "forman" in parameter["r_salinity"]:
            print("ERROR: below-ground module 'SaltFeedbackBucket' can't be used with 'Forman' salinity response"
                  " function (e.g. used in plant module 'Kiwi').")
            exit()

    def getPlantWaterUseNoSalinity(self, parameter, geometry):
        # root_surface_resistance
        lp = parameter["lp"]
        k_geom = parameter["k_geom"]
        r_root = geometry["r_root"]
        h_root = geometry["h_root"]
        root_surface_resistance = (1 / lp / k_geom / np.pi / r_root**2 /
                                   h_root)
        # xylem_resistance
        r_crown = geometry["r_crown"]
        h_stem = geometry["h_stem"]
        r_root = geometry["r_root"]
        kf_sap = parameter["kf_sap"]
        r_stem = geometry["r_stem"]
        flow_length = (2 * r_crown + h_stem + 0.5**0.5 * r_root)
        xylem_resistance = (flow_length / kf_sap / np.pi / r_stem**2)

        total_resistance = root_surface_resistance + xylem_resistance

        delta_psi = parameter["leaf_water_potential"] + \
                    (2 * geometry["r_crown"] + geometry["h_stem"]) * 9810
        constant_contribution = -delta_psi / total_resistance * 1000 / np.pi
        return constant_contribution

    def calculateBelowgroundResources(self):
        tree_water_use_no_salinity = self._plant_constant_contribution
        print(tree_water_use_no_salinity)

        # Numpy array of shape [res_x, res_y, n_plants]
        distance = (((self.my_grid[0][:, :, np.newaxis] -
                      np.array(self.xe)[np.newaxis, np.newaxis, :])**2 +
                     (self.my_grid[1][:, :, np.newaxis] -
                      np.array(self.ye)[np.newaxis, np.newaxis, :])**2)**0.5)
        min_distance = np.min(distance)

        # Array of shape distance [res_x, res_y, n_plants], indicating which
        # cells are occupied by plant root plates
        root_radius = np.array(self.r_root)
        # If root radius < mesh size, set it to mesh size
        root_radius[np.where(root_radius < min_distance)] = min_distance
        plants_present = root_radius[np.newaxis, np.newaxis, :] >= distance
        for i in range(len(self.xe)):

            distance = (((self.my_grid[0] - np.array(self.xe)[i])**2 +
                         (self.my_grid[1] - np.array(self.ye)[i])**2)**0.5)
            print()
            ac = distance[distance <= rr]
            print(ac)
            indices = np.where(np.less(rr, distance))
            print(indices)

        #self.my_grid[3][plants_present[2]]


        exit()
        salinity_plant = self.getPlantSalinity() # Berechnung anhang my_grid
        tree_water_use = self.getTreeWaterUse()
        psi_zero = np.array(self._psi_leaf) + (2 * np.array(self._r_crown) +
                                                   np.array(self._h_stem)) * 9810
        psi_sali = np.array(psi_zero) + 85000000 * salinity_plant
        self.belowground_resources = psi_sali / psi_zero

    def getTreeWaterUse(self):
        pass


if __name__ == '__main__':
    # Build xml tree snippet
    from lxml import etree

    root = etree.Element("belowground")
    etree.SubElement(root, "type").text = "SaltFeedbackBucket"
    etree.SubElement(root, "min_x").text = "0"
    etree.SubElement(root, "max_x").text = "20"
    etree.SubElement(root, "salinity").text = "0 10/1000"
    etree.SubElement(root, "x_1").text = "0"
    etree.SubElement(root, "x_2").text = "20"
    etree.SubElement(root, "y_1").text = "10"
    etree.SubElement(root, "y_2").text = "0"
    etree.SubElement(root, "domain").text = ""
    etree.SubElement(root, "x_resolution").text = "10"
    etree.SubElement(root, "y_resolution").text = "5"

    resource = SaltFeedbackBucket(args=root)
    resource.prepareNextTimeStep(t_ini=100 * 3600 * 24, t_end=105 * 3600 * 24)
    resource._xe = [5]
    resource.xe = [5]
    resource.ye = [5]
    resource.r_root = [3]


