#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
from os import path
import os

## This is an example file to start OGS with MANGA as boundary condition
# Directories and file names need to be updated

# Please specify the required directories below
manga_dir = "/path/to/pyMANGA/directory/"
setup_dir = "path/to/external_setup/"

ogs_exe = os.path.join(manga_dir, "ResourceLib", "BelowGround", "Individual",
                       "OGS", "bin", "ogs")

ogs_project_folder = os.path.join(manga_dir, setup_dir)

ogs_project_file = os.path.join(ogs_project_folder, "testmodel.prj")

# Run OGS
# info: generate OGS output with 'all' instead of 'error'
print("Running ogs...")
if not (os.system(ogs_exe + " " + ogs_project_file + " -o " +
                  ogs_project_folder + " -l error") == 0):
    raise ValueError("Ogs calculation failed!")
print("OGS-calculation done.")
