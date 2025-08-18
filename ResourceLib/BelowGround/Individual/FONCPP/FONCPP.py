#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import numpy as np
from ResourceLib import ResourceModel
from joblib import Parallel, delayed
from multiprocessing import cpu_count

import os, importlib
_pkg = __name__.rsplit(".", 1)[0]  # 'ResourceLib.BelowGround.Individual.FONCPP'
try:
    foncpp = importlib.import_module(f"{_pkg}.foncpp")
except Exception:
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(os.path.dirname(__file__))
    foncpp = importlib.import_module(f"{_pkg}.foncpp")



class FONCPP(ResourceModel):
    """
    Optimized FON with lower peak memory and same results.
    - If C++ backend (fon_hpc) is available, use it automatically.
    - Otherwise use the optimized Python fallback below.
    """

    def __init__(self, args):
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()

        # 网格一次性转换为 float32（C-order），后续不再 astype
        self._gx = np.asarray(self.my_grid[0], dtype=np.float32, order="C")
        self._gy = np.asarray(self.my_grid[1], dtype=np.float32, order="C")

        # 网格栅格尺寸检查（与原逻辑一致）
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
        # 这三个参数在同一物种内通常是常量：每次覆盖保持与原版行为一致
        self.aa = np.float32(parameter["aa"])
        self.bb = np.float32(parameter["bb"])
        self.fmin = np.float32(parameter["fmin"])

    # ===== 线程与分批策略（保持你原逻辑） =====
    def _determine_n_jobs(self, n_plants):
        logical_cores = cpu_count()
        n_jobs = max(1, math.floor(logical_cores * 0.5))
        n_jobs = min(n_jobs, 48)
        return n_jobs

    def _determine_batch_size(self, n_plants, grid_size, force_batch_size=None):
        if force_batch_size is not None:
            return min(force_batch_size, n_plants)
        n_cores = 48
        if grid_size > 2_000_000:
            base_size = 5000
        elif grid_size > 1_000_000:
            base_size = 8000
        elif grid_size > 500_000:
            base_size = 10000
        else:
            base_size = 20000
        dynamic_size = max(base_size, n_plants // (2 * n_cores))
        return min(dynamic_size, n_plants)

    # ===== 主计算 =====
    def calculateBelowgroundResources(self):
        n_plants = len(self._r_stem)
        if n_plants == 0:
            self.belowground_resources = np.array([], dtype=np.float32)
            return

        # 若 C++ 后端存在，则直接调用（确定性：与 Python 串行一致）
        if foncpp is not None:
            px = np.asarray(self._xe, dtype=np.float32)
            py = np.asarray(self._ye, dtype=np.float32)
            rs = np.asarray(self._r_stem, dtype=np.float32)
            threads = self._determine_n_jobs(n_plants)
            resources = foncpp.compute_fon_resources(
                self._gx, self._gy, px, py, rs,
                float(self.aa), float(self.bb), float(self.fmin),
                threads=threads, deterministic=True
            )
            self.belowground_resources = np.asarray(resources, dtype=np.float32)
            return

        # ------- Python fallback（优化版） -------
        xe = np.asarray(self._xe, dtype=np.float32)
        ye = np.asarray(self._ye, dtype=np.float32)
        r_stem = np.asarray(self._r_stem, dtype=np.float32)

        nx, ny = self._gx.shape
        grid_size = nx * ny

        batch_size = self._determine_batch_size(n_plants, grid_size)
        n_jobs = self._determine_n_jobs(n_plants)
        n_batches = (n_plants + batch_size - 1) // batch_size

        resource_limitations = np.empty(n_plants, dtype=np.float32)
        fon_total = np.zeros((nx, ny), dtype=np.float32)
        fon_areas = np.zeros(n_plants, dtype=np.int32)   # 面积用 int，更省内存&明确语义
        fon_sums = np.zeros(n_plants, dtype=np.float32)

        # Pass-1：分批并行，累计 fon_total / fon_sums / fon_areas（不缓存整张 my_fon）
        for batch_idx, start in enumerate(range(0, n_plants, batch_size), start=1):
            end = min(start + batch_size, n_plants)
            percent = batch_idx / n_batches * 100.0
            print(f"[INFO] Pass-1 batch {batch_idx}/{n_batches} ({start}..{end-1}) ... {percent:.2f}%")

            # 并行计算当前批次每棵树的 (local_sum, local_area, local_img)
            # 为了避免峰值内存暴涨，这里只返回 sum/area 以及“对总场的增量累加”
            results = Parallel(n_jobs=n_jobs, prefer="threads")(
                delayed(self._single_fon_reduce)(
                    self._gx, self._gy, xe[i], ye[i], r_stem[i],
                    float(self.aa), float(self.bb), float(self.fmin)
                )
                for i in range(start, end)
            )

            # 聚合：累加 fon_total，并记录 sum/area
            for idx, (local_sum, local_area, local_inc) in enumerate(results, start=start):
                fon_sums[idx] = local_sum
                fon_areas[idx] = local_area
                fon_total += local_inc  # 按批增量叠加，不保留每棵树整图

        total_sum = np.float32(fon_total.sum())

        # Pass-2：分批并行，逐棵树在其支持域上计算 impact_sum
        for batch_idx, start in enumerate(range(0, n_plants, batch_size), start=1):
            end = min(start + batch_size, n_plants)
            percent = batch_idx / n_batches * 100.0
            print(f"[INFO] Pass-2 batch {batch_idx}/{n_batches} ({start}..{end-1}) ... {percent:.2f}%")

            # 并行：每棵树重算一次 my_fon（不保留整张），只在 my_fon>0 的格点上整合 (fon_total - my_fon)
            batch_vals = Parallel(n_jobs=n_jobs, prefer="threads")(
                delayed(self._single_fon_impact)(
                    self._gx, self._gy, xe[i], ye[i], r_stem[i],
                    float(self.aa), float(self.bb), float(self.fmin),
                    fon_total
                )
                for i in range(start, end)
            )

            for i, impact_sum in zip(range(start, end), batch_vals):
                area = fon_areas[i]
                if area == 0:
                    resource_limitations[i] = 1.0
                    continue
                stress = impact_sum / np.float32(area)
                if not np.isfinite(stress):
                    stress = np.float32(0.0)
                res = np.float32(1.0) - np.float32(2.0) * stress
                if res < 0.0:
                    res = 0.0
                resource_limitations[i] = res

        self.belowground_resources = resource_limitations

    # ====== 内部：Python 版单棵树计算 ======
    @staticmethod
    def _fon_params(r_stem, aa, bb, fmin):
        fon_radius = aa * (r_stem ** bb)
        denom = fon_radius - r_stem
        # 与原逻辑一致：可能出现 division-by-zero -> inf
        cc = -np.log(fmin) / denom if denom != 0.0 else np.inf
        return fon_radius, cc

    def _single_fon_reduce(self, gx, gy, x, y, r_stem, aa, bb, fmin):
        """
        返回：local_sum, local_area, local_inc（本棵树对 fon_total 的增量）
        """
        dx = gx - x
        dy = gy - y
        # hypot 比手写 sqrt(dx*dx+dy*dy) 在 MKL/Vec 场景下通常更快且更稳定
        distance = np.hypot(dx, dy, dtype=np.float32)

        fon_radius, cc = self._fon_params(r_stem, aa, bb, fmin)

        # 只分配一次增量图（float32）
        local = np.empty_like(distance, dtype=np.float32)

        if np.isinf(cc):
            # cc=+inf: d<=r_stem -> 1 ; d>r_stem -> 0
            np.less_equal(distance, r_stem, out=local)
            local = local.astype(np.float32, copy=False)
        else:
            np.exp(-cc * (distance - r_stem), out=local)
            # 裁剪：>1 -> 1, <fmin -> 0
            np.minimum(local, 1.0, out=local)
            local[local < fmin] = 0.0

        local_area = int(np.count_nonzero(local))   # 支持域单元数
        local_sum = np.float32(local.sum())         # 本棵树 FON 总和

        return local_sum, local_area, local

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

    # ====== 输入参数（保持原标签） ======
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
