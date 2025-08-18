# ResourceLib/AboveGround/AsymmetricZOICPP.py
import math
import numpy as np
from ResourceLib import ResourceModel
from multiprocessing import cpu_count
# —— C++ 后端加载（使用全限定名，避免循环）——
import os, importlib

_pkg = __name__.rsplit(".", 1)[0]  # 'ResourceLib.AboveGround.AsymmetricZOICPP'
try:
    asymzoicpp = importlib.import_module(f"{_pkg}.asymzoicpp")
except Exception:
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(os.path.dirname(__file__))
    asymzoicpp = importlib.import_module(f"{_pkg}.asymzoicpp")



# asymzoicpp 是编译出来的 C++ 扩展模块（.pyd 动态库），不会放在当前目录里，而是安装到当前 conda 环境的 site-packages 里

class AsymmetricZOICPP(ResourceModel):
    """
    与原 Python 版本接口/输出保持一致，但计算内核由 C++ 实现。
    """
    def __init__(self, args):
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()

    def _determine_n_jobs(self, n_plants):
        logical_cores = cpu_count()
        n_jobs = max(1, math.floor(logical_cores * 0.5))
        n_jobs = min(n_jobs, 48)
        return n_jobs

    def _determine_batch_size(self, n_plants, grid_size, force_batch_size=None):
        # 这里保留原接口，但 C++ 内核是不分 batch 的（更稳更快）
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

    def calculateAbovegroundResources(self, force_batch_size=None):
        n_plants = len(self.xe)
        if n_plants == 0:
            self.aboveground_resources = np.array([], dtype=np.float32)
            return

        grid_x = np.ascontiguousarray(self.my_grid[0], dtype=np.float32)
        grid_y = np.ascontiguousarray(self.my_grid[1], dtype=np.float32)


        self.xe = np.asarray(self.xe, dtype=np.float32)
        self.ye = np.asarray(self.ye, dtype=np.float32)
        self.h_stem = np.asarray(self.h_stem, dtype=np.float32)
        self.r_ag = np.asarray(self.r_ag, dtype=np.float32)

        # 线程数与 Python 逻辑一致
        n_jobs = self._determine_n_jobs(n_plants)

        try:
            out = asymzoicpp.compute_aboveground_resources(
                self.xe, self.ye, self.h_stem, self.r_ag,
                grid_x, grid_y,
                bool(self.curved_crown),
                float(self.mesh_size),
                int(n_jobs)
            )
        except RuntimeError as e:
            # 保持与 Python 一致的报错风格
            msg = str(e)
            if "NaN detected in aboveground_resources" in msg:
                print("ERROR:", msg)
                raise SystemExit(1)
            raise

        # 与原版一致：float32 的一维数组
        self.aboveground_resources = np.asarray(out, dtype=np.float32)

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
                raise SystemExit(1)

        self.xe.append(np.float32(x))
        self.ye.append(np.float32(y))
        self.h_stem.append(np.float32(h_stem))
        self.r_ag.append(np.float32(r_ag))
