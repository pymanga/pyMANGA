#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np


class ResourceModel:
    """
    Parent class for all resource modules.
    """

    def getAbovegroundResources(self):
        """
        Get above-ground resource values
        Returns:
            vector with floats
        """
        return self.aboveground_resources

    def getBelowgroundResources(self):
        """
        Get below-ground resource values
        Returns:
            vector with floats
        """
        return self.belowground_resources

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepare next time step by initializing relevant variables.
        Args:
            t_ini (int): start of current time step in seconds
            t_end (int): end of current time step in seconds
        """
        pass

    def addPlant(self, plant):
        """
        Add each plant and its relevant geometry and parameters to the object to
        be used in the next time step.
        Args:
            plant (dict): tree object
        """
        pass

    def getInputParameters(self, **tags):
        """
        Read module tags from project file.
        Args:
            tags (dict): dictionary containing tags found in the project file as well as required and optional tags of
            the module under consideration.
        """
        try:
            prj_file_tags = tags["prj_file"]
        except KeyError:
            prj_file_tags = []
            print("WARNING: Module attributes are missing.")
        try:
            required_tags = tags["required"]
        except KeyError:
            required_tags = []
        try:
            optional_tags = tags["optional"]
        except KeyError:
            optional_tags = []

        for arg in prj_file_tags.iterdescendants():
            tag = arg.tag
            for i in range(0, len(required_tags)):
                if tag == required_tags[i]:
                    try:
                        super(ResourceModel, self).__setattr__(tag, float(eval(arg.text)))
                    except (ValueError, NameError, SyntaxError):
                        super(ResourceModel, self).__setattr__(tag, str(arg.text))
            try:
                required_tags.remove(tag)
            except ValueError:
                pass

            for i in range(0, len(optional_tags)):
                if tag == optional_tags[i]:
                    try:
                        super(ResourceModel, self).__setattr__(tag, float(eval(arg.text)))
                    except (ValueError, NameError, SyntaxError):
                        super(ResourceModel, self).__setattr__(tag, str(arg.text))

        if len(required_tags) > 0:
            string = ""
            for tag in required_tags:
                string += tag + " "
            raise KeyError(
                "Missing input parameters (in project file) for resource module initialisation: " + string)

    def makeGrid(self):
        """
        Create grid with defined size and resolution
        Sets:
            multiple float
        """
        l_x = self.x_2 - self.x_1
        l_y = self.y_2 - self.y_1
        x_step = l_x / self.x_resolution
        y_step = l_y / self.y_resolution
        xe = np.linspace(self.x_1 + x_step / 2.,
                         self.x_2 - x_step / 2.,
                         int(self.x_resolution),
                         endpoint=True)
        ye = np.linspace(self.y_1 + y_step / 2.,
                         self.y_2 - y_step / 2.,
                         int(self.y_resolution),
                         endpoint=True)
        self.my_grid = np.meshgrid(xe, ye)
        self._mesh_size = np.maximum(x_step, y_step)
        self.cell_area = x_step * y_step

    def makeBoolFromArg(self, var_name):
        """
        Transform input variable in boolean, excepting various options to indicate True.
        Args:
            var_name (string): name of variable
        Returns:
            bool
        """
        if hasattr(self, var_name):
            var = str(getattr(self, var_name))
            if var.lower() in ['true', '1', '1.0', 't', 'y', 'yes']:
                var = True
            else:
                var = False
        else:
            var = False
        return var
