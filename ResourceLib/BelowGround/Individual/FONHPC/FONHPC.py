#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import numpy as np
from ResourceLib import ResourceModel
from joblib import Parallel, delayed
from multiprocessing import cpu_count


class FONHPC(ResourceModel):
    """
    Optimized FONHPC with less memory allocations but identical results.
    """

    def __init__(self, args):
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()
        if self.mesh_size > 0.25:
            print("Error: mesh not fine enough for FON!")
            print("Please refine mesh to grid size < 0.25m !")
            exit()

    def prepareNextTimeStep(self, t_ini, t_end):
        self._xe = []
        self._ye = []
        self._r_stem = []
        self._t_ini = np.float32(t_ini)
        self._t_end = np.float32(t_end)

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self._xe.append(np.float32(x))
        self._ye.append(np.float32(y))
        self._r_stem.append(np.float32(geometry["r_stem"]))
        self.aa = np.float32(parameter["aa"])
        self.bb = np.float32(parameter["bb"])
        self.fmin = np.float32(parameter["fmin"])

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

    def calculateBelowgroundResources(self):
        n_plants = len(self._r_stem)
        if n_plants == 0:
            self.belowground_resources = np.array([], dtype=np.float32)
            return

        xe = np.array(self._xe, dtype=np.float32)
        ye = np.array(self._ye, dtype=np.float32)
        r_stem = np.array(self._r_stem, dtype=np.float32)

        nx, ny = self.my_grid[0].shape
        grid_size = nx * ny

        batch_size = self._determine_batch_size(n_plants, grid_size)

        resource_limitations = np.empty(n_plants, dtype=np.float32)
        fon_total = np.zeros((nx, ny), dtype=np.float32)
        fon_areas = np.zeros(n_plants, dtype=np.float32)
        fon_sums = np.zeros(n_plants, dtype=np.float32)

        fons_cache = [None] * n_plants

        n_jobs = self._determine_n_jobs(n_plants)
        n_batches = (n_plants + batch_size - 1) // batch_size

        for batch_idx, start in enumerate(range(0, n_plants, batch_size), start=1):
            end = min(start + batch_size, n_plants)
            percent = batch_idx / n_batches * 100
            print(f"[INFO] Processing batch {batch_idx}/{n_batches} ({start} to {end - 1}) ... {percent:.2f}% done.")

            results = Parallel(n_jobs=n_jobs, prefer="threads")(
                delayed(self._calculate_single_fon)(xe[i], ye[i], r_stem[i])
                for i in range(start, end)
            )

            for i, my_fon in zip(range(start, end), results):
                fons_cache[i] = my_fon
                fon_total += my_fon
                fon_areas[i] = np.sum(my_fon > 0)
                fon_sums[i] = my_fon.sum()

        total_sum = fon_total.sum()

        for batch_idx, start in enumerate(range(0, n_plants, batch_size), start=1):
            end = min(start + batch_size, n_plants)
            for i in range(start, end):
                if fon_areas[i] == 0:
                    resource_limitations[i] = 1.0
                    continue
                my_fon = fons_cache[i]
                impact_sum = total_sum - fon_sums[i]

                mask = (my_fon < self.fmin)
                if np.any(mask):
                    impact_sum -= np.sum(fon_total[mask])

                stress_factor = impact_sum / fon_areas[i]
                if np.isnan(stress_factor):
                    stress_factor = 0.0
                resource_limitations[i] = max(0.0, 1.0 - 2.0 * stress_factor)

        self.belowground_resources = resource_limitations

    def _calculate_single_fon(self, x, y, r_stem, out=None):
        dx = self.my_grid[0].astype(np.float32) - np.float32(x)
        dy = self.my_grid[1].astype(np.float32) - np.float32(y)
        distance = np.hypot(dx, dy)

        fon_radius = self.aa * (r_stem ** self.bb)
        cc = -np.log(self.fmin) / (fon_radius - r_stem)

        if out is None:
            out = np.empty_like(distance, dtype=np.float32)

        np.exp(-cc * (distance - r_stem), out=out)
        out[out > 1] = 1.0
        out[out < self.fmin] = 0.0
        return out

    def getInputParameters(self, args, required_tags=None):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2",
                         "x_resolution", "y_resolution"]
        }
        super().getInputParameters(**tags)
        self._x_1 = np.float32(self.x_1)
        self._x_2 = np.float32(self.x_2)
        self._y_1 = np.float32(self.y_1)
        self._y_2 = np.float32(self.y_2)
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)
