#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel
from joblib import Parallel, delayed
from multiprocessing import cpu_count


def _compute_single_tree(i, x, y, h_stem, r_ag, grid_x, grid_y, curved_crown, mesh_size, min_r_ag):
    """
    Compute the height and crown area for a single tree based on its position and crown radius.
    """
    dx = grid_x - x
    dy = grid_y - y
    distance_sq = dx * dx + dy * dy

    # determine crown radius
    if r_ag < min_r_ag:
        r_ag = mesh_size

    r_ag_sq = r_ag * r_ag
    mask = distance_sq <= r_ag_sq
    my_height = np.zeros_like(distance_sq)

    # calculate height based on distance
    if curved_crown:
        temp = np.maximum(4 * r_ag_sq - distance_sq[mask], 0)
        my_height[mask] = h_stem + np.sqrt(temp)
    else:
        my_height[mask] = h_stem + 2 * r_ag

    crown_area = np.count_nonzero(mask)
    return i, my_height, crown_area


class AsymmetricZOIHighPerformanceComputing(ResourceModel):
    """
    AsymmetricZOI with batch-parallel merging, optimized for memory efficiency and wins computation
    """

    def __init__(self, args):
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()

    def _determine_n_jobs(self, n_plants):
        """
        Dynamically determine the number of parallel threads based on the number of trees.
        """
        max_threads = min(10, cpu_count())  #   Limit to 10 threads or available CPU cores
        return min(16, max_threads) if n_plants < 10_000 else max_threads   

    def _determine_batch_size(self, n_plants, grid_size, force_batch_size=None):
        """
        Dynamically adjust the batch size based on the grid size. The larger the grid, the smaller the batch size to avoid memory overflow.
        force_batch_size: If not None, a fixed batch size will be enforced.
        """
        if force_batch_size is not None:
            return min(force_batch_size, n_plants)

        if grid_size > 2_000_000:       # Extra-large grid
            base_size = 500
        elif grid_size > 1_000_000:     # Large grid
            base_size = 5000
        elif grid_size > 500_000:       # Medium grid
            base_size = 10000
        else:                           # Small grid
            base_size = 20000          # Default batch size for small grids
        return min(base_size, n_plants)

    def calculateAbovegroundResources(self):
        """
        Calculate above-ground resources allocation.
        """
        n_plants = len(self.xe)
        if n_plants == 0:
            self.aboveground_resources = np.array([])
            return

        grid_x, grid_y = self.my_grid
        canopy_height = np.zeros_like(grid_x)
        highest_plant = np.full_like(grid_x, fill_value=-1, dtype=np.int64)
        crown_areas = np.zeros(n_plants)
        wins = np.zeros(n_plants)

        n_jobs = self._determine_n_jobs(n_plants)
        grid_size = grid_x.size
        batch_size = self._determine_batch_size(n_plants, grid_size, force_batch_size=8000)
        n_batches = (n_plants + batch_size - 1) // batch_size
        print(f"[INFO] Using {n_jobs} threads for {n_plants} plants (batch_size={batch_size}, total_batches={n_batches}).")

        min_r_ag = self.mesh_size * (1 / 2 ** 0.5)
        mask_buffer = np.zeros_like(canopy_height, dtype=bool)

        # Parallel computation in batches
        for batch_idx, start in enumerate(range(0, n_plants, batch_size), start=1):
            end = min(start + batch_size, n_plants)
            percent = batch_idx / n_batches * 100
            print(f"[INFO] Processing batch {batch_idx}/{n_batches} ({start} to {end-1}) ... {percent:.2f}% done.")

            results = Parallel(n_jobs=n_jobs, prefer="threads")(
                delayed(_compute_single_tree)(
                    i, self.xe[i], self.ye[i],
                    self.h_stem[i], self.r_ag[i],
                    grid_x, grid_y, self.curved_crown,
                    self.mesh_size, min_r_ag
                )
                for i in range(start, end)
            )

            # Serial merging of batch results
            for i, my_height, crown_area in results:
                crown_areas[i] = crown_area
                mask_buffer[:] = my_height > canopy_height
                np.copyto(canopy_height, my_height, where=mask_buffer)
                np.copyto(highest_plant, i, where=mask_buffer)

        # Vectorized wins statistics
        valid_idx = highest_plant[highest_plant >= 0]
        counts = np.bincount(valid_idx, minlength=n_plants)
        wins[:] = counts

        self.aboveground_resources = wins / crown_areas

        # check NaN
        if np.any(np.isnan(self.aboveground_resources)):
            nan_indices = np.where(np.isnan(self.aboveground_resources))[0]
            print(f"ERROR: NaN detected in aboveground_resources for plants at indices: {nan_indices}")
            exit()

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"],
            "optional": ["allow_interpolation", "curved_crown"]
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
        try:
            r_ag = geometry["r_crown"]
            h_stem = geometry["h_stem"]
        except KeyError:
            r_ag = geometry["r_ag"]
            h_stem = geometry["height"] - 2 * r_ag

        if r_ag < (self.mesh_size * 1 / 2 ** 0.5):
            if not hasattr(self, "allow_interpolation") or not self.allow_interpolation:
                print("Error: mesh not fine enough for crown dimensions!")
                print("Please refine mesh or increase initial crown radius above " +
                      str(self.mesh_size) + "m !")
                exit()

        self.xe.append(x)
        self.ye.append(y)
        self.h_stem.append(h_stem)
        self.r_ag.append(r_ag)
