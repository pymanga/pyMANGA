#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime

## This is an example file to start OGS with MANGA as boundary condition
# Directories and file names need to be updated

# Please specify the required directories below
ogs_project_folder = "OGS_input"
ogs_project_file = os.path.join(ogs_project_folder, "ogs_project.prj")

# Path to pyMANGA (only needed if OGS version provided by pyMANGA is used)
manga_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         os.pardir, os.pardir, os.pardir))

# Path to OGS.exe
ogs_exe = os.path.join(manga_dir, "ResourceLib/BelowGround/Individual/OGS/bin/ogs")


# Run OGS
# info: generate OGS output with 'all' instead of 'error'
t_start = datetime.datetime.now()
print("Running ogs...")
if not (os.system(ogs_exe + " " + ogs_project_file + " -o " +
                  ogs_project_folder + " -l error") == 0):
    raise ValueError("Ogs calculation failed!")
print("OGS-calculation done.")
t_end = datetime.datetime.now()
print("OGS finished at", t_end)
print("Total execution took", (t_end - t_start).seconds, "minutes")
