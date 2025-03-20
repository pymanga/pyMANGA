#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


class Dispersal_v310:
    """
    Constructor to initialize dispersal modules, by calling respective initialization methods.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        self.xml_args = xml_args
        distribution = self.xml_args.find("distribution")
        distribution_type = distribution.find("type").text

        if distribution_type == "Random":
            from .Random import Random as BC
        elif distribution_type == "FromFile":
            from .FromFile import FromFile as BC
        else:
            raise KeyError("Population initialisation of type " +
                           distribution_type + " not implemented!")
        print("Population: " + distribution_type + ".")

        self.dispersal = BC(self.xml_args)
        tags = {
            "prj_file": self.xml_args,
            "required": ["domain", "x_1", "x_2", "y_1", "y_2"],
            "optional": ["n_recruitment_per_step",
                         "weight_formula", "weight_file", "x_res", "y_res"]
        }
        tags = self.dispersal.getTags(tags)
        self.getInputParameters(**tags)

        if hasattr(self, "weight_file"):
            self.iniWeightsFile()
        elif hasattr(self, "weight_formula"):
            self.iniWeightsFormula()

    def iniWeightsFormula(self):
        """
        Create map (grid) with weights indicating suitability for recruitment.
        Map is initialized at the beginning of the simulation for each plant group.
        Weights should range between 0 (not suitable) and 1 (suitable).
        """
        if not hasattr(self, "x_res"):
            self.x_res = self.x_2 - self.x_1
            print("> Set dispersal parameter 'x_res' to default:", self.x_res)
        if not hasattr(self, "y_res"):
            self.y_res = self.y_2 - self.y_1
            print("> Set dispersal parameter 'y_res' to default:", self.y_res)

        # Cell dimensions
        self.dispersal.x_r = 1 / (self.x_res / self.l_x)
        self.dispersal.y_r = 1 / (self.y_res / self.l_y)

        # Create xy coordinates of all nodes in the grid
        x, y = np.linspace(self.dispersal.x_r, self.l_x, int(self.x_res)),\
            np.linspace(self.dispersal.y_r, self.l_y, int(self.y_res))
        self.dispersal.grid_x, self.dispersal.grid_y = self.expand_grid(x, y)

        # Calculate weights based on function
        weighting_function = self.string_to_function(self.weight_formula)
        self.dispersal.weights = weighting_function(self.dispersal.grid_x, self.dispersal.grid_y)

        if np.max(self.dispersal.weights) > 1:
            print("WARNING: dispersal weights are > 1.")

    def iniWeightsFile(self):
        """
        Read grid and weights from csv-file.
        Returns:

        """
        try:
            weight_file = pd.read_csv(self.weight_file, delimiter=";|,|\t", engine='python')
        except pd.errors.ParserError:
            weight_file = pd.read_csv(self.weight_file, delimiter=";", engine='python')

        if not set(['x', 'y', 'weight']).issubset(weight_file.columns):
            print("Error: Wrong column names in weight map file (population > distribution > weight_file).\n"
                  "Required column names: x, y, weight (without quotes).")
            exit()

        self.dispersal.grid_x = weight_file['x'].to_numpy()
        self.dispersal.grid_y = weight_file['y'].to_numpy()
        self.dispersal.weights = weight_file['weight'].to_numpy()

        self.dispersal.x_r = np.mean(np.diff(weight_file['x'].unique()))
        self.dispersal.y_r = np.mean(np.diff(weight_file['y'].unique()))

        if np.max(self.dispersal.weights) > 1:
            print("WARNING: dispersal weights are > 1.")

    def string_to_function(self, expression):
        """
        Evaluate formula from project file
        Credits: https://saturncloud.io/blog/pythonnumpyscipy-converting-string-to-mathematical-function/#numpys-frompyfunc-function
        Args:
            expression (string): weighting formula (from prj file)
        Returns:
            array
        """
        def function(x, y):
            return eval(expression)

        return np.frompyfunc(function, 2, 1)

    def expand_grid(self, x, y):
        """
        Create grid based on xy coordinates.
        Args:
            x (array): x-coordinates
            y (array): y-coordinates
        Returns:
            list(array, array)
        """
        xG, yG = np.meshgrid(x, y)
        xG = xG.flatten()
        yG = yG.flatten()

        return [xG, yG]

    def getPlantAttributes(self, initial_group):
        """
        Return positions and geometries of plants.
        Args:
            initial_group (bool): indicate whether these are the first plants in the system (initial population).
        Returns:
            dict, np.array
        """
        positions, geometry, network = self.dispersal.getPlantAttributes(initial_group=initial_group)

        # Check if plants are inside model domain
        if len(positions['x']) > 0:
            nx, mx = min(positions['x']), max(positions['x'])
            ny, my = min(positions['y']), max(positions['y'])
            borderx = [self.x_1, self.x_2]
            bordery = [self.y_1, self.y_2]
            if any([nx < x < mx for x in borderx]) or any([ny < y < my for y in bordery]):
                print("ERROR: Plant(s) are positioned outside model domain: X(", self.x_1, ", ", self.x_2, "), Y(",
                      self.y_1, ", ", self.y_2, "). Please check the population input file.")
                exit()
        return positions, geometry, network

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
                        super(Dispersal_v310, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(Dispersal_v310, self).__setattr__(tag, str(arg.text))
            try:
                required_tags.remove(tag)
            except ValueError:
                pass

            for i in range(0, len(optional_tags)):
                if tag == optional_tags[i]:
                    try:
                        super(Dispersal_v310, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(Dispersal_v310, self).__setattr__(tag, str(arg.text))

        if len(required_tags) > 0:
            string = ""
            for tag in required_tags:
                string += tag + " "
            raise KeyError(
                "Missing input parameters (in project file) for population module initialisation: " + string)

        try:
            self.n_recruitment_per_step = int(self.n_recruitment_per_step)
        except AttributeError:
            self.n_recruitment_per_step = 0

        try:
            self.n_individuals = int(self.n_individuals)
        except AttributeError:
            pass

        self.l_x = self.x_2 - self.x_1
        self.l_y = self.y_2 - self.y_1

        # Transfer attribute dictionary to respective dispersal module
        self.dispersal.__dict__.update(self.__dict__)
