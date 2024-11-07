from ProjectLib import helpers as helpers


class InitialPop:
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        print(">>> InitialPop init")
        self.initialPopulation(xml_args=xml_args)

    def initialPopulation(self, xml_args):
        print(">>> InitialPop initialPopulation")

        case = xml_args.find("type").text
        module_dir = 'PopulationLib.InitialPop.'
        # Class needs to be imported on demand to avoid circular import
        from ProjectLib.Project import MangaProject

        self.initial_population = MangaProject.importModule(self=self,
                                                            module_name=case,
                                                            modul_dir=module_dir,
                                                            prj_args=xml_args)

    def setModelDomain(self, x1, x2, y1, y2):
        print(">>> InitialPop setModelDomain")
        self.initial_population.setModelDomain(x1, x2, y1, y2)

    def getPlantAttributes(self):
        print(">>> InitialPop getPlantAttributes")

        positions, geometry, network = self.initial_population.getPlantAttributes()
        return positions, geometry, network

