#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeOutputLib.TreeOutput import TreeOutput
import os


## Output class. This class creates one file per timestep at a defined
#  location. A line containing time, position, desired geometric measures and
#  desired parameters is written at every nth timestep.
class OneTimestepOneFile(TreeOutput):
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
        ## Parameters included in output
        self.growth_outputs = []
        ## Counter for output generation
        self._output_counter = 0
        for key in args.iterchildren("geometry_output"):
            self.geometry_outputs.append(key.text.strip())
        for key in args.iterchildren("parameter_output"):
            self.parameter_outputs.append(key.text.strip())
        for key in args.iterchildren("growth_output"):
            self.growth_outputs.append(key.text.strip())
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

    ## Writes output to predefined folder
    #  For each timestep a file is created throughout the simulation.
    #  This function is only able to work, if the output directory exists and
    #  is empty at the begin of the model run
    def writeOutput(self, tree_groups, time):
        self._output_counter = (self._output_counter %
                                self.output_each_nth_timestep)
        filename = ("Population_t_%012.1f" % (time) + ".csv")
        file = open(self.output_dir + filename, "w")
        string = ""
        string += "tree,\t time,\t x,\t y"
        for geometry_output in self.geometry_outputs:
            string += ",\t" + geometry_output
        for parameter_output in self.parameter_outputs:
            string += ",\t" + parameter_output
        for growth_output in self.growth_outputs:
            string += ",\t" + growth_output
        string += "\n"
        file.write(string)
        if self._output_counter == 0:
            for group_name, tree_group in tree_groups.items():
                for tree in tree_group.getTrees():
                    growth_information = tree.getGrowthConceptInformation()
                    string = ""
                    string += (group_name + "_" + "%09.0d" % (tree.getId()) +
                               ",\t" + str(time) + ",\t" + str(tree.x) +
                               ",\t" + str(tree.y))
                    if (len(self.geometry_outputs) > 0):
                        geometry = tree.getGeometry()
                        for geometry_output in self.geometry_outputs:
                            string += ",\t" + str(geometry[geometry_output])
                    if (len(self.parameter_outputs) > 0):
                        parameter = tree.getParameter()
                        for parameter_output in self.parameter_outputs:
                            string += ",\t" + str(parameter[parameter_output])
                    if (len(growth_information) > 0):
                        for growth_output_key in self.growth_outputs:
                            try:
                                string += ",\t" + str(
                                    growth_information[growth_output_key])
                            except KeyError:
                                raise KeyError(
                                    "Key " + growth_output_key +
                                    " not available in growth concept!" +
                                    " Please read growth concept documentation."
                                )
                    string += "\n"
                    file.write(string)
        file.close()
        self._output_counter += 1

    ## This function checks if a key exists and if its text content is empty.
    #  Raises key-errors, if the key is not properly defined.
    #  @param key Name of the key to be checked
    #  @param args args parsed from project. Xml-element
    def checkRequiredKey(self, key, args):
        tmp = args.find(key)
        if tmp is None:
            raise KeyError("Required key '" + key + "' in project file at " +
                           "position MangaProject__tree_output is missing.")
        elif tmp.text.strip() == "":
            raise KeyError("Key '" + key + "' in project file at position " +
                           "MangaProject__tree_output needs to be specified.")
        return tmp.text

    ## This function returns the output directory
    def getOutputDir(self):
        return self.output_dir