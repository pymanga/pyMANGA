#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ProjectLib import helpers as helpers


class Dispersal:
    """
    Constructor to initialize dispersal modules, by calling respective initialization methods.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        print(">>> Dispersal init")
        self.dispersalTyp(xml_args=xml_args)

    def dispersalTyp(self, xml_args):
        print(">>> Dispersal productionType")
        case = xml_args.find("type").text
        module_dir = 'PopulationLib.Dispersal.'
        # Class needs to be imported on demand to avoid circular import
        from ProjectLib.Project import MangaProject

        self.dispersal = MangaProject.importModule(self=self,
                                                   module_name=case,
                                                   modul_dir=module_dir,
                                                   prj_args=xml_args)

    def getPositions(self, number_of_plants):
        return self.dispersal.getPositions(number_of_plants)

    def setModelDomain(self, x1, x2, y1, y2):
        print(">>> Dispersal setModelDomain")
        self.dispersal.setModelDomain(x1, x2, y1, y2)
