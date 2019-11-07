#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from ProjectLib import MangaProject
    from TimeLoopLib import TreeDynamicTimeStepping

prj = MangaProject(xml_project_file="ProjectLib/testproject.xml")
time_stepper = TreeDynamicTimeStepping.TreeDynamicTimeStepping(prj)
prj.runProject(time_stepper)
