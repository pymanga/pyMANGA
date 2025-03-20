class Dispersal:
    """
    Constructor to initialize dispersal modules, by calling respective initialization methods.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        self.iniDispersal(xml_args=xml_args)

    def iniDispersal(self, xml_args):
        """
        Initialize selected dispersal module.
        Args:
            xml_args (lxml.etree._Element): dispersal module specifications from project file tags
        """
        case = xml_args.find("type").text
        module_dir = 'PopulationLib.Dispersal.'
        # Class needs to be imported on demand to avoid circular import
        from ProjectLib.Project import MangaProject
        self.dispersal = MangaProject.importModule(self=self,
                                                   module_name=case,
                                                   modul_dir=module_dir,
                                                   prj_args=xml_args)

    def getPositions(self, number_of_plants, plants):
        """
        Get plant positions from selected dispersal module.
        Args:
            number_of_plants (int or list of ints): total number of plants to be added to the system or a list of
            numbers to be added per existing plant.
            plants (dict): plant object, see ``pyMANGA.PopulationLib.PopManager.Plant``
        Returns:
            dict
        """
        return self.dispersal.getPositions(number_of_plants, plants)

    def setModelDomain(self, x1, x2, y1, y2):
        """
        Adds model domain boundaries to the object.
        Args:
            x1 (float): x-coordinate of left bottom border of grid
            x2 (float): x-coordinate of right bottom border of grid
            y1 (float): y-coordinate of left top border of grid
            y2 (float): y-coordinate of right top border of grid
        """
        self.dispersal.setModelDomain(x1, x2, y1, y2)
