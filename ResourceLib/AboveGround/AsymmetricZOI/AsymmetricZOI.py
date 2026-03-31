#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from ResourceLib import ResourceModel

# ---- Try to load C++ core (pybind11) ----------------------------------------
try:
    from ResourceLib.AboveGround.AsymmetricZOI import asymzoi  # compiled C++ core
    _ASYMZOI_OK = True
except Exception:
    asymzoi = None
    _ASYMZOI_OK = False


class AsymmetricZOI(ResourceModel):
    """
    AsymmetricZOI above-ground resource concept.
    Fully compatible with the legacy pure-Python workflow; adds an optional C++ backend.
    """

    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): above-ground module specifications from project file tags
        """
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()
        self._selectBackend()

    # Legacy-compatible Python path
    def calculateAbovegroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on the asymmetric zone of influence concept.
        Sets:
            numpy array of shape(number_of_trees)
        """
        # Choose backend
        if getattr(self, "_backend", "python") == "cpp":
            self._calculateCppCompatible()
            return

        #Array to save value of highest plant with shape = (res_x, res_y)
        canopy_height = np.zeros_like(self.my_grid[0])
        #Array to safe index of highest plant with shape = (res_x, res_y)
        highest_plant = np.full_like(self.my_grid[0], fill_value=-99999)
        #Array to safe number of wins per plant with shape = (n_plants)
        wins = np.zeros_like(self.xe)
        #Array to safe number of grid_points per plant with shape = (n_plants)
        crown_areas = np.zeros_like(self.xe)
        #Iteration over plants to identify highest plant at gridpoint

        for i in range(len(self.xe)):
            distance = (((self.my_grid[0] - np.array(self.xe)[i])**2 +
                         (self.my_grid[1] - np.array(self.ye)[i])**2)**0.5)
            # As the geometry is "complex", my_height is position dependent
            my_height, canopy_bools = self.calculateHeightFromDistance(
                np.array([self.h_stem[i]]), np.array([self.r_ag[i]]),
                distance)
            crown_areas[i] = np.sum(canopy_bools)
            indices = np.where(np.less(canopy_height, my_height))
            canopy_height[indices] = my_height[indices]
            highest_plant[indices] = i
        #Check for each plant, at which gridpoint it is the highest plant

        for i in range(len(self.xe)):
            wins[i] = len(np.where(highest_plant == i)[0])

        self.aboveground_resources = wins / crown_areas

        nan_indices = np.where(np.isnan(self.aboveground_resources))[0]

        if len(nan_indices) > 0:
            print(f"ERROR: NaN detected in aboveground_resources for plants at indices: {nan_indices}")
            exit()

    def calculateHeightFromDistance(self, stem_height, crown_radius, distance):
        """
        Calculate plant heights at each mesh point (node) based on the distance between plant and node.
        Args:
            stem_height (array): stem heights (shape: n_plants)
            crown_radius (array): crown radii (shape: n_plants)
            distance (array): distance between node and stem positions (shape: x_res, y_res)

        Returns:
            array, array (shape: x_res, y_res)
        """
        min_distance = np.min(distance)
        # If crown radius < mesh size, set it to mesh size
        crown_radius[np.where(crown_radius < min_distance)] = min_distance

        bools = crown_radius >= distance
        idx = np.where(bools)
        height = np.zeros_like(distance)
        #Here, the curved top of the plant is considered..
        if self.curved_crown:
            height[idx] = stem_height + (4 * crown_radius ** 2 -
                                         distance[idx] ** 2) ** 0.5
        else:
            height[idx] = stem_height + 2 * crown_radius
        return height, bools

    # C++ accelerated path
    def _calculateCppCompatible(self):
        """
        The C++ acceleration branch packages the data prepared in Python for the pybind11 kernel, which computes the 'above-ground resource factor' for each tree.
        The results are then written back to self.aboveground_resources.

        """
        gx, gy = self._requireGrid()

        xe = np.ascontiguousarray(np.asarray(self.xe, dtype=np.float64))
        ye = np.ascontiguousarray(np.asarray(self.ye, dtype=np.float64))
        h_stem = np.ascontiguousarray(np.asarray(self.h_stem, dtype=np.float64))
        r_ag = np.ascontiguousarray(np.asarray(self.r_ag, dtype=np.float64))
        grid_x = np.ascontiguousarray(gx.astype(np.float64, copy=False))
        grid_y = np.ascontiguousarray(gy.astype(np.float64, copy=False))

        out = asymzoi.compute_aboveground_resources(
            xe, ye, h_stem, r_ag,
            grid_x, grid_y,
            bool(self.curved_crown),
            float(self.mesh_size) if hasattr(self, "mesh_size") else 1.0
        )
        self.aboveground_resources = np.asarray(out, dtype=np.float64)

    # Parameters
    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"],
            "optional": ["allow_interpolation", "curved_crown", "backend_type"],
            "case_insensitive": ["backend_type"]
        }
        super().getInputParameters(**tags)

        self._x_1 = self.x_1
        self._x_2 = self.x_2
        self._y_1 = self.y_1
        self._y_2 = self.y_2
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)

        self.allow_interpolation = super().makeBoolFromArg("allow_interpolation")

        if not hasattr(self, "curved_crown"):
            self.curved_crown = True
            print("INFO: set above-ground parameter curved_crown to default: ", self.curved_crown)
        else:
            self.curved_crown = super().makeBoolFromArg("curved_crown")

        # for backend_type, only accept 'cpp' or 'python'; others/omitted => AUTO
        if not hasattr(self, "backend_type"):
            self.backend_type = "cpp"

    def _selectBackend(self):
        have_cpp = _ASYMZOI_OK
        if self.backend_type == "cpp":
            if have_cpp:
                self._backend = "cpp"
                print("[AsymmetricZOI] Backend = cpp")
            else:
                self._backend = "python"
                print("[AsymmetricZOI] WARNING: <backend_type>cpp</backend_type> set, but C++ core not found. Falling back to python.")
        elif self.backend_type == "python":
            self._backend = "python"
            print("[AsymmetricZOI] Backend = python")
        else:
            self._backend = "cpp" if have_cpp else "python"
            print(f"[AsymmetricZOI] Backend = {self._backend} (auto)")

    def prepareNextTimeStep(self, t_ini, t_end):
        self.xe = []
        self.ye = []
        self.h_stem = []
        self.r_ag = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        # ToDo: resolve when all geometries are renamed

        # Get above-ground radius
        if "r_crown" in geometry:
            r_ag = geometry["r_crown"]
        elif "r_ag" in geometry:
            r_ag = geometry["r_ag"]
        else:
            raise KeyError("Missing above-ground radius: geometry must contain 'r_crown' or 'r_ag'.")

        # Get height
        if "h_stem" in geometry:
            h_stem = geometry["h_stem"]
        elif "height" in geometry:
            h_stem = geometry["height"] - 2 * r_ag
        elif "h_ag" in geometry:
            h_stem = geometry["h_ag"] - 2 * r_ag
        else:
            raise KeyError("Missing height: geometry must contain 'h_stem', 'height', or 'h_ag'.")

        if r_ag < (self.mesh_size * 1 / 2**0.5):
            if not hasattr(self, "allow_interpolation") or not self.allow_interpolation:
                print("Error: mesh not fine enough for crown dimensions!")
                print("Please refine mesh or increase initial crown radius above " +
                      str(self.mesh_size) + "m !")
                exit()

        self.xe.append(x)
        self.ye.append(y)
        self.h_stem.append(h_stem)
        self.r_ag.append(r_ag)

    def _requireGrid(self):
        """
        Confirm that the object contains 'my_grid', that it is not 'None', and that it contains precisely 'grid_x' and 'grid_y'.
        Otherwise, raise an exception immediately and prompt the user to check whether they have forgotten to call the superclass's `makeGrid()` method.
        """
        if not hasattr(self, "my_grid") or self.my_grid is None or len(self.my_grid) != 2:
            raise RuntimeError("Grid not initialized. Did super().makeGrid() run?")
        gx, gy = self.my_grid
        if gx.ndim != 2 or gy.ndim != 2 or gx.shape != gy.shape:
            raise RuntimeError("grid_x and grid_y must be 2D arrays with the same shape.")
        return gx, gy