#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from lxml import etree
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    parent = (path.split(path.dirname(path.abspath(__file__))))[0]
    parent = path.split(parent)[0]
    sys.path.append(parent)
from ProjectLib import XMLtoProject

# =============================================================================
# KeyError = alles in <>, return from element.key
# =============================================================================


def checkForEmptyTreeError(tree):
    try:
        XMLtoProject(xml_tree=tree)
    except AttributeError:
        if not tree.getroot() == None:
            raise KeyError("Empty tree error for non empty tree.")


def checkKeyErrorForMissingKey(tree, key):
    try:
        XMLtoProject()
    except KeyError:
        if tree.find(key) != (None):
            raise KeyError("Required key '" + key + "' " +
                           "not correctly checked.")


def checkCorrectAttributeError(tree, tag, key):
    #try:

    XMLtoProject(xml_tree=tree)


#except AttributeError:
#    print(tag.find(key))
#    if tag.find(key) != None:
#        raise AttributeError("Required tag 'type' for tag " + tag.key  +
#                             "not correctly checked.")


def checkCorrectKeyErrorForWrongKey(args, tag, key, test):
    try:
        XMLtoProject()

    except KeyError:
        if tag.find(key) == test:
            raise KeyError("Case not correctly checked.")


def checkForProjectArgExisting(args, search):
    try:
        XMLtoProject()

    except KeyError:
        if search in (args.keys()):
            raise KeyError("Key not correctly checked.")


# create empty tree
tree = etree.ElementTree()
checkForEmptyTreeError(tree)

# add root
root = etree.Element("MangaProject")
root.text = ""
tree = etree.ElementTree(root)

# check if tree_dynamics tag/ key exists
# XMLtoProject(xml_tree = tree)
checkKeyErrorForMissingKey(tree, "tree_dynamics")

#
etree.SubElement(root, "tree_dynamics")
XMLtoProject(xml_tree=tree)

tree_dynamics = ["aboveground_competition", "belowground_competition"]

#if not tree.getroot(): print("True")
# =============================================================================
#
# for text in tree_dynamics:
#     XMLtoProject(xml_tree = tree)
# =============================================================================
# =============================================================================
#     checkForProjectArgExisting( tree, text)
#
#     print(args)
#     print(tag)
#     print(tag.find("type"))
#     checkCorrectAttributeError(args, tag, "type")
#     etree.SubElement(tag, "type")
#     checkCorrectKeyErrorForMissingKey(prj, args, tag, "type")
#     tag.find("type").text = "Simple"
#
#
#     checkCorrectKeyErrorForWrongKey(prj, args, tag, "type", "SimpleTest")
#     tag.find("type").text = "SimpleTest"
#
#     #print(tag.find("type").text)
#
#
# =============================================================================
