#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. include:: ./SoilWaterContent.md
"""

import numpy as np
from os import path
from ResourceLib import ResourceModel
from PlantModelLib.SimpleBettina import SimpleBettina


class SoilWaterContent(ResourceModel):
    ## Simple soil water content water scarcity model. This concept is based
    #  on the idead of trees occupying the same node of the grid share
    #  the below-ground resource of this node equally (BETTINA geometry of a
    #  tree assumed). See Heinermann 2023: ODD protocol of the model
    #  BETTINA-AYSE IBM\n
    #  Forest patches represent the forest soil with its specific capabilities
    #  of storing water (c water) and releasing it for use by plants
    #  (psi matrix). Trees interact with the soil by taking up water and thus
    #  reducing the water content of the soil (c water). It is assumed that
    #  tree roots do not reach deeper than 1 meter below ground level and thus
    #  plants do not have access to groundwater. Soil water content (c water)
    #  is therefore only increased by precipitation and only decreased by plant
    #  uptake. This simplification of a groundwater model is described as
    #  ”bucket”-model (Manabe 1969).
    #  @param Tags to define SoilWaterContent: see tag documentation
    #  @date: 2023 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        # Grid initialization
        self.makeGrid(args)
        self.initializeSoil(args.find("soil_properties"))
        self.initializePrecipitation(args.find("precipitation"))
        ## Timestepping of belowground competition concept
        self._delta_t_concept = float(args.find("delta_t_concept").text)

    ## Initialization of soil properties according to Janosh ODD
    def initializeSoil(self, args):
        # Model initialization
        ## Saturated water content [m**3/m**3]
        self._omega_s = float(args.find("omega_s").text)
        ## Residual water content [m**3/m**3]
        self._omega_r = float(args.find("omega_r").text)
        ## Scaling of matrix potential [1/PA]
        self._alpha = float(args.find("alpha").text)
        ## Measure for pore-size distribution
        self._n = float(args.find("n").text)
        ## Suction pressure [Pa]
        self._psi_matrix = float(args.find("psi_matrix").text)
        ## Maximal soil water content [m**3]
        self._max_soil_water_content = (
            self._omega_r + (self._omega_s - self._omega_r) / ((
                1 + (-self._alpha * self._psi_matrix / 100)**self._n)**(
                    1 - 1 / self._n))) * np.ones_like(self.my_grid[1])
        ## Current soil water content [m**3]
        self._soil_water_content = 0 + self._max_soil_water_content # 0 + -- creates copy

    ## This function prepares the precipitation submodel based on information
    #  provided in the pymanga-config file.
    def initializePrecipitation(self, args):
        file_name = path.join(path.abspath("./"),
                              args.find("data_file").text.strip())
        column_number = int(args.find("precipitation_col_number").text)
        self._delta_tpercip = float(args.find("delta_t_per_row").text)

        precipitation = np.loadtxt(
            file_name, delimiter=";", skiprows=1, usecols=column_number - 1)

        # Empty array
        self._precipitation_input = np.zeros(len(precipitation))
        ## Precipitation input: precipitation in [m]
        self._precipitation_input = precipitation / 1000.

    ## This functions prepares arrays for the competition
    #  concept. In the SymmetricZOI concept, trees geometric measures
    #  are saved in simple lists and the timestepping is updated. \n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self.xe = []
        self.ye = []
        self._t_ini = t_ini
        self._t_end = t_end
        self._trees = []
        self._tree_flows = []
        self._max_tree_flows = []

    ## Integrates precipitation data
    #  In the current form, the precipitation falls directly to the ground.
    #  Stem flow and interception loss can be integrated in this function.
    #  @param t_0 - Start time for precipitation period
    #  @param t_1 - End time for precipitation period
    def integratePrecipitationData(self, t_0, t_1):
        # Index of t_ini and t_end in self._precipitation_input. The number
        # calculated here is a float
        t_0_idx = (t_0 / self._delta_tpercip
                   ) % len(self._precipitation_input)
        t_1_idx = (t_1 / self._delta_tpercip
                   ) % len(self._precipitation_input)

        # Precipitation data in three parts:
        # contribution_left corresponds to part before the first full idx
        # contribution_right corresponds to part behind the last full idx
        # contribution_middle addresses all other datapoints
        contribution_left = self._precipitation_input[int(t_0_idx)
                                                      ] * (1 - t_1_idx % 1)
        contribution_right = self._precipitation_input[int(t_1_idx)
                                                       ] * (t_1_idx % 1)
        # If condition catches, if the modulus of timesteps in percipitation
        # data file is active.
        if int(t_0_idx) <= int(t_1_idx):
            contribution_middle = np.sum(self._precipitation_input[
                int(t_0_idx) + 1:int(t_1_idx)])
        elif int(t_0_idx) > int(t_1_idx):
            contribution_middle = np.sum(self._precipitation_input[
                int(t_0_idx) + 1:])
            contribution_middle += np.sum(self._precipitation_input[
                :int(t_1_idx)])

        integrated_precipitation = (
            contribution_left + contribution_right + contribution_middle)
        # Update of soil water content with new precipitation
        #self.updateSoilWaterContent(integrated_precipitation)

    ## Update of soil water content (SWC) [m]
    #  @param flux - water flux into patch in [m].
    #  Positive value corresponds to influx.
    def updateSoilWaterContent(self, flux):
        ## Add infiltration to SWC
        self._soil_water_content += flux
        ## Cap SWC at maximum value
        idx = np.where(self._soil_water_content > self._max_soil_water_content)
        self._soil_water_content[idx] = self._max_soil_water_content[idx]
        ## Cut SWC at minimum value (residual water content)
        self._soil_water_content[
            np.where(self._soil_water_content < self._omega_r)] = self._omega_r

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their current implementation for the next timestep.
    #  @param tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        self._pf = parameter["pF"]
        if geometry["r_root"] < self.min_r_root:
            print("Error: mesh not fine enough for root dimensions!")
            print("Please refine mesh or increase initial root radius above ",
                  str(self.min_r_root) + "m !")
            exit()
        if not ((self._x_1 < x < self._x_2) and (self._y_1 < y < self._y_2)):
            raise ValueError("""It appears as a tree is located outside of the
                             domain, where BC is defined. Please check domains
                             in project file!!""")
        self.xe.append(x)
        self.ye.append(y)
        ## List of trees
        self._trees.append(tree)
        ## List containing current flow for each tree [m]
        self._tree_flows.append(0)

        # Calculation of potential maximal flow for tree
        self.calculateMatrixPotential(self._max_soil_water_content)
        self.extractRelevantInformation(
            geometry=geometry,
            parameter=parameter)
        flow = (self.bgResources(
            (self.deltaPsi() - self._psi_matrix[0, 0]
             ) / self.deltaPsi(),
            self._t_end - self._t_ini))
        ## List containing potential flow for each tree [m]
        self._max_tree_flows.append(flow)

    ## This function returns the BelowgroundResources calculated in the
    #  subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        t_1 = self._t_ini
        t_2 = 0
        # Numpy array of shape [res_x, res_y, n_trees]
        # Distance of all nodes to each tree
        distance = (((self.my_grid[0][
            :, :, np.newaxis] - np.array(self.xe)[
                np.newaxis, np.newaxis, :])**2 + (
                    self.my_grid[1][
                        :, :, np.newaxis] - np.array(self.ye)[
                            np.newaxis, np.newaxis, :])**2)**0.5)
        # While loop applies concept native timestepping
        # If delta_t_concept < delta_t, time stepping is refined
        # otherwise, delta_t is used
        while t_2 < self._t_end:
            if (t_1 + self._delta_t_concept) <= self._t_end:
                t_2 = t_1 + self._delta_t_concept
            else:
                t_2 = self._t_end
            # Array to store data for total water flux per timestep
            flux = np.zeros_like(self._soil_water_content)
            # Update precipitation
            self.integratePrecipitationData(t_1, t_2)
            # Calculate resulting soil potentials
            self.calculateMatrixPotential(self._soil_water_content)
            for i in range(len(self._trees)):
                tree = self._trees[i]
                # Calculation of possible water uptake for each tree
                self.extractRelevantInformation(
                    geometry=tree.getGeometry(),
                    parameter=tree.getParameter())
                root_radius = tree.geometry["r_root"]
                tree_nodes = np.where(root_radius > distance[:, :, i])
                # Actual flow for tree i
                flow = (self.bgResources(
                    (self.deltaPsi() - self._psi_matrix[tree_nodes]
                     ) / self.deltaPsi(),
                    t_2 - t_1))
                # Contribution to the fluxes in and out of the grid
                flux[tree_nodes] -= flow / float(len(tree_nodes[0]))
                # Average flow for tree
                self._tree_flows[i] += np.sum(flow) / float(len(tree_nodes[0]))

            #self.updateSoilWaterContent(flux)
            t_1 = t_2
        # Belowground resources is real flow divided by potential flow
        self.belowground_resources = np.array(
            self._tree_flows) / np.array(self._max_tree_flows)
        print("time: ", int(self._t_end / 3600 / 24), ", pF: ", self._pf,
              ", mean soil water content: ", np.mean(self._soil_water_content),
              ", mean psi matrix: ", np.mean(self._psi_matrix),
              ", below_c: ", self.belowground_resources)
        exit()

    ## Calculates matrix potential according to equation from janosch
    # Matrix potential ~ pF value (transformed)
    # psi_matrix = -100 * 10**pF
    #  @param water_content - water content of the soil
    def calculateMatrixPotential(self, water_content):
        # base = ((self._omega_s - self._omega_r) / (
        #     water_content - self._omega_r))
        # exponent = 1 / (1 - 1 / self._n)
        # self._psi_matrix = - (
        #     base ** exponent - 1) ** (1 / self._n) / self._alpha
        self._psi_matrix = water_content * 0
        self._psi_matrix = -100 * (10**self._pf) + self._psi_matrix
        self._psi_matrix[np.where(self._psi_matrix < -7860000)] = -7860000



    ## Runs all functions relevant to calculate tree water uptake using Bettina
    #  @param geometry - tree geometry
    #  @param parameter - tree parameter
    def extractRelevantInformation(self, geometry, parameter):
        self.time = self._delta_t_concept
        SimpleBettina.extractRelevantInformation(
            self=self, geometry=geometry, parameter=parameter)

    ## Composite from BETTINA
    def flowLength(self):
        SimpleBettina.flowLength(self=self)

    ## Composite from BETTINA
    def treeVolume(self):
        SimpleBettina.treeVolume(self=self)

    ## Composite from BETTINA
    def rootSurfaceResistance(self):
        SimpleBettina.rootSurfaceResistance(self=self)

    ## Composite from BETTINA
    def xylemResistance(self):
        SimpleBettina.xylemResistance(self=self)

    ## Composite from BETTINA
    def deltaPsi(self):
        return SimpleBettina.deltaPsi(self=self)

    ## Composite from BETTINA: TODO: needed?
    def bgResources(self, bg_resources, delta_time):
        self.time = delta_time
        SimpleBettina.bgResources(self=self,
                                  belowground_resources=bg_resources)
        return self.bg_resources

    ## This function reads x- and y-domain and mesh resolution
    #  from project file and creates the mesh.\n
    #  @param Tags to define plot size and spatial resolution: see tag
    #  documentation
    #  TODO: Update after restructuring
    def makeGrid(self, args):
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution",
            "y_resolution"
        ]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "x_resolution":
                x_resolution = int(arg.text)
            if tag == "y_resolution":
                y_resolution = int(arg.text)
            elif tag == "x_1":
                self._x_1 = float(arg.text)
            elif tag == "x_2":
                self._x_2 = float(arg.text)
            elif tag == "y_1":
                self._y_1 = float(arg.text)
            elif tag == "y_2":
                self._y_2 = float(arg.text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                pass
                # print("WARNING: Tag " + tag +
                #       " not specified for below-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground grid initialisation in "
                "project file.")
        l_x = self._x_2 - self._x_1
        l_y = self._y_2 - self._y_1
        x_step = l_x / x_resolution
        y_step = l_y / y_resolution
        self.min_r_root = np.max([x_step, y_step]) * 1 / 2**0.5
        xe = np.linspace(self._x_1 + x_step / 2.,
                         self._x_2 - x_step / 2.,
                         x_resolution,
                         endpoint=True)
        ye = np.linspace(self._y_1 + y_step / 2.,
                         self._y_2 - y_step / 2.,
                         y_resolution,
                         endpoint=True)
        self.my_grid = np.meshgrid(xe, ye)
