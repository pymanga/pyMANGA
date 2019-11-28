#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeOutputLib.TreeOutput import TreeOutput
import os


## Output class. This class creates one file per tree at a defined location.
#  A line containing time, position, desired geometric measures and desired
#  parameters is written at every nth timestep.
class OneTreeOneFile(TreeOutput):
    ## Constructor of dummy objects in order to drop output
    #  @param args xml element parsed from project to this constructor.
    def __init__(self, args):
        ## Directory, where output is saved. Please make sure it exists and is
        #  empty.
        self.output_dir = self.checkRequiredKey("output_dir", args)
        ## N-timesteps between two outputs
        self.output_each_nth_timestep = int(
            self.checkRequiredKey("output_each_nth_timestep", args))
        ## Geometric measures included in output
        self.geometry_outputs = []
        ## Parameters included in output
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

    ## This function checks if a key exists and if its text content is empty.
    #  Raises key-errors, if the key is not properly defined.
    #  @param key Name of the key to be checked
    #  @param args args parsed from project. Xml-element
    def checkRequiredKey(self, key, args):
        tmp = args.find(key)
        if tmp == None:
            raise KeyError("Required key '" + key + "' in project file at " +
                           "position MangaProject__tree_output is missing.")
        elif tmp.text.strip() == "":
            raise KeyError("Key '" + key + "' in project file at position " +
                           "MangaProject__tree_output needs to be specified.")
        return tmp.text
