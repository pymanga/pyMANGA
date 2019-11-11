#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
## This script converts the tag documentation from the .md format to doxygen-
#  readable format. Additionally it is providing the correct linking of tags.
#  CAUTION: Only run script from this folder.

import os


def clear_folder(_dir):
    if os.path.exists(_dir):
        for the_file in os.listdir(_dir):
            file_path = os.path.join(_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                else:
                    clear_folder(file_path)
                    os.rmdir(file_path)
            except Exception as e:
                print(e)


md_parent = "./ProjectFile"
dox_parent = "./project_dox"
try:
    clear_folder(dox_parent)
    os.rmdir(dox_parent)
    print("Directory project_dox removed.")
except FileNotFoundError:
    print("Directory project_dox did not exist")
os.mkdir(dox_parent)
print("Directory project_dox created.")


def edit_dir(dox_parent, md_parent):
    all_files_in_folder = os.listdir(md_parent)
    i_files_in_folder = []
    c_files_in_folder = []
    t_files_in_folder = []
    s_files_in_folder = []
    folders_in_folder = []
    t_folders_in_folder = []

    for file in all_files_in_folder:
        if (file[-3:]) == ".md":
            case = file[0]
            if case == "i":
                i_files_in_folder.append(file)
            if case == "c":
                c_files_in_folder.append(file)
            if case == "t":
                t_files_in_folder.append(file)
            if case == "s":
                s_files_in_folder.append(file)
        elif "." not in file and file.islower():
            folders_in_folder.append(file)
        elif "." not in file and not file.islower():
            t_folders_in_folder.append(file)
        else:
            raise KeyError("File of type " + file.split(".")[-1] +
                           " not compatible with this script! " +
                           " Please use '.md' files for documentation.")

    for file in os.listdir(md_parent):
        if (file[-3:]) == ".md":
            case = file[0]
            tag_type = ""
            if case == "i":
                tag_type = "[input]"
            if case == "t":
                tag_type = "[tag]"
            if case == "c":
                tag_type = "[case]"
            if case == "s":
                tag_type = "[spec]"
            md_file = open(os.path.join(md_parent, file), "r")
            dox_filename = os.path.join(dox_parent, file[:-3])
            dox_file = open(dox_filename + ".dox", "w")

            page_name = dox_filename.strip("./").replace(
                "/" + case + "_", "__").replace("/", "__")
            dox_file.write("/*! \page " + page_name + " " + "&emsp;" +
                           tag_type + "" + file[2:-3] + "\n")
            for line in md_file.readlines():
                dox_file.write(line)
            if case == "i" or case == "c":
                if (len(folders_in_folder) + len(t_files_in_folder) +
                        len(s_files_in_folder)) > 0:
                    dox_file.write("# Required inputs: \n \n")
                    for subfolder in folders_in_folder:
                        submodule_path = os.path.join(dox_parent, subfolder)
                        subpage_name = submodule_path.strip("./").replace(
                            "/", "__") + "__" + subfolder
                        dox_file.write("- \subpage " + subpage_name + "\n")
                    for subfolder in t_files_in_folder:
                        subfolder = subfolder[2:-3]
                        submodule_path = os.path.join(dox_parent, subfolder)
                        subpage_name = submodule_path.strip("./").replace(
                            "/", "__")
                        dox_file.write("- \subpage " + subpage_name + "\n")

                    for subfolder in s_files_in_folder:
                        subfolder = subfolder[2:-3]
                        submodule_path = os.path.join(dox_parent, subfolder)
                        subpage_name = submodule_path.strip("./").replace(
                            "/", "__")
                        dox_file.write("- \subpage " + subpage_name + "\n")
                if len(t_folders_in_folder) > 0:
                    dox_file.write("\n # Possible cases: \n \n")
                    for subfolder in t_folders_in_folder:
                        submodule_path = os.path.join(dox_parent, subfolder)
                        subpage_name = submodule_path.strip("./").replace(
                            "/", "__") + "__" + subfolder
                        dox_file.write("- \subpage " + subpage_name + "\n")
            if case == "t":
                dox_file.write("# Available cases \n \n")
                for subfolder in t_folders_in_folder:
                    dox_file.write("- " + subfolder + "\n")

            dox_file.write("*/")
            dox_file.close()
            md_file.close()
        else:
            subdir = file
            os.mkdir(dox_parent + "/" + file)
            dox_child = os.path.join(dox_parent, subdir)
            md_child = os.path.join(md_parent, subdir)

            edit_dir(dox_child, md_child)


edit_dir(dox_parent, md_parent)
