#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import math
import numpy as np
import pandas as pd
import importlib

from ResourceLib import ResourceModel

# ---- 尝试加载 C++ 后端 -------------------------------------------------------
_pkg = __name__.rsplit(".", 1)[0]  # e.g. 'ResourceLib.BelowGround.Salinity.FixedSalinityCPP'
try:
    fixedsalcpp = importlib.import_module("fixedsalcpp")
except Exception:
    # 尝试相对目录（Windows 动态库路径支持）
    try:
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(os.path.dirname(__file__))
        fixedsalcpp = importlib.import_module("fixedsalcpp")
    except Exception:
        fixedsalcpp = None


class FixedSalinityCPP(ResourceModel):
    """
    FixedSalinity below-ground resource concept with C++ backend.
    - 若 fixedsalcpp 可用：调用 C++ 版本（constant / sine / timeseries）
    - 否则：回退到 NumPy 版本
    输出：
        self.belowground_resources: np.ndarray(shape=(n_plants,), dtype=float64)
    """

    # --------------------------- 生命周期钩子 ---------------------------
    def __init__(self, args):
        case = args.find("type").text
        self.getInputParameters(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        self.plants = []
        self._t_ini = float(t_ini)
        self._t_end = float(t_end)

        # 缓存每株参数
        self._xe = []
        self._h_stem = []
        self._r_crown = []
        self._psi_leaf = []
        self._r_salinity = []      # "bettina"/"forman"/None
        self._salt_effect_d = []   # 仅 forman
        self._salt_effect_ui = []  # 仅 forman

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self.plants.append(plant)

        # 位置
        self._xe.append(float(x))

        # r_salinity 类型
        r_sal = parameter.get("r_salinity", None)
        self._r_salinity.append(r_sal if r_sal is not None else None)

        # 物种参数（可能缺失）
        try:
            self._salt_effect_d.append(float(parameter["salt_effect_d"]))
            self._salt_effect_ui.append(float(parameter["salt_effect_ui"]))
        except Exception:
            self._salt_effect_d.append(np.nan)
            self._salt_effect_ui.append(np.nan)

        # 几何与生理
        try:
            self._h_stem.append(float(geometry["h_stem"]))
            self._r_crown.append(float(geometry["r_crown"]))
            self._psi_leaf.append(float(parameter["leaf_water_potential"]))
        except Exception:
            # psi_leaf 缺失时，保持与原实现一致的容错（后续仅 bettina 用）
            self._h_stem.append(np.nan)
            self._r_crown.append(np.nan)
            self._psi_leaf.append(np.nan)

    # --------------------------- 主计算入口 ---------------------------
    def calculateBelowgroundResources(self):
        n = len(self._xe)
        if n == 0:
            self.belowground_resources = np.array([], dtype=np.float64)
            return

        # r_salinity -> 编码：1=bet, 2=for, 0=忽略（与原版“只在对应 idx 填值”一致）
        r_code = np.zeros(n, dtype=np.int8)
        for i, t in enumerate(self._r_salinity):
            if t is None:
                r_code[i] = 0
            elif isinstance(t, str):
                tt = t.strip().lower()
                if tt == "bettina":
                    r_code[i] = 1
                elif tt == "forman":
                    r_code[i] = 2
                else:
                    r_code[i] = 0
            else:
                r_code[i] = 0

        plant_x = np.asarray(self._xe, dtype=np.float64)
        h_stem = np.asarray(self._h_stem, dtype=np.float64)
        r_crown = np.asarray(self._r_crown, dtype=np.float64)
        psi_leaf = np.asarray(self._psi_leaf, dtype=np.float64)
        salt_d = np.asarray(self._salt_effect_d, dtype=np.float64)
        salt_ui = np.asarray(self._salt_effect_ui, dtype=np.float64)

        # 选择 C++/Python 路径
        use_cpp = fixedsalcpp is not None

        # 计算当步边界盐度与（可选）空间-分布扰动
        if hasattr(self, "t_variable"):
            # ---- time series 模式 ----
            left, right, used_ts_exact = self._get_border_from_timeseries(self._t_ini)
            # C++：内部自带时间插值与分布/噪声；Python 回退：手动实现
            if use_cpp:
                dist_type, deviation, relative, seed = self._map_distribution_args()
                out = fixedsalcpp.compute_resources_timeseries(
                    plant_x, r_code, h_stem, r_crown, psi_leaf, salt_d, salt_ui,
                    float(self.min_x), float(self.max_x),
                    self._salinity_over_t, float(self._t_ini),
                    dist_type, deviation, relative, seed
                )
                self.belowground_resources = np.asarray(out, dtype=np.float64)

                # 写入 growth_concept_information['salinity']
                # 若未启用分布/噪声，则可在 Python 端复现 salinity_plant（与 C++ 一致）
                if dist_type == "" and not np.any(np.isnan([left, right])):
                    sal_plant = self._spatial_interp_salinity(plant_x, left, right)
                    self._write_salinity_to_plants(sal_plant)
                else:
                    # 无法 100% 复现 C++ 内部采样，这里就不覆盖，保持原有行为安全
                    pass

            else:
                left, right = self._ensure_bc_valid(left, right)
                sal_plant = self._spatial_interp_salinity(plant_x, left, right)
                sal_plant = self._maybe_apply_distribution(sal_plant, left, right)
                self._calc_resources_numpy(r_code, h_stem, r_crown, psi_leaf, salt_d, salt_ui, sal_plant)
                self._write_salinity_to_plants(sal_plant)

        elif hasattr(self, "amplitude"):
            # ---- sine 模式 ----
            s0 = self.amplitude * math.sin(self._t_ini / self.stretch + self.offset)
            left_base = self.left_bc
            right_base = self.right_bc
            if use_cpp:
                dist_type, deviation, relative, seed = self._map_distribution_args()
                out = fixedsalcpp.compute_resources_sine(
                    plant_x, r_code, h_stem, r_crown, psi_leaf, salt_d, salt_ui,
                    float(self.min_x), float(self.max_x),
                    float(self._t_ini), float(self.amplitude), float(self.stretch),
                    float(self.offset), float(self.noise),
                    float(left_base), float(right_base),
                    dist_type, deviation, relative, seed
                )
                self.belowground_resources = np.asarray(out, dtype=np.float64)

                # 仅当 noise=0 且未启用分布时，可复现 salinity_plant
                if (self.noise == 0) and dist_type == "":
                    left = s0 + left_base
                    right = s0 + right_base
                    left, right = self._ensure_bc_valid(left, right)
                    sal_plant = self._spatial_interp_salinity(plant_x, left, right)
                    self._write_salinity_to_plants(sal_plant)
            else:
                left = s0 + left_base
                right = s0 + right_base
                left, right = self._ensure_bc_valid(left, right)
                # Python 版：在边界加噪声
                if self.noise and self.noise > 0:
                    left = float(np.random.normal(loc=left, scale=self.noise))
                    right = float(np.random.normal(loc=right, scale=self.noise))
                    left = left if left > 0 else 0.0
                    right = right if right > 0 else 0.0
                sal_plant = self._spatial_interp_salinity(plant_x, left, right)
                sal_plant = self._maybe_apply_distribution(sal_plant, left, right)
                self._calc_resources_numpy(r_code, h_stem, r_crown, psi_leaf, salt_d, salt_ui, sal_plant)
                self._write_salinity_to_plants(sal_plant)

        else:
            # ---- constant 边界 ----
            left, right = self.left_bc, self.right_bc
            left, right = self._ensure_bc_valid(left, right)
            if use_cpp:
                dist_type, deviation, relative, seed = self._map_distribution_args()
                out = fixedsalcpp.compute_resources_constant(
                    plant_x, r_code, h_stem, r_crown, psi_leaf, salt_d, salt_ui,
                    float(self.min_x), float(self.max_x),
                    float(left), float(right),
                    dist_type, deviation, relative, seed
                )
                self.belowground_resources = np.asarray(out, dtype=np.float64)

                # 未启用分布时可复现 salinity_plant
                if dist_type == "":
                    sal_plant = self._spatial_interp_salinity(plant_x, left, right)
                    self._write_salinity_to_plants(sal_plant)
            else:
                sal_plant = self._spatial_interp_salinity(plant_x, left, right)
                sal_plant = self._maybe_apply_distribution(sal_plant, left, right)
                self._calc_resources_numpy(r_code, h_stem, r_crown, psi_leaf, salt_d, salt_ui, sal_plant)
                self._write_salinity_to_plants(sal_plant)

    # --------------------------- NumPy 回退实现 ---------------------------
    def _calc_resources_numpy(self, r_code, h_stem, r_crown, psi_leaf, salt_d, salt_ui, sal_plant):
        res = np.zeros_like(sal_plant, dtype=np.float64)

        # bettina
        idx_b = np.where(r_code == 1)[0]
        if idx_b.size > 0:
            psi_zero = psi_leaf[idx_b] + (2.0 * r_crown[idx_b] + h_stem[idx_b]) * 9810.0
            psi_sali = psi_zero + 85000000.0 * sal_plant[idx_b]
            res[idx_b] = psi_sali / psi_zero

        # forman
        idx_f = np.where(r_code == 2)[0]
        if idx_f.size > 0:
            expo = salt_d[idx_f] * (salt_ui[idx_f] - sal_plant[idx_f] * 1000.0)  # ppt
            res[idx_f] = 1.0 / (1.0 + np.exp(expo))

        self.belowground_resources = res

    # --------------------------- 工具：边界与分布 ---------------------------
    def _spatial_interp_salinity(self, plant_x, left, right):
        # 与 Python 原版 getPlantSalinity 的空间线性插值一致
        L = float(self.max_x) - float(self.min_x)
        if L == 0.0:
            return np.full_like(plant_x, 0.5 * (left + right), dtype=np.float64)
        slope = (right - left) / L
        return (plant_x - float(self.min_x)) * slope + left

    def _maybe_apply_distribution(self, salinity_plant, left_bc, right_bc):
        # 与原版 getSalinityDistribution 等价
        if not hasattr(self, "distribution"):
            return salinity_plant

        t = getattr(self, "type", "normal")
        dev = getattr(self, "deviation", 5.0 / 1000.0)
        rel = getattr(self, "relative", False)

        t_low = str(t).lower()
        if t_low.startswith("norm"):
            if rel:
                out = np.array([np.random.normal(loc=mu, scale=max(mu * dev, 0.0))
                                for mu in salinity_plant], dtype=np.float64)
            else:
                out = np.array([np.random.normal(loc=mu, scale=dev)
                                for mu in salinity_plant], dtype=np.float64)
        elif t_low.startswith("uni"):
            out = np.random.uniform(low=left_bc, high=right_bc, size=salinity_plant.shape[0])
        else:
            raise KeyError(f"Distribution parameter 'type={t}' does not exist. "
                           "Check inputs for FixedSalinity.")

        out[out < 0.0] = 0.0
        return out

    def _get_border_from_timeseries(self, t_ini):
        """
        返回 (left, right, found_exact)
        - 若命中时间点：直接取
        - 若夹在两点：线性插值
        - 若越界：取端点
        """
        A = self._salinity_over_t  # shape (N,3): [t, left, right]
        tcol = A[:, 0]
        # 精确命中
        hit = np.where(tcol == t_ini)[0]
        if hit.size > 0:
            row = A[hit[0], :]
            return float(row[1]), float(row[2]), True

        # 找 before / after
        before = np.where(tcol < t_ini)[0]
        after = np.where(tcol > t_ini)[0]
        if before.size > 0 and after.size > 0:
            ib = before[-1]
            ia = after[0]
            tb, lb, rb = A[ib, 0], A[ib, 1], A[ib, 2]
            ta, la, ra = A[ia, 0], A[ia, 1], A[ia, 2]
            w = (t_ini - tb) / (ta - tb)
            left = lb + w * (la - lb)
            right = rb + w * (ra - rb)
            return float(left), float(right), False
        else:
            # 越界取端点
            if t_ini < tcol.min():
                row = A[0, :]
            else:
                row = A[-1, :]
            return float(row[1]), float(row[2]), False

    def _ensure_bc_valid(self, left, right):
        # 与原版 checkSalinityInput 同步的基本校验
        if (left > 1.0) or (right > 1.0):
            raise ValueError("ERROR: Salinity over 1000 ppt. "
                             "Are you sure the salinity is in kg/kg (not ppt)?")
        left = left if left > 0 else 0.0
        right = right if right > 0 else 0.0
        return left, right

    def _map_distribution_args(self):
        """
        将 Python 端 distribution 配置映射为 C++ 接口：
            "" | "normal" | "normal_relative" | "uniform"
        返回：(distribution_type, deviation, relative, seed)
        说明：为保证复现，默认不传 seed，由 C++ 使用随机设备/或用户可扩展传 seed。
        """
        if not hasattr(self, "distribution"):
            return "", 0.0, False, None

        t = getattr(self, "type", "normal")
        dev = float(getattr(self, "deviation", 5.0 / 1000.0))
        rel = bool(getattr(self, "relative", False))

        t_low = str(t).lower()
        if t_low.startswith("uni"):
            dist = "uniform"
        elif t_low.startswith("norm"):
            dist = "normal_relative" if rel else "normal"
        else:
            raise KeyError(f"Distribution parameter 'type={t}' does not exist for FixedSalinity.")

        # 你也可以在 XML 中扩展一个 <seed> 字段用于复现；如果没有则传 None
        seed = getattr(self, "seed", None)
        if seed is not None:
            try:
                seed = int(seed)
            except Exception:
                seed = None
        return dist, dev, rel, seed

    def _write_salinity_to_plants(self, salinity_plant):
        # 将当步每株盐度写入 growth_concept_information['salinity']（与原版一致）
        for i, plant in enumerate(self.plants):
            gci = plant.getGrowthConceptInformation()
            gci["salinity"] = float(salinity_plant[i])
            plant.setGrowthConceptInformation(gci)

    # --------------------------- 参数读入（与原版标签兼容） ---------------------------
    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "min_x", "max_x", "salinity"],
            "optional": ["sine", "amplitude", "stretch", "offset", "noise",
                         "distribution", "type", "deviation", "relative", "seed"]
        }
        super().getInputParameters(**tags)
        self._setDefaultParameters()
        self._checkSalinityInput()

    def _setDefaultParameters(self):
        # 直接把 <salinity> 读进来（字符串 path 或 "left right"）
        self._salinity = self.salinity

        # 读取 min/max
        try:
            self.min_x = float(self.min_x)
            self.max_x = float(self.max_x)
        except Exception:
            pass

        # 解析 salinity 标签：常量 or CSV
        self._readSalinityTag()

        # 分布参数默认
        self.relative = super().makeBoolFromArg("relative")

        # 正弦参数默认
        if hasattr(self, "sine"):
            if not hasattr(self, "amplitude"):
                print("> Set sine parameter 'amplitude' to default: 0")
                self.amplitude = 0.0
            if not hasattr(self, "stretch"):
                print("> Set sine parameter 'stretch' to default: 58*3600*24")
                self.stretch = 58 * 3600 * 24
            if not hasattr(self, "noise"):
                print("> Set sine parameter 'noise' to default: 0")
                self.noise = 0.0
            if not hasattr(self, "offset"):
                print("> Set sine parameter 'offset' to default: 0")
                self.offset = 0.0

        if hasattr(self, "distribution"):
            if not hasattr(self, "type"):
                print("> Set distribution parameter 'type' to default: normal")
                self.type = "normal"
            if not hasattr(self, "deviation"):
                print("> Set distribution parameter 'deviation' to default: 0.005 (5 ppt)")
                self.deviation = 5.0 / 1000.0
            if not hasattr(self, "relative"):
                print("> Set distribution parameter 'relative' to default: false")
                self.relative = False

    def _readSalinityTag(self):
        """
        解析 <salinity>：
        - "L R" 两个常数（kg/kg）
        - CSV 路径（分隔符 ; , 或 \t），三列 [t,left,right]
        """
        s = str(self._salinity)
        parts = s.split()
        if len(parts) == 2:
            # 常数边界
            left = float(eval(parts[0]))
            right = float(eval(parts[1]))
            self.left_bc = left
            self.right_bc = right
        elif os.path.exists(s):
            # CSV 时序
            sal_over_t = pd.read_csv(s, delimiter=";|,|\t", engine="python")
            A = sal_over_t.to_numpy()
            if A.ndim != 2 or A.shape[1] != 3:
                raise KeyError("Problems occurred when reading the salinity file. "
                               "Expect 3 columns: [t, left, right].")
            self._salinity_over_t = A.astype(np.float64, copy=False)
            self.t_variable = True
        else:
            raise KeyError("Wrong definition of <salinity>. "
                           "Use two constants 'left right' (kg/kg) or path to CSV with columns [t,left,right].")

    def _checkSalinityInput(self):
        # 当 left/right 已存在时先做一次快速检测
        if hasattr(self, "left_bc") and hasattr(self, "right_bc"):
            if (self.left_bc > 1.0) or (self.right_bc > 1.0):
                raise ValueError("ERROR: Salinity over 1000 ppt. "
                                 "Are you sure the salinity is in kg/kg (not ppt)?")
