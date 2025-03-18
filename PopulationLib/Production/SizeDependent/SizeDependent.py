from ProjectLib import helpers as helpers

class SizeDependent:
    """
    SizeDependent production module with an optional threshold for reproduction.
    """

    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): Production module specifications from the project file.
        """
        self.getInputParameters(args=xml_args)
        self.iniProductionFormula()

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "formula", "x_geometry"],
            "optional": ["log", "log1", "x_min"]
        }
        myself = super(SizeDependent, self)
        helpers.getInputParameters(myself, **tags)

        # Set default values if not provided
        if not hasattr(self, "log"):
            self.log = False
            print("INFO: Default value for <production><log> is used. Default:", self.log)

        if not hasattr(self, "log1"):
            self.log1 = False
            print("INFO: Default value for <production><log1> is used. Default:", self.log1)

        if hasattr(self, "x_min"):
            self.x_min = float(self.x_min)
        else:
            self.x_min = None

    def iniProductionFormula(self):
        """
        Converts the formula for calculating individual production, given as a string in the project file,
        into an evaluable function.
        """
        self.production_function = helpers.string_to_function(self, self.formula)

    def getNumberSeeds(self, plants):
        """
        Calculates the number of seeds/seedlings based on the size of the plants
        and provides various statistics on reproduction.

        Args:
            plants (dict): Plant objects from pyMANGA.PopulationLib.PopManager.Plant.

        Returns:
            dict: {"per_individual": List of seed counts per plant}
        """
        no_new_plants = []

        for plant in plants:
            x = plant.getGeometry().get(self.x_geometry)

            if x is None:
                print(f"ERROR: Geometry key '{self.x_geometry}' not found in the plant. "
                      f"Available keys: {list(plant.getGeometry().keys())}")
                continue

            # Check if the plant is capable of reproducing
            if self.x_min is None or x >= self.x_min:

                no_per_plant = self.production_function(x, 0)

                if self.log:
                    no_per_plant = int(10 ** no_per_plant)

                if self.log1:
                    no_per_plant = max(0, int(10 ** no_per_plant - 1))

                no_new_plants.append(no_per_plant)
            else:
                no_new_plants.append(0)

        return {"per_individual": no_new_plants}