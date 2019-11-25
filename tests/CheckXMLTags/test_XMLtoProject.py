#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2019-Today
@author: marie-christin.wimmler@tu-dresden.de

Test ProjectLib/XMLtoProject.py

Actions that require an error message to appear
- no xml-input file/ xml-file not found
- type: xml - @Jasper: enough?
- empty xml-file - @Jasper: necessary?
- required xml-tree-elements are missing (e.g. tree_dynamics)
- required subelements are missing (e.g. aboveground_competition)
- required xml-tags are missing (e.g. type, species)
<<<<<<< HEAD
=======
- #wrong xml-text type (e.g. string instead of float)
>>>>>>> 4509c00... [tests] started xml unit testing

@ToDo: we need to specify required elements and tags - e.g. with DTD: each case requires DTD
"""

import unittest

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    parent = (path.split(path.dirname(path.abspath(__file__))))[0]
    parent = path.split(parent)[0]
    sys.path.append(parent)
from ProjectLib import XMLtoProject
from lxml import etree


class TestXMLToProject(unittest.TestCase):
    ## check if error is raised when file does not exist or file is not a file
    def test_file_exists(self):
        with self.assertRaisesRegex(OSError,
                                    'File is not a file or does not exist'):
            XMLtoProject(xml_project_file="tests/CheckXMLTags/notExistingFile")

    ## check if error is raised when project file has no ".xml" ending
    def test_file_extension(self):
        with self.assertRaisesRegex(ValueError, "File is not an xml file"):
            XMLtoProject(xml_project_file='error.txt')

    ## check if error is raised when required elements in MangaProject do not exist
    # required_elements: "tree_dynamics", "initial_population",
    #                    "tree_time_loop", "visualization"
    def test_required_elements_manga_project(self):
        required_elements = ["tree_dynamics", "initial_population",
                            "tree_time_loop", "visualization"]
        # build test tree
        manga_project = etree.Element("MangaProject")

        for element in required_elements:
            with self.assertRaisesRegex(
                KeyError, "Key '" + element +
                          "' is missing in project file"):
                XMLtoProject(xml_tree=manga_project).findChild(
                    parent=manga_project, key=element)

    ## check if error is raised when required elements in "tree_dynamics" do not exist
    # required elements: "aboveground_competition", "belowground_competition",
    #                    "tree_growth_and_death"
    # check if error is raised when required sub-elements do not exist
    # required sub element: "type"
    def test_required_elements_tree_dynamics(self):
        required_elements = ["aboveground_competition",
                             "belowground_competition",
                             "tree_growth_and_death"]
        # build test tree
        root = etree.Element("tree_dynamics")

        for element in required_elements:
            with self.assertRaisesRegex(
                KeyError, "Key '" + element +
                          "' is missing in project file"):
                XMLtoProject(xml_tree=root).findChild(
                    parent=root, key=element)

            sub_element = etree.SubElement(root, element)
            with self.assertRaisesRegex(
                KeyError, "Key '" + "type" +
                          "' is missing in project file"):
                XMLtoProject(xml_tree=root).findChild(
                    parent=sub_element, key="type")

    ## check if error is raised when required elements in "initial_population" do not exist
    # required element: "group"
    # required sub element: "name", "species", "distribution"
    def test_required_elements_initial_population(self):
        required_element = "group"
        required_sub_element = ["name", "species", "distribution"]

        root = etree.Element("initial_population")

        with self.assertRaisesRegex(
            KeyError, "Key '" + required_element +
                      "' is missing in project file"):
            XMLtoProject(xml_tree=root).findChild(
                parent=root, key=required_element)

        sub_element = etree.SubElement(root, "group")

        for sub_sub_element in required_sub_element:
            with self.assertRaisesRegex(
                KeyError, "Key '" + sub_sub_element +
                          "' is missing in project file"):
                XMLtoProject(xml_tree=root).findChild(
                    parent=sub_element, key=sub_sub_element)

    ## check if error is raised when required elements in "tree_time_loop" do not exist
    # required elements: "type", "t_start", "t_end"
    def test_required_elements_tree_time_loop(self):
        required_elements = ["type", "t_start", "t_end"]

        root = etree.Element("tree_time_loop")
        for element in required_elements:
            with self.assertRaisesRegex(
                KeyError, "Key '" + element +
                          "' is missing in project file"):
                XMLtoProject(xml_tree=root).findChild(
                    parent=root, key=element)

if __name__ == '__main__':
    unittest.main(verbosity=2)
# in tree_dynamics:
# above, below, growth
# type
# in pop.
# group
# name, species, distr.
# in time
# type, start, end

