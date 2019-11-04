#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ProjectLib import Project

prj = Project.MangaProject(xml_project_file="ProjectLib/testproject.xml")
prj.runProject()
