class Recruitment:
    """
    Constructor to initialize recruitment modules, by calling respective initialization methods.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        self.iniRecruitment(xml_args=xml_args)

    def iniRecruitment(self, xml_args):
        """
        Initialize selected recruitment module.
        Args:
            xml_args (lxml.etree._Element): recruitment module specifications from project file tags
        """
        case = xml_args.find("type").text
        module_dir = 'PopulationLib.Recruitment.'
        # Class needs to be imported on demand to avoid circular import
        from ProjectLib.Project import MangaProject
        self.recruitment = MangaProject.importModule(self=self,
                                                     module_name=case,
                                                     modul_dir=module_dir,
                                                     prj_args=xml_args)

    def updatePositions(self, positions):
        """
        Get plant positions from selected recruitment module.
        Args:
            number_of_plants (int or list of ints): total number of plants to be added to the system or a list of
            numbers to be added per existing plant.
            plants (dict): plant object, see ``pyMANGA.PopulationLib.PopManager.Plant``
        Returns:
            dict
        """
        return self.recruitment.updatePositions(positions)

    def setModelDomain(self, x1, x2, y1, y2):
        """
        Adds model domain boundaries to the object.
        Args:
            x1 (float): x-coordinate of left bottom border of grid
            x2 (float): x-coordinate of right bottom border of grid
            y1 (float): y-coordinate of left top border of grid
            y2 (float): y-coordinate of right top border of grid
        """
        self.recruitment.setModelDomain(x1, x2, y1, y2)
