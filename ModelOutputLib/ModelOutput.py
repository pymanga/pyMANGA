#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class ModelOutput:
    """
    Parent class for all model output modules.
    """

    def __init__(self, args, time):
        """
        Get relevant tags from project file and create output directory and/or file.
        Check if output file exists and can be overwritten.
        Args:
            args: module specifications from project file tags
        """
        ## Directory, where output is saved. Please make sure it is empty
        #  or set allow_previous_output to true
        self.output_dir = self.checkRequiredKey("output_dir", args)
        ## N-timesteps between two outputs
        self.output_each_nth_timestep = args.find("output_each_nth_timestep")
        if self.output_each_nth_timestep is not None:
            self.output_each_nth_timestep = int(
                self.checkRequiredKey("output_each_nth_timestep", args))
        else:
            self.output_each_nth_timestep = None
        ## Check if overwrite of previous output is allowed
        allow_previous_output = args.find("allow_previous_output")
        if allow_previous_output is not None:
            allow_previous_output = eval(allow_previous_output.text)
        else:
            allow_previous_output = False
        ## Check if specific timesteps for output are defined
        self.output_times = args.find("output_times")
        if self.output_times is not None:
            self.output_times = eval(self.output_times.text)
        self.output_time_range = args.find("output_time_range")
        if self.output_time_range is not None:
            self.output_time_range = eval(self.output_time_range.text)
            if len(self.output_time_range) != 2:
                raise ValueError("The tag \'<output_time_range>\' in the xml file"
                                 " caused an error. Please check your input!")

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

        self._it_is_output_time = True
        print(
            "Output to '" + os.path.join(os.getcwd(), self.output_dir) +
            "' of plant positions, the " + "parameters ",
            self.parameter_outputs, " and geometric" + " measures ",
            self.geometry_outputs, " at every " +
            str(self.output_each_nth_timestep) + " timesteps initialized.")

    def getOutputType(self):
        """
        Get selected output type.
        Returns:
            string
        """
        return self.case

    def getOutputDir(self):
        """
        Get output directory.
        Returns:
            string
        """
        return self.output_dir

    def addSelectedHeadings(self, string, delimiter):
        """
        Collect selected output parameters to create a file header.
        Args:
            string (string): beginning of header, e.g. plant ID
            delimiter (string): delimiter to be used in csv file
        Returns:
            string
        """
        for geometry_output in self.geometry_outputs:
            string += delimiter + geometry_output
        for parameter_output in self.parameter_outputs:
            string += delimiter + parameter_output
        for growth_output in self.growth_outputs:
            string += delimiter + growth_output
        for network_output in self.network_outputs:
            string += delimiter + network_output
        return string

    def addSelectedOutputs(self, plant, string, delimiter, growth_information):
        """
        Collect values of selected output parameters to fill output file.
        Args:
            plant (dict): plant object
            string (string): beginning of line, e.g. plant ID
            delimiter (string): delimiter to be used in csv file
            growth_information (dict): dictionary containing growth information of the respective plant
        Returns:
            string
        """
        if len(self.geometry_outputs) > 0:
            geometry = plant.getGeometry()
            for geometry_output in self.geometry_outputs:
                string += delimiter + str(geometry[geometry_output])
        if len(self.parameter_outputs) > 0:
            parameter = plant.getParameter()
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
                    # print("Key " + growth_output_key +
                    #       " might be not available in growth " + "concept!" +
                    #       " Please read growth concept documentation.")
        if len(self.network_outputs) > 0:
            network = plant.getNetwork()
            for network_output in self.network_outputs:
                string += delimiter + str(network[network_output])
        return string

    def checkRequiredKey(self, key, args):
        """
        Check whether a key (i.e., required element) is specified in project file.
        Args:
            key (string): name of key to be checked
            args (lxml.etree._Element): module specifications from project file tags
        Returns:
            string or raise KeyError
        """
        tmp = args.find(key)
        if tmp is None:
            raise KeyError("Required key '" + key + "' in project file at " +
                           "position MangaProject_model_output is missing.")
        elif tmp.text.strip() == "":
            raise KeyError("Key '" + key + "' in project file at position " +
                           "MangaProject_model_output needs to be specified.")
        return tmp.text

    def writeOutput(self, plant_groups, time, force_output=False, group_died=False):
        """
        Check whether it is output time and call the output method of the selected module.
        Args:
            plant_groups (dict): plant groups object
            time (float): current time step
            force_output (bool): indicate whether writing output is forced
            group_died (bool): indicate whether a whole plant group died
        """
        self._it_is_output_time = False
        self.cond1, self.cond2, self.cond3 = False, False, False
        if self.output_each_nth_timestep is not None:
            self._output_counter = (self._output_counter %
                                    self.output_each_nth_timestep)
            self.cond1 = (self._output_counter == 0)

        if self.output_times is not None:
            self.cond2 = (time in self.output_times)
        if self.output_time_range is not None:
            self.cond3 = (self.output_time_range[0] <=
                                       time <=
                                       self.output_time_range[1])
        if any([self.cond1, self.cond2, self.cond3]):
            self._it_is_output_time = True

        if force_output or group_died:
            self._it_is_output_time = True

        if self._it_is_output_time:
            self.outputContent(plant_groups=plant_groups,
                               time=time,
                               group_died=group_died)
        self._output_counter += 1

    def outputContent(self, plant_groups, time, **kwargs):
        """
        Write output content to file, i.e., values of selected parameters.
        Args:
            plant_groups (dict): plant groups object
            time (float): current time step
            **kwargs (dict): named arguments
        """
        pass
