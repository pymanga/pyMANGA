#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel


class FONHPC(ResourceModel):
    """
    Pure-Python FONHPC (below-ground):
    - Two-pass algorithm, aligned to the C++ window+bitmask design.
    - PASS1: windowed loop with circle mask, accumulate fon_total, record support indices,
             compute per-plant sum and area.
    - PASS2: sum fon_total over each plant's support, exclude own sum, average over area,
             limitation = max(0, 1 - 2 * stress).
    - Strict float32 pipeline; bottom clamp uses strict '<' for v < fmin -> 0; top clamp v>1 -> 1.
    - Output: np.float32 array with shape (n_plants,), stored in self.belowground_resources.
    """

    _F32  = np.float32
    _ZERO = np.float32(0.0)
    _ONE  = np.float32(1.0)
    _TWO  = np.float32(2.0)

    def __init__(self, args):
        # 与 pyMANGA 模式一致：先读参数，再建网格
        self.getInputParameters(args)
        super().makeGrid()

        # 预构造 float32 网格与轴（meshgrid('ij') 假设）
        self._gx32 = np.asarray(self.my_grid[0], dtype=np.float32, order="C")
        self._gy32 = np.asarray(self.my_grid[1], dtype=np.float32, order="C")
        self._nx, self._ny = self._gx32.shape
        self._xs = self._gx32[:, 0].copy()
        self._ys = self._gy32[0, :].copy()

        # 容器
        self._xe = []
        self._ye = []
        self._r_stem = []

        # 模型参数（如每株不同，“最后一个覆盖”与原版一致）
        self.aa   = self._F32(0.0)
        self.bb   = self._F32(1.0)
        self.fmin = self._F32(1e-6)

        # 可选：网格粒度提示（与您之前代码保持一致）
        if hasattr(self, "mesh_size") and self.mesh_size > 0.25:
            print("Error: mesh not fine enough for FON!")
            print("Please refine mesh to grid size < 0.25m !")
            raise SystemExit(1)

    # ---- pyMANGA 生命周期 ----
    def prepareNextTimeStep(self, t_ini, t_end):
        self._xe.clear()
        self._ye.clear()
        self._r_stem.clear()

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry  = plant.getGeometry()
        parameter = plant.getParameter()

        self._xe.append(self._F32(x))
        self._ye.append(self._F32(y))
        self._r_stem.append(self._F32(geometry["r_stem"]))

        # 若每株参数不同，这里采用“最后一株覆盖”以保持与原始习惯一致
        self.aa   = self._F32(parameter["aa"])
        self.bb   = self._F32(parameter["bb"])
        self.fmin = self._F32(parameter["fmin"])

    # ---- 主计算 ----
    def calculateBelowgroundResources(self):
        n_plants = len(self._r_stem)
        if n_plants == 0:
            self.belowground_resources = np.array([], dtype=np.float32)
            return

        px = np.asarray(self._xe, dtype=np.float32)
        py = np.asarray(self._ye, dtype=np.float32)
        rs = np.asarray(self._r_stem, dtype=np.float32)

        nx, ny = self._nx, self._ny
        xs, ys = self._xs, self._ys

        # 预计算每株的 R、R^2、c（严格 float32）
        R  = np.empty(n_plants, dtype=np.float32)
        R2 = np.empty(n_plants, dtype=np.float32)
        cc = np.empty(n_plants, dtype=np.float32)
        for i in range(n_plants):
            ri = rs[i]
            # R = aa * r_stem^bb
            Ri = self._F32(self.aa * self._F32(ri ** self.bb))
            R[i]  = Ri
            R2[i] = self._F32(Ri * Ri)
            denom = self._F32(Ri - ri)
            if denom == 0.0:
                cc[i] = self._F32(np.inf)  # 极限：d<=r → v=1，否则 0
            else:
                cc[i] = self._F32(-np.log(self.fmin) / denom)

        # PASS1：累计场、记录支持域索引、每株 sum 与 area
        fon_total = np.zeros((nx, ny), dtype=np.float32)
        fon_sums  = np.zeros(n_plants, dtype=np.float32)
        fon_area  = np.zeros(n_plants, dtype=np.int32)
        support_indices = [None] * n_plants  # 每株一个线性索引数组

        for i in range(n_plants):
            xi = px[i]; yi = py[i]; ri = rs[i]
            Ri = R[i];  R2i = R2[i]; ci = cc[i]

            i0, i1 = self._find_index_window(xs, xi - Ri, xi + Ri)
            j0, j1 = self._find_index_window(ys, yi - Ri, yi + Ri)
            if i1 < 0 or j1 < 0:
                fon_sums[i] = self._ZERO
                fon_area[i] = 0
                support_indices[i] = np.empty(0, dtype=np.int64)
                continue

            # +1 half-cell 边界（与 C++ 行为一致）
            if i0 > 0:    i0 -= 1
            if i1 < nx-1: i1 += 1
            if j0 > 0:    j0 -= 1
            if j1 < ny-1: j1 += 1

            local_sum = self._ZERO
            local_idx = []

            # 窗口内循环；仅圆内才开方
            for ii in range(i0, i1 + 1):
                ddx  = self._F32(xs[ii] - xi)
                ddx2 = self._F32(ddx * ddx)
                base = ii * ny
                for jj in range(j0, j1 + 1):
                    ddy  = self._F32(ys[jj] - yi)
                    d2   = self._F32(ddx2 + ddy * ddy)
                    if d2 > R2i:
                        continue

                    if np.isinf(ci):
                        v = self._ONE if d2 <= self._F32(ri * ri) else self._ZERO
                    else:
                        d = self._F32(np.sqrt(d2))
                        v = self._F32(np.exp(self._F32(-ci * (d - ri))))
                        if v > self._ONE:
                            v = self._ONE
                        if v < self.fmin:  # 严格 '<'
                            v = self._ZERO

                    if v > self._ZERO:
                        fon_total[ii, jj] += v  # 顺序累加（可复现）
                        local_sum += v
                        local_idx.append(base + jj)

            fon_sums[i] = self._F32(local_sum)
            fon_area[i] = len(local_idx)
            support_indices[i] = (np.fromiter(local_idx, dtype=np.int64, count=len(local_idx))
                                  if local_idx else np.empty(0, dtype=np.int64))

        # PASS2：在支持域上累加 total，再减去自身，平均到 area
        resources = np.empty(n_plants, dtype=np.float32)
        flat_total = fon_total.ravel()  # 线性访问

        for i in range(n_plants):
            area = int(fon_area[i])
            if area == 0:
                resources[i] = self._ONE
                continue

            idxs = support_indices[i]
            sum_total_on_support = self._ZERO
            # 手动累加以保持 float32（避免默认 float64）
            for idx in idxs:
                sum_total_on_support += flat_total[idx]

            impact = self._F32(sum_total_on_support - fon_sums[i])
            stress = self._F32(impact / self._F32(area))
            if not np.isfinite(stress):
                stress = self._ZERO

            res = self._F32(self._ONE - self._TWO * stress)
            if res < self._ZERO:
                res = self._ZERO
            resources[i] = res

        self.belowground_resources = resources  # shape=(n_plants,), float32

    # ---- 输入参数 ----
    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2",
                         "x_resolution", "y_resolution"],
            "optional": []  # 如需扩展 threads/deterministic，可加入这里（本纯Python版未用）
        }
        super().getInputParameters(**tags)

    # ---- 与 C++ find_index_window 对齐的窗口搜索 ----
    @staticmethod
    def _find_index_window(axis: np.ndarray, lo: np.float32, hi: np.float32):
        """
        输入：
          axis: 单轴坐标（长度 n），可能非严格单调
          lo, hi: 窗口边界（闭区间）
        输出：
          (i0, i1) 闭区间索引，若空则 (0, -1)
        逻辑与 C++ 版保持一致：
          - 单调（非降或非升）用 searchsorted
          - 非单调退化为线性裁剪
          - 最后做边界截断
        """
        n = axis.size
        if n == 0:
            return 0, -1

        d = np.diff(axis)
        nondec = np.all(d >= 0)
        noninc = np.all(d <= 0)

        if nondec:
            i0 = int(np.searchsorted(axis, lo, side="left"))
            i1 = int(np.searchsorted(axis, hi, side="right")) - 1
        elif noninc:
            neg = -axis
            i0 = int(np.searchsorted(neg, -lo, side="left"))
            i1 = int(np.searchsorted(neg, -hi, side="right")) - 1
        else:
            # 非单调：全局裁剪
            lo_, hi_ = (lo, hi) if lo <= hi else (hi, lo)
            L = 0
            R = n - 1
            while L < n and axis[L] < lo_:
                L += 1
            while R >= 0 and axis[R] > hi_:
                R -= 1
            i0, i1 = L, R

        # 截断
        if i0 < 0:
            i0 = 0
        if i1 >= n:
            i1 = n - 1
        if i0 > i1:
            return 0, -1
        return i0, i1
