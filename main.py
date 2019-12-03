#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping

# prj = XMLtoProject(xml_tree=
#                    "tree_dynamics")

prj = XMLtoProject(xml_project_file="ProjectLib/testproject.xml")
time_stepper = TreeDynamicTimeStepping(prj)
prj.runProject(time_stepper)
