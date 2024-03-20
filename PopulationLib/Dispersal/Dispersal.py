#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np


class Dispersal:
    """
    Constructor to initialize dispersal modules, by calling respective initialization methods.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        self.xml_args = xml_args
        distribution = self.xml_args.find("distribution")
        distribution_type = distribution.find("type").text

        if distribution_type == "Random":
            from .Random import Random as BC
        elif distribution_type == "FromFile":
            from .FromFile import FromFile as BC
        else:
            raise KeyError("Population initialisation of type " +
                           distribution_type + " not implemented!")
        print("Population: " + distribution_type + ".")

        self.dispersal = BC(self.xml_args)
        tags = self.dispersal.getTags()
        self.getInputParameters(**tags)

    def getPlantAttributes(self, initial_group):
        """
        Return positions and geometries of plants.
        Args:
            initial_group (bool): indicate whether these are the first plants in the system (initial population).
        Returns:
            dict, np.array
        """
        positions, geometry = self.dispersal.getPlantAttributes(initial_group=initial_group)
        return positions, geometry

    def getInputParameters(self, **tags):
        """
        Read module tags from project file.
        Args:
            tags (dict): dictionary containing tags found in the project file as well as required and optional tags of
            the module under consideration.
        """
        try:
            prj_file_tags = tags["prj_file"]
        except KeyError:
            prj_file_tags = []
            print("WARNING: Module attributes are missing.")
        try:
            required_tags = tags["required"]
        except KeyError:
            required_tags = []
        try:
            optional_tags = tags["optional"]
        except KeyError:
            optional_tags = []

        for arg in prj_file_tags.iterdescendants():
            tag = arg.tag
            for i in range(0, len(required_tags)):
                if tag == required_tags[i]:
                    try:
                        super(Dispersal, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(Dispersal, self).__setattr__(tag, str(arg.text))
            try:
                required_tags.remove(tag)
            except ValueError:
                pass

            for i in range(0, len(optional_tags)):
                if tag == optional_tags[i]:
                    try:
                        super(Dispersal, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(Dispersal, self).__setattr__(tag, str(arg.text))

        if len(required_tags) > 0:
            string = ""
            for tag in required_tags:
                string += tag + " "
            raise KeyError(
                "Missing input parameters (in project file) for population module initialisation: " + string)

        try:
            self.n_recruitment_per_step = int(self.n_recruitment_per_step)
        except AttributeError:
            self.n_recruitment_per_step = 0

        try:
            self.n_individuals = int(self.n_individuals)
        except AttributeError:
            pass

        self.l_x = self.x_2 - self.x_1
        self.l_y = self.y_2 - self.y_1

        # Transfer attribute dictionary to respective dispersal module
        self.dispersal.__dict__.update(self.__dict__)
