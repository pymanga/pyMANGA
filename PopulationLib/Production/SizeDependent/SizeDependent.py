from ProjectLib import helpers as helpers

class SizeDependent:
    """
    SizeDependent production module with optional threshold for reproduction.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): production module specifications from project file tags
        """
        self.getInputParameters(args=xml_args)
        self.iniProductionFormula()

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "formula", "x_geometry"],
            "optional": ["log", "min_r_stem"]  # 🆕 min_r_stem als optionale Variable hinzugefügt
        }
        myself = super(SizeDependent, self)
        helpers.getInputParameters(myself, **tags)

        if not hasattr(self, "log"):
            self.log = False
            print("INFO: Default value for <production><log> is used. Default:", self.log)

        if hasattr(self, "min_r_stem"):
            self.min_r_stem = float(self.min_r_stem)  # Sicherstellen, dass der Wert als Zahl interpretiert wird
        else:
            self.min_r_stem = None  # Standardmäßig deaktiviert

    def iniProductionFormula(self):
        """
        Convert the formula for calculating individual production, given as a string in the project file,
        into an evaluable formula.
        """
        self.production_function = helpers.string_to_function(self, self.formula)

    def getNumberSeeds(self, plants):
        """
        Get number of seeds/seedlings produced in the current timestep based on the geometry (size) of the existing plants.
        Args:
            plants (dict): plant object, see ``pyMANGA.PopulationLib.PopManager.Plant``
        Returns:
            int or array of length = number of plants in previous timestep
        """
        no_new_plants = []
        for plant in plants:
            x = plant.getGeometry()[self.x_geometry]

            # 🆕 Falls ein Schwellenwert für r_stem gesetzt ist, prüfen, ob der Baum sich verjüngen darf
            if self.min_r_stem is not None and x < self.min_r_stem:
                no_new_plants.append(0)  # Keine Verjüngung für diesen Baum
                continue

            no_per_plant = self.production_function(x, 0)
            if self.log:
                no_per_plant = int(10 ** no_per_plant - 1)
            no_new_plants.append(no_per_plant)

        return {"per_individual": no_new_plants}

