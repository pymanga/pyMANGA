import numpy as np
import pandas as pd
import os
from ResourceLib import ResourceModel
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import math


class FixedSalinityHighPerformanceComputing(ResourceModel):
    """
    FixedSalinity below-ground resource concept (optimized, float32, with parallel batch computation).
    """

    def __init__(self, args):
        case = args.find("type").text
        self.getInputParameters(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        self.plants = []
        self._xe = []
        self._r_salinity = []
        self._salt_effect_d = []
        self._salt_effect_ui = []
        self._h_stem = []
        self._r_crown = []
        self._psi_leaf = []
        self._t_ini = np.float32(t_ini)
        self._t_end = np.float32(t_end)

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()

        self.plants.append(plant)
        self._xe.append(np.float32(x))
        self._r_salinity.append(parameter.get("r_salinity", "unknown"))
        self._salt_effect_d.append(np.float32(parameter.get("salt_effect_d", 0.0)))
        self._salt_effect_ui.append(np.float32(parameter.get("salt_effect_ui", 0.0)))
        self._h_stem.append(np.float32(geometry.get("h_stem", 0)))
        self._r_crown.append(np.float32(geometry.get("r_crown", 0)))
        self._psi_leaf.append(np.float32(parameter.get("leaf_water_potential", 0)))

    def _determine_n_jobs(self, n_plants):
        logical_cores = cpu_count()
        n_jobs = max(1, math.floor(logical_cores * 0.5))
        n_jobs = min(n_jobs, 48)  # 限制最大 48 核
        return n_jobs
    

    def _determine_batch_size(self, n_plants, force_batch_size=None):
        if force_batch_size is not None:
            return min(force_batch_size, n_plants)
        base_size = 50000
        return min(base_size, n_plants)

    def calculateBelowgroundResources(self):
        n_plants = len(self.plants)
        if n_plants == 0:
            self.belowground_resources = np.array([], dtype=np.float32)
            return

        salinity_plant = self.getPlantSalinity()

        # Convert parameters to numpy arrays once
        r_salinity = np.array(self._r_salinity)
        salt_effect_d = np.array(self._salt_effect_d, dtype=np.float32)
        salt_effect_ui = np.array(self._salt_effect_ui, dtype=np.float32)
        psi_leaf = np.array(self._psi_leaf, dtype=np.float32)
        r_crown = np.array(self._r_crown, dtype=np.float32)
        h_stem = np.array(self._h_stem, dtype=np.float32)

        batch_size = self._determine_batch_size(n_plants)
        n_jobs = self._determine_n_jobs(n_plants)

        resource_limitations = np.zeros(n_plants, dtype=np.float32)

        def calc_batch(start_idx, end_idx):
            batch_results = []
            for i in range(start_idx, end_idx):
                r_sal = r_salinity[i]
                s = salinity_plant[i]
                if r_sal == "bettina":
                    psi_zero = psi_leaf[i] + (2 * r_crown[i] + h_stem[i]) * 9810
                    psi_sali = psi_zero + 8.5e7 * s
                    val = psi_sali / psi_zero
                elif r_sal == "forman":
                    exp = salt_effect_d[i] * (salt_effect_ui[i] - s * 1000)
                    val = 1 / (1 + np.exp(exp))
                else:
                    val = 1.0  # Default no limitation
                batch_results.append((i, val))
            return batch_results

        results = Parallel(n_jobs=n_jobs, prefer="threads")(
            delayed(calc_batch)(start, min(start + batch_size, n_plants))
            for start in range(0, n_plants, batch_size)
        )

        # Flatten results and assign
        for batch_result in results:
            for i, val in batch_result:
                resource_limitations[i] = val

        self.belowground_resources = resource_limitations

        # Update each plant's growth concept information
        for i, plant in enumerate(self.plants):
            gci = plant.getGrowthConceptInformation()
            gci['salinity'] = salinity_plant[i]
            gci['belowground_resource'] = resource_limitations[i]
            plant.setGrowthConceptInformation(gci)

    def getPlantSalinity(self):
        self.getBorderSalinity()
        xe = np.array(self._xe, dtype=np.float32)
        salinity_plant = ((xe - self._min_x) /
                          (self._max_x - self._min_x) *
                          (self._salinity[1] - self._salinity[0]) +
                          self._salinity[0])
        if hasattr(self, "distribution"):
            salinity_plant = self.getSalinityDistribution(salinity_plant)
        return salinity_plant.astype(np.float32)

    def getBorderSalinity(self):
        self._xe = np.array(self._xe, dtype=np.float32)
        if hasattr(self, "t_variable"):
            self.getSalinityTimeseries()
        elif hasattr(self, "amplitude"):
            self.getSalinitySine()

    def getSalinityDistribution(self, salinity_plant):
        if self.type.startswith("norm"):
            if self.relative:
                salinity_plant_new = np.random.normal(loc=salinity_plant, scale=salinity_plant * self.deviation).astype(np.float32)
            else:
                salinity_plant_new = np.random.normal(loc=salinity_plant, scale=self.deviation).astype(np.float32)
            return np.clip(salinity_plant_new, 0, None)
        elif self.type.startswith("uni"):
            return np.random.uniform(np.float32(self._salinity[0]), np.float32(self._salinity[1]), len(salinity_plant)).astype(np.float32)
        else:
            raise ValueError(f"Error: Distribution parameter 'type = {self.type}' does not exist.")

    def getSalinitySine(self):
        s0 = np.float32(self.amplitude) * np.sin(np.float32(self._t_ini) / np.float32(self.stretch) + np.float32(self.offset))
        left = s0 + np.float32(self.left_bc)
        self._salinity[0] = max(0, np.random.normal(loc=left, scale=np.float32(self.noise)))
        right = s0 + np.float32(self.right_bc)
        self._salinity[1] = max(0, np.random.normal(loc=right, scale=np.float32(self.noise)))

    def getSalinityTimeseries(self):
        ts = self._salinity_over_t[:, 0].astype(np.float32)
        if np.isclose(self._t_ini, ts).any():
            self._salinity = self._salinity_over_t[np.isclose(ts, self._t_ini), 1:][0].astype(np.float32)
        else:
            idx = np.searchsorted(ts, self._t_ini)
            if idx == 0:
                self._salinity = self._salinity_over_t[0, 1:].astype(np.float32)
            elif idx >= len(ts):
                self._salinity = self._salinity_over_t[-1, 1:].astype(np.float32)
            else:
                ts_before = idx - 1
                frac = (self._t_ini - ts[ts_before]) / (ts[idx] - ts[ts_before])
                sal_left = self._salinity_over_t[ts_before, 1] + frac * (self._salinity_over_t[idx, 1] - self._salinity_over_t[ts_before, 1])
                sal_right = self._salinity_over_t[ts_before, 2] + frac * (self._salinity_over_t[idx, 2] - self._salinity_over_t[ts_before, 2])
                self._salinity = np.array([sal_left, sal_right], dtype=np.float32)
        self.checkSalinityInput()

    def checkSalinityInput(self):
        if np.any(np.array(self._salinity, dtype=np.float32) > np.float32(1)):
            raise ValueError("ERROR: Salinity over 1000 ppt. Check units.")

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "min_x", "max_x", "salinity"],
            "optional": ["sine", "amplitude", "stretch", "offset", "noise",
                         "distribution", "type", "deviation", "relative"]
        }
        super().getInputParameters(**tags)
        self.setDefaultParameters()
        self.checkSalinityInput()

    def setDefaultParameters(self):
        self._salinity = [np.float32(v) for v in self.salinity] if isinstance(self.salinity, (list, tuple)) else self.salinity
        self._min_x = np.float32(getattr(self, "min_x", 0))
        self._max_x = np.float32(getattr(self, "max_x", 1))
        self.readSalinityTag()
        self.relative = super().makeBoolFromArg("relative")

        if hasattr(self, "sine"):
            self.amplitude = np.float32(getattr(self, "amplitude", 0))
            self.stretch = np.float32(getattr(self, "stretch", 58 * 3600 * 24))
            self.noise = np.float32(getattr(self, "noise", 0))
            self.offset = np.float32(getattr(self, "offset", 0))

        if hasattr(self, "distribution"):
            self.distribution = getattr(self, "distribution", "normal")
            self.deviation = np.float32(getattr(self, "deviation", 5 / 1000))
            self.relative = getattr(self, "relative", False)

    def readSalinityTag(self):
        if isinstance(self._salinity, str) and len(self._salinity.split()) == 2:
            vals = self._salinity.split()
            self._salinity = [np.float32(eval(vals[0])), np.float32(eval(vals[1]))]
            self.left_bc, self.right_bc = self._salinity
        elif os.path.exists(self._salinity):
            salinity_over_t = pd.read_csv(self._salinity, delimiter=";|,|\t", engine='python')
            self._salinity_over_t = salinity_over_t.to_numpy(dtype=np.float32)
            if self._salinity_over_t.shape[1] != 3:
                raise KeyError("Salinity file format error.")
            self.t_variable = True
        else:
            raise KeyError("Wrong salinity definition in belowground competition definition.")
