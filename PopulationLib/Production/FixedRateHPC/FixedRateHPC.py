import numpy as np
from ProjectLib import helpers as helpers

class FixedRateHPC:
    """
    FixedRate production module (vectorized internally, returns Python list).
    """

    def __init__(self, xml_args):
        self.current_step = 0
        self.nth_timestep = 1
        self.getInputParameters(args=xml_args)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type"],
            "optional": ["per_individual", "per_ha", "per_model_area", "nth_timestep"]
        }

        myself = super(FixedRateHPC, self)
        helpers.getInputParameters(myself, **tags)

        # 强制转换 nth_timestep，如果失败就默认设为 1
        try:
            self.nth_timestep = int(self.nth_timestep)
        except (AttributeError, ValueError, TypeError):
            print("INFO: No valid <nth_timestep> specified, using default = 1")
            self.nth_timestep = 1
        print(f"[FixedRateHPC] Final nth_timestep = {self.nth_timestep}")

        if not hasattr(self, "per_model_area"):
            self.per_model_area = None
            print("INFO: Default value for <Production><FixedRate><per_model_area> is used. Default:", self.per_model_area)
        if not hasattr(self, "per_individual"):
            self.per_individual = None
            print("INFO: Default value for <Production><FixedRate><per_individual> is used. Default:", self.per_individual)
        if not hasattr(self, "per_ha"):
            self.per_ha = None
            print("INFO: Default value for <Production><FixedRate><per_ha> is used. Default:", self.per_ha)
        if self.per_model_area and self.per_ha:
            raise ValueError("Both parameters, per_model_area and per_ha, are defined but only one can be used.")


    def getNumberSeeds(self, plants):
        """
        Get number of seeds/seedlings produced in the current timestep.
        """

        # 尝试从 plant 对象中获取当前的 global time
        try:
            any_plant = next(iter(plants.values()))
            current_t = any_plant.getTime()
        except Exception:
            current_t = None

        # 初始化缓存
        if not hasattr(self, "_last_checked_t"):
            self._last_checked_t = current_t
            self._internal_step = 0

        # 若时间推进了才计数
        if current_t != self._last_checked_t:
            self._internal_step += 1
            self._last_checked_t = current_t

        # 判断是否是 nth_timestep
        if self._internal_step % self.nth_timestep != 0:
            return {
                "per_individual": [],
                "per_ha": 0,
                "per_model_area": 0
            }

        per_individual, per_ha, per_model_area = [], 0, 0
        n_plants = len(plants)

        if self.per_individual:
            per_individual = self.getSeedsPerPlant(n_plants)
        if self.per_ha:
            per_ha = self.getSeedsPerHa()
        if self.per_model_area:
            per_model_area = self.getSeedsPerModelArea()

        return {
            "per_individual": per_individual,
            "per_ha": per_ha,
            "per_model_area": per_model_area
        }



    def getSeedsPerPlant(self, no_plants):
        """
        Vectorized creation of seed counts per plant, returning Python list.
        """
        if no_plants <= 0:
            return []
        return np.full(no_plants, self.per_individual, dtype=np.int32).tolist()

    def getSeedsPerHa(self):
        domain_ha = (self.l_x * self.l_y) / 10000
        return domain_ha * self.per_ha

    def getSeedsPerModelArea(self):
        return self.per_model_area

    def setModelDomain(self, x1, x2, y1, y2):
        helpers.setModelDomain(self, x1, x2, y1, y2)
