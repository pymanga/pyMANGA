import numpy as np
from ProjectLib import helpers as helpers


class SizeDependentHPC:
    """
    SizeDependent production module with vectorized optimization using float32.
    """

    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): Production module specifications from project file.
        """
        self.getInputParameters(args=xml_args)
        self.iniProductionFormula()

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "formula", "x_geometry"],
            "optional": ["log", "log1", "x_min"]
        }
        myself = super(SizeDependentHPC, self)
        helpers.getInputParameters(myself, **tags)

        # 默认值设置
        if not hasattr(self, "log"):
            self.log = False
            print("INFO: Default value for <Production><SizeDependent><log> is used. Default:", self.log)

        if not hasattr(self, "log1"):
            self.log1 = False
            print("INFO: Default value for <Production><SizeDependent><log1> is used. Default:", self.log1)

        if self.log and self.log1:
            print("ERROR: <Production><SizeDependent><log> and <log1> are both set to TRUE.")
            exit()

        self.x_min = float(self.x_min) if hasattr(self, "x_min") else None

    def iniProductionFormula(self):
        """
        Converts the formula for calculating individual production into a callable function.
        """
        self.production_function = helpers.string_to_function(self, self.formula)

    def getNumberSeeds(self, plants):
        """
        Vectorized calculation of seed numbers using float32.
        Args:
            plants (list): Plant objects from pyMANGA.PopulationLib.PopManager.Plant.
        Returns:
            dict: {"per_individual": List of seed counts per plant}
        """
        # 提取所有 x 值，使用 float32
        x_values = np.array([
            plant.getGeometry().get(self.x_geometry, np.nan) for plant in plants
        ], dtype=np.float32)

        no_new_plants = np.zeros(len(plants), dtype=int)

        valid_mask = ~np.isnan(x_values)
        if self.x_min is not None:
            valid_mask &= (x_values >= np.float32(self.x_min))

        if np.any(valid_mask):
            prod_values = np.array(
                [self.production_function(np.float32(x), np.float32(0)) for x in x_values[valid_mask]],
                dtype=np.float32
            )

            if self.log:
                prod_values = np.floor(np.float32(10.0) ** prod_values).astype(int)
            elif self.log1:
                prod_values = np.maximum(0, np.floor(np.float32(10.0) ** prod_values - 1)).astype(int)
            else:
                prod_values = prod_values.astype(int)

            no_new_plants[valid_mask] = prod_values

        return {"per_individual": no_new_plants.tolist()}
