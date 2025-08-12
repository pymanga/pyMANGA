#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import numpy as np
from ResourceLib import ResourceModel
from joblib import Parallel, delayed
from multiprocessing import cpu_count


def _compute_single_tree(i, x, y, h_stem, r_ag, grid_x, grid_y, curved_crown, mesh_size, min_r_ag):
    """
    Calculate the crown height and crown cover area of a single tree.
    """
    dx = grid_x - np.float32(x)
    dy = grid_y - np.float32(y)
    distance_sq = dx * dx + dy * dy

    r_ag = np.float32(r_ag)
    mesh_size = np.float32(mesh_size)
    min_r_ag = np.float32(min_r_ag)
    h_stem = np.float32(h_stem)

    if r_ag < min_r_ag:
        r_ag = mesh_size

    r_ag_sq = r_ag * r_ag
    mask = distance_sq <= r_ag_sq
    my_height = np.zeros_like(distance_sq, dtype=np.float32)

    if curved_crown:
        temp = np.maximum(np.float32(4) * r_ag_sq - distance_sq[mask], np.float32(0))
        my_height[mask] = h_stem + np.sqrt(temp, dtype=np.float32)
    else:
        my_height[mask] = h_stem + np.float32(2) * r_ag

    crown_area = np.count_nonzero(mask)
    return i, my_height, crown_area


class AsymmetricZOIHighPerformanceComputing(ResourceModel):
    """
    High-performance computing version of the Asymmetric Zone of Influence (Asymmetric ZOI).
    """

    def __init__(self, args):
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()

    def _determine_n_jobs(self, n_plants):
        logical_cores = cpu_count()
        n_jobs = max(1, math.floor(logical_cores * 0.5))
        n_jobs = min(n_jobs, 48)  # 限制最大 48 核
        return n_jobs

    def _determine_batch_size(self, n_plants, grid_size, force_batch_size=None):
        if force_batch_size is not None:
            return min(force_batch_size, n_plants)

        # 获取可用核心数
        n_cores = 48
        # 根据网格大小确定一个基础大小
        if grid_size > 2_000_000:
            base_size = 5000
        elif grid_size > 1_000_000:
            base_size = 8000
        elif grid_size > 500_000:
            base_size = 10000
        else:
            base_size = 20000

        # **动态放大：让batch_size至少能同时占满核心**
        dynamic_size = max(base_size, n_plants // (2 * n_cores))
        return min(dynamic_size, n_plants)

    def calculateAbovegroundResources(self, force_batch_size=None):
        n_plants = len(self.xe)
        if n_plants == 0:
            self.aboveground_resources = np.array([], dtype=np.float32)
            return

        grid_x, grid_y = (self.my_grid[0].astype(np.float32),
                          self.my_grid[1].astype(np.float32))
        canopy_height = np.zeros_like(grid_x, dtype=np.float32)
        highest_plant = np.full_like(grid_x, fill_value=-1, dtype=np.int32)
        crown_areas = np.zeros(n_plants, dtype=np.float32)
        wins = np.zeros(n_plants, dtype=np.float32)

        n_jobs = self._determine_n_jobs(n_plants)
        grid_size = grid_x.size
        batch_size = self._determine_batch_size(n_plants, grid_size, force_batch_size)
        n_batches = (n_plants + batch_size - 1) // batch_size
        print(f"[INFO] Using {n_jobs} threads for {n_plants} plants (batch_size={batch_size}, total_batches={n_batches}).")

        min_r_ag = np.float32(self.mesh_size * (1 / 2 ** 0.5))
        mask_buffer = np.zeros_like(canopy_height, dtype=bool)

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

            for i, my_height, crown_area in results:
                crown_areas[i] = np.float32(crown_area)
                mask_buffer[:] = my_height > canopy_height
                np.copyto(canopy_height, my_height, where=mask_buffer)
                np.copyto(highest_plant, i, where=mask_buffer)

        valid_idx = highest_plant[highest_plant >= 0]
        counts = np.bincount(valid_idx, minlength=n_plants).astype(np.float32)
        wins[:] = counts

        self.aboveground_resources = wins / crown_areas

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
        self._x_1 = np.float32(self.x_1)
        self._x_2 = np.float32(self.x_2)
        self._y_1 = np.float32(self.y_1)
        self._y_2 = np.float32(self.y_2)
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
        self.t_ini = np.float32(t_ini)
        self.t_end = np.float32(t_end)

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

        self.xe.append(np.float32(x))
        self.ye.append(np.float32(y))
        self.h_stem.append(np.float32(h_stem))
        self.r_ag.append(np.float32(r_ag))
