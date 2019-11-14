#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ProjectLib import Project
from TimeLoopLib import TreeDynamicTimeStepping

prj = Project.MangaProject(xml_project_file="ProjectLib/testproject.xml")
time_stepper = TreeDynamicTimeStepping.TreeDynamicTimeStepping(prj)
prj.runProject(time_stepper)
