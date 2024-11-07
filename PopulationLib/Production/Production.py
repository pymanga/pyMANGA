from ProjectLib import helpers as helpers


class Production:
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        print(">>> Production init")
        self.productionType(xml_args=xml_args)

    def productionType(self, xml_args):
        print(">>> Production productionType")

        case = xml_args.find("type").text
        module_dir = 'PopulationLib.Production.'
        # Class needs to be imported on demand to avoid circular import
        from ProjectLib.Project import MangaProject

        self.production = MangaProject.importModule(self=self,
                                                    module_name=case,
                                                    modul_dir=module_dir,
                                                    prj_args=xml_args)

    def getNumberSeeds(self, plants):
        print(">>> Production getNumberSeeds")
        return self.production.getNumberSeeds(plants)

    def setModelDomain(self, x1, x2, y1, y2):
        print(">>> Production setModelDomain")
        self.production.setModelDomain(x1, x2, y1, y2)
