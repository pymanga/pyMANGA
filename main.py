#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ProjectLib import MangaProject
from TimeLoopLib import TreeDynamicTimeStepping

prj = MangaProject(xml_project_file="ProjectLib/testproject.xml")
time_stepper = TreeDynamicTimeStepping(prj)
prj.runProject(time_stepper)
