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
- #wrong xml-text type (e.g. string instead of float)

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
    def test_file_exists(self):
        # check if error is raised when file does not exist or file is not a file
        with self.assertRaisesRegex(OSError,
                                    'File is not a file or does not exist'):
            XMLtoProject(xml_project_file="tests/CheckXMLTags/notExistingFile")

    def test_file_extension(self):
        # check if error is raised when project file has no ".xml" ending
        with self.assertRaisesRegex(ValueError, "File is not an xml file"):
            XMLtoProject(xml_project_file='error.txt')

    def test_elements_exist(self):
        from lxml import etree

        # check if error is raised when required elements do not exist
        requiredElements = [
            "tree_dynamics", "initial_population", "tree_time_loop"
        ]

        # build test tree
        manga_project = etree.Element("MangaProject")
        element = etree.SubElement(manga_project,
                                   requiredElements[1])  # "tree_dynamics")
        etree.SubElement(element, "test")
        print("MangaProject \n", etree.dump(manga_project))

        print("TYPE:  ", type(manga_project))

        for tag in manga_project.iter():
            print(tag, tag.attrib)

        # test for "tree_dynamics"
        with self.assertRaisesRegex(
                KeyError, "Key '" + requiredElements[0] +
                "' is missing in project file"):
            XMLtoProject(xml_tree=manga_project).findChild(
                parent=manga_project, key="tree_dynamics")


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
