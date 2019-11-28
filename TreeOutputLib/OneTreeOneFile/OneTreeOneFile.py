#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeOutputLib.TreeOutput import TreeOutput
import os


class OneTreeOneFile(TreeOutput):
    ## Constructor of dummy objects in order to drop output
    def __init__(self, args):
        self.output_dir = self.checkRequiredKey("output_dir", args)
        self.output_each_nth_timestep = int(
            self.checkRequiredKey("output_each_nth_timestep", args))
        self.geometry_outputs = []
        self.parameter_outputs = []
        for key in args.iterchildren("geometry_output"):
            self.geometry_outputs.append(key.text.strip())
        for key in args.iterchildren("parameter_output"):
            self.parameter_outputs.append(key.text.strip())
        try:
            dir_files = len(os.listdir(self.output_dir))
        except FileNotFoundError:
            raise FileNotFoundError(
                "[Errno 2] No such directory: '" + self.output_dir +
                "' as defined in the project file." +
                " Please make sure your output directory exists!")
        if dir_files > 0:
            raise ValueError("Output directory '" + self.output_dir +
                             "' is not empty.")
        print(
            "Output to '" + self.output_dir + "' of tree positions, the " +
            "parameters ", self.parameter_outputs,
            " and geometric" + " measures ", self.geometry_outputs,
            " at every " + str(self.output_each_nth_timestep) +
            " timesteps initialized.")

    def writeOutput(self, tree_groups, time):
        for group in tree_groups:
            for tree in group:
                print("")

    def checkRequiredKey(self, key, args):
        tmp = args.find(key)
        if tmp == None:
            raise KeyError("Required key '" + key + "' in project file at " +
                           "position MangaProject__tree_output is missing.")
        elif tmp.text.strip() == "":
            raise KeyError("Key '" + key + "' in project file at position " +
                           "MangaProject__tree_output needs to be specified.")
        return tmp.text
