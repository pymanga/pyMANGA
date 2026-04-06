#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel

# ---- Try to load C++ core (pybind11) ----------------------------------------
try:
    from ResourceLib.BelowGround.Individual.FON import fonzoi  # compiled C++ core
    _FONZOI_OK = True
except Exception:
    fonzoi = None
    _FONZOI_OK = False


class FON(ResourceModel):
    """
    FON (Field of Neighborhood) below-ground resource concept.
    Fully compatible with the legacy pure-Python workflow; adds an optional C++ backend.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()
        self._selectBackend()

    def prepareNextTimeStep(self, t_ini, t_end):
        self._fon_area = []
        self._fon_impact = []
        self._resource_limitation = []
        self._xe = []
        self._ye = []
        self._r_stem = []
        self._aa = []
        self._bb = []
        self._fmin = []
        self._phi = []
        self._t_ini = t_ini
        self._t_end = t_end
        self._fon_height = np.zeros_like(self.my_grid[0])

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self._xe.append(x)
        self._ye.append(y)
        self._r_stem.append(geometry["r_stem"])
        self._aa.append(parameter["aa"])
        self._bb.append(parameter["bb"])
        self._fmin.append(parameter["fmin"])
        self._phi.append(parameter.get("phi", 2.0))
        fon_radius = parameter["aa"] * geometry["r_stem"] ** parameter["bb"]
        if not hasattr(self, '_mesh_warned') and fon_radius < self.mesh_size:
            print(f"Warning: plant FON radius ({fon_radius:.4f}m) is smaller than "
                  f"mesh size ({self.mesh_size:.4f}m). Competition may not be resolved.")
            self._mesh_warned = True

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on competition with neighboring plants.
        Sets:
            numpy array with shape(number_of_plants)
        """
        # Choose backend
        if getattr(self, "_backend", "python") == "cpp":
            self._calculateCppCompatible()
            return

        self._r_stem = np.array(self._r_stem)
        self._aa = np.array(self._aa)
        self._bb = np.array(self._bb)
        self._fmin = np.array(self._fmin)
        self._phi = np.array(self._phi)
        dx = (self.my_grid[0][:, :, np.newaxis] -
              np.array(self._xe)[np.newaxis, np.newaxis, :])
        dy = (self.my_grid[1][:, :, np.newaxis] -
              np.array(self._ye)[np.newaxis, np.newaxis, :])
        if self._periodic_boundary:
            dx = dx - self._lx * np.round(dx / self._lx)
            dy = dy - self._ly * np.round(dy / self._ly)
        distance = (dx**2 + dy**2)**0.5
        my_fon = self.calculateFonFromDistance(distance=distance)

        fon_areas = np.zeros_like(my_fon)
        # Add a one, where plant is larger than 0
        fon_areas[np.where(my_fon > 0)] += 1
        # Count all nodes, which are occupied by plants
        # returns array of shape (nplants)
        fon_areas = fon_areas.sum(axis=(0, 1))
        fon_heights = my_fon.sum(axis=-1)

        fon_impacts = fon_heights[:, :, np.newaxis] - my_fon
        fon_impacts[np.where(my_fon < self._fmin)] = 0
        fon_impacts = fon_impacts.sum(axis=(0, 1))

        # tree-to-tree competition, eq. (7) Berger & Hildenbrandt (2000)
        stress_factor = fon_impacts / fon_areas
        stress_factor = np.nan_to_num(stress_factor, nan=0)
        resource_limitations = 1 - self._phi * stress_factor
        resource_limitations[np.where(resource_limitations < 0)] = 0
        self.belowground_resources = resource_limitations

    def calculateFonFromDistance(self, distance):
        """
        Calculate the FON height of each plant at each grid point.
        Args:
            distance (int): array of distances of all mesh points to plant position
        Returns:
            numpy array with shape(x_grid_points, y_grid_points, number_of_plants)
        """
        # fon radius, eq. (1) Berger et al. 2002
        fon_radius = self._aa * self._r_stem**self._bb
        cc = -np.log(self._fmin) / (fon_radius - self._r_stem)
        height = np.exp(-cc[np.newaxis, np.newaxis, :] *
                        (distance - self._r_stem[np.newaxis, np.newaxis, :]))
        height[height > 1] = 1
        height[height < self._fmin] = 0
        return height

    def getInputParameters(self, args, required_tags=None):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution",
                         "y_resolution"],
            "optional": ["periodic_boundary", "backend_type"],
            "case_insensitive": ["backend_type"]
        }
        super().getInputParameters(**tags)
        self._x_1 = self.x_1
        self._x_2 = self.x_2
        self._y_1 = self.y_1
        self._y_2 = self.y_2
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)
        self._periodic_boundary = self.makeBoolFromArg("periodic_boundary")
        if self._periodic_boundary:
            self._lx = self._x_2 - self._x_1
            self._ly = self._y_2 - self._y_1
        else:
            self._lx = 0.0
            self._ly = 0.0

        if not hasattr(self, "backend_type"):
            self.backend_type = "cpp"

    def _selectBackend(self):
        have_cpp = _FONZOI_OK
        if self.backend_type == "cpp":
            if have_cpp:
                self._backend = "cpp"
                print("[FON] Backend = cpp")
            else:
                self._backend = "python"
                print("[FON] WARNING: <backend_type>cpp</backend_type> set, but C++ core not found. Falling back to python.")
        elif self.backend_type == "python":
            self._backend = "python"
            print("[FON] Backend = python")
        else:
            self._backend = "cpp" if have_cpp else "python"
            print(f"[FON] Backend = {self._backend} (auto)")

    # C++ accelerated path
    def _calculateCppCompatible(self):
        """
        The C++ acceleration branch packages the data prepared in Python for the
        pybind11 kernel, which computes the belowground resource factor for each plant.
        """
        gx, gy = self._requireGrid()

        xe = np.ascontiguousarray(np.asarray(self._xe, dtype=np.float64))
        ye = np.ascontiguousarray(np.asarray(self._ye, dtype=np.float64))
        r_stem = np.ascontiguousarray(np.asarray(self._r_stem, dtype=np.float64))
        aa = np.ascontiguousarray(np.asarray(self._aa, dtype=np.float64))
        bb = np.ascontiguousarray(np.asarray(self._bb, dtype=np.float64))
        fmin = np.ascontiguousarray(np.asarray(self._fmin, dtype=np.float64))
        phi = np.ascontiguousarray(np.asarray(self._phi, dtype=np.float64))
        grid_x = np.ascontiguousarray(gx.astype(np.float64, copy=False))
        grid_y = np.ascontiguousarray(gy.astype(np.float64, copy=False))

        periodic = self._periodic_boundary
        lx = self._lx if periodic else 0.0
        ly = self._ly if periodic else 0.0

        out = fonzoi.compute_belowground_resources(
            xe, ye, r_stem, aa, bb, fmin, phi,
            grid_x, grid_y,
            periodic, lx, ly
        )
        self.belowground_resources = np.asarray(out, dtype=np.float64)

    def _requireGrid(self):
        """Raise RuntimeError if my_grid is absent or malformed."""
        if not hasattr(self, "my_grid") or self.my_grid is None or len(self.my_grid) != 2:
            raise RuntimeError("Grid not initialized. Did super().makeGrid() run?")
        gx, gy = self.my_grid
        if gx.ndim != 2 or gy.ndim != 2 or gx.shape != gy.shape:
            raise RuntimeError("grid_x and grid_y must be 2D arrays with the same shape.")
        return gx, gy
