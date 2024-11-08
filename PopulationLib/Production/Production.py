class Production:
    """
    Constructor to initialize production modules, by calling respective initialization methods.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): production module specifications from project file tags
        """
        self.iniProduction(xml_args=xml_args)

    def iniProduction(self, xml_args):
        """
        Initialize selected production module.
        Args:
            xml_args (lxml.etree._Element): dispersal module specifications from project file tags
        """
        case = xml_args.find("type").text
        module_dir = 'PopulationLib.Production.'
        # Class needs to be imported on demand to avoid circular import
        from ProjectLib.Project import MangaProject
        self.production = MangaProject.importModule(self=self,
                                                    module_name=case,
                                                    modul_dir=module_dir,
                                                    prj_args=xml_args)

    def getNumberSeeds(self, plants):
        """
        Get number of produced seeds/plants from selected production module.
        Args:
            plants (dict): plant object, see ``pyMANGA.PopulationLib.PopManager.Plant``
        Returns:
            int or list of ints
        """
        return self.production.getNumberSeeds(plants)

    def setModelDomain(self, x1, x2, y1, y2):
        """
        Adds model domain boundaries to the object.
        Args:
            x1 (float): x-coordinate of left bottom border of grid
            x2 (float): x-coordinate of right bottom border of grid
            y1 (float): y-coordinate of left top border of grid
            y2 (float): y-coordinate of right top border of grid
        """
        self.production.setModelDomain(x1, x2, y1, y2)
