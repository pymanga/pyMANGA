#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os
import datetime

## This is an alternative version of runModel.py to start OGS with MANGA as boundary condition.
# Only use this if the original version does not work for you. Please make sure all required packages are installed.
# Directories and file names need to be updated. Refer to runModel.py for commented code.

ogs_project_folder = "OGS_input"
ogs_project_file = "ogs_project.prj"
ogs_project_file_path = os.path.join(ogs_project_folder, ogs_project_file)

manga_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         os.pardir, os.pardir, os.pardir))

ogs_exe = os.path.join(manga_dir, "ResourceLib/BelowGround/Individual/OGS/bin/ogs")

arguments = [ogs_project_file_path, "-o", ogs_project_folder, "-l", "error"]

t_start = datetime.datetime.now()
print("Running ogs...")
try:
    subprocess.run([ogs_exe] + arguments, check = True)
    print("OGS-calculation done.")
except subprocess.CalledProcessError:
    print("OGS calculation failed!")
    exit()
t_end = datetime.datetime.now()
print("OGS finished at", t_end)
print("Total execution took", (t_end - t_start).seconds, "minutes")