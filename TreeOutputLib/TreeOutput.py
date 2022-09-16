#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import os

## Parent class for tree output
class TreeOutput:
    ## Constructor for tree output calling different constructors depending on
    #  choosen case.

    def __init__(self, args):
        ## Directory, where output is saved. Please make sure it exists and is
        #  empty.
        self.output_dir = self.checkRequiredKey("output_dir", args)
        ## N-timesteps between two outputs
        self.output_each_nth_timestep = args.find("output_each_nth_timestep")
        if self.output_each_nth_timestep is not None:
            self.output_each_nth_timestep = int(
                self.checkRequiredKey("output_each_nth_timestep", args))
        else:
            self.output_each_nth_timestep = 1
        ## Check if overwrite of previous output is allowed
        allow_previous_output = args.find("allow_previous_output")
        if allow_previous_output is not None:
            allow_previous_output = eval(allow_previous_output.text)
        else:
            allow_previous_output = False
        ## Check if specific timesteps for output are defined
        output_times = args.find("output_times")
        if output_times is not None:
            self.output_times = eval(output_times.text)
            print(self.output_times)
        else:
            self.output_times = None

        ## Geometric measures included in output
        self.geometry_outputs = []
        ## Parameters included in output
        self.parameter_outputs = []
        ## Parameters included in output
        self.growth_outputs = []
        ## Network information included in output
        self.network_outputs = []
        ## Counter for output generation
        self._output_counter = 0
        for key in args.iterchildren("geometry_output"):
            self.geometry_outputs.append(key.text.strip())
        for key in args.iterchildren("parameter_output"):
            self.parameter_outputs.append(key.text.strip())
        for key in args.iterchildren("growth_output"):
            self.growth_outputs.append(key.text.strip())
        for key in args.iterchildren("network_output"):
            self.network_outputs.append(key.text.strip())
        try:
            dir_files = len(os.listdir(self.output_dir))
        except FileNotFoundError:
            print("No such directory: '" + self.output_dir +
                  "' as defined in the project file." +
                  " Creating directory...")
            os.mkdir(self.output_dir)
            dir_files = 0
        if (dir_files > 0 and allow_previous_output == False):
            raise ValueError("Output directory '" + self.output_dir +
                             "' is not empty.")

        self.it_is_output_time = False
        print(
            "Output to '" + os.path.join(os.getcwd(), self.output_dir) +
            "' of tree positions, the " + "parameters ",
            self.parameter_outputs, " and geometric" + " measures ",
            self.geometry_outputs, " at every " +
            str(self.output_each_nth_timestep) + " timesteps initialized.")

    ## Constructor for no output generation.
    def iniNONE(self, args):
        from .NONE import NONE
        self.output = NONE(args)

    ## Constructor for output which generates one file per tree.
    def iniOneTreeOneFile(self, args):
        from .OneTreeOneFile import OneTreeOneFile
        self.output = OneTreeOneFile(args)

    ## Constructor for output which generates one file per timestep.
    def iniOneTimestepOneFile(self, args):
        from .OneTimestepOneFile import OneTimestepOneFile
        self.output = OneTimestepOneFile(args)

    ## Constructor for output which generates one file per group per timestep.
    def iniOneTimestepOneFilePerGroup(self, args):
        from .OneTimestepOneFilePerGroup import OneTimestepOneFilePerGroup
        self.output = OneTimestepOneFilePerGroup(args)

    ## Constructor for output which generates one file per simulation.
    def iniOneFile(self, args):
        from .OneFile import OneFile
        self.output = OneFile(args)

    ## Returns output type:
    def getOutputType(self):
        return self.case

    ## This function returns the output directory
    def getOutputDir(self):
        return self.output_dir

    def addSelectedHeadings(self, string, delimiter):
        for geometry_output in self.geometry_outputs:
            string += delimiter + geometry_output
        for parameter_output in self.parameter_outputs:
            string += delimiter + parameter_output
        for growth_output in self.growth_outputs:
            string += delimiter + growth_output
        for network_output in self.network_outputs:
            string += delimiter + network_output
        return string

    def addSelectedOutputs(self, tree, string, delimiter, growth_information):
        if len(self.geometry_outputs) > 0:
            geometry = tree.getGeometry()
            for geometry_output in self.geometry_outputs:
                string += delimiter + str(geometry[geometry_output])
        if len(self.parameter_outputs) > 0:
            parameter = tree.getParameter()
            for parameter_output in self.parameter_outputs:
                string += delimiter + str(parameter[parameter_output])
        if len(self.growth_outputs) > 0:
            for growth_output_key in self.growth_outputs:
                try:
                    string += delimiter + str(
                        growth_information[growth_output_key])
                except KeyError:
                    growth_information[growth_output_key] = "NaN"
                    string += delimiter + str(
                        growth_information[growth_output_key])
                    print("Key " + growth_output_key +
                          " might be not available in growth " + "concept!" +
                          " Please read growth concept documentation.")
        if len(self.network_outputs) > 0:
            network = tree.getNetwork()
            for network_output in self.network_outputs:
                string += delimiter + str(network[network_output])
        return string

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

    ## Writes output to predefined folder
    #  For each timestep a file is created throughout the simulation.
    #  This function is only able to work, if the output directory exists and
    #  is empty at the begin of the model run
    def writeOutput(self, tree_groups, time):
        self._output_counter = (self._output_counter %
                                self.output_each_nth_timestep)

        if self.output_times is not None:
            self.it_is_output_time = (time in self.output_times)
        if not self.it_is_output_time:
            self.it_is_output_time = (self._output_counter == 0)

        if self.it_is_output_time:
            self.outputContent(tree_groups, time)
            self.it_is_output_time = False
        self._output_counter += 1

    def outputContent(self, tree_groups, time):
        pass
