#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. include:: ./SoilWaterContent.md
"""
import numpy as np
from os import path
from ResourceLib import ResourceModel
from PlantModelLib.Bettina import Bettina


class SoilWaterContent(ResourceModel):
    ## Simple soil water content water scarcity model. This concept is based
    #  on the idead of plants occupying the same node of the grid share
    #  the below-ground resource of this node equally (BETTINA geometry of a
    #  plant assumed). See Heinermann 2023: ODD protocol of the model
    #  BETTINA-AYSE IBM\n
    #  Forest patches represent the forest soil with its specific capabilities
    #  of storing water (c water) and releasing it for use by plants
    #  (psi matrix). plants interact with the soil by taking up water and thus
    #  reducing the water content of the soil (c water). It is assumed that
    #  plant roots do not reach deeper than 1 meter below ground level and thus
    #  plants do not have access to groundwater. Soil water content (c water)
    #  is therefore only increased by precipitation and only decreased by plant
    #  uptake. This simplification of a groundwater model is described as
    #  ”bucket”-model (Manabe 1969).
    #  @param Tags to define SoilWaterContent: see tag documentation
    #  @date: 2023 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.getInputParameters(args)
        super().makeGrid()
        self.initializeSoil()
        self.initializePrecipitation()

    ## Initialization of soil properties according to Janosh ODD
    def initializeSoil(self):
        ## Maximal soil water content [m**3]
        self.max_soil_water_content = (self.omega_r + (self.omega_s - self.omega_r) /
                                       ((1 + (-self.alpha * self.psi_matrix / 100)**self.n)**(1 - 1 / self.n))) *\
                                      np.ones_like(self.my_grid[1])
        ## Current soil water content [m**3]
        self.soil_water_content = 0 + self.max_soil_water_content # 0 + -- creates copy

    ## This function prepares the precipitation submodel based on information
    #  provided in the pymanga-config file.
    def initializePrecipitation(self):
        file_name = path.join(path.abspath("./"), self.data_file)
        column_number = int(self.precipitation_col_number)
        self.delta_tpercip = float(self.delta_t_per_row)

        precipitation = np.loadtxt(file_name, delimiter=";", skiprows=1, usecols=column_number - 1)

        # Empty array
        self.precipitation_input = np.zeros(len(precipitation))
        ## Precipitation input: precipitation in [m]
        self.precipitation_input = precipitation / 1000.

    ## This functions prepares arrays for the competition
    #  concept. In the SymmetricZOI concept, plants geometric measures
    #  are saved in simple lists and the timestepping is updated. \n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self.xe = []
        self.ye = []
        self.r_roots = []
        self.r_crowns = []
        self.h_stems = []
        self.delta_psis = []
        self.flow_lengths = []
        self.plant_volums = []
        self.flow_resistances = []


        self.t_ini = t_ini
        self.t_end = t_end
        self.plants = []
        self.plant_flows = []
        self.max_plant_flows = []

    ## Integrates precipitation data
    #  In the current form, the precipitation falls directly to the ground.
    #  Stem flow and interception loss can be integrated in this function.
    #  @param t_0 - Start time for precipitation period
    #  @param t_1 - End time for precipitation period
    def integratePrecipitationData(self, t_0, t_1):
        # Index of t_ini and t_end in self.precipitation_input. The number
        # calculated here is a float
        t_0_idx = (t_0 / self.delta_tpercip) % len(self.precipitation_input)
        t_1_idx = (t_1 / self.delta_tpercip) % len(self.precipitation_input)

        # Precipitation data in three parts:
        # contribution_left corresponds to part before the first full idx
        # contribution_right corresponds to part behind the last full idx
        # contribution_middle addresses all other datapoints
        contribution_left = self.precipitation_input[int(t_0_idx)] * (1 - t_1_idx % 1)
        contribution_right = self.precipitation_input[int(t_1_idx)] * (t_1_idx % 1)

        # If condition catches, if the modulus of timesteps in percipitation
        # data file is active.
        if int(t_0_idx) <= int(t_1_idx):
            contribution_middle = np.sum(self.precipitation_input[
                int(t_0_idx) + 1:int(t_1_idx)])
        elif int(t_0_idx) > int(t_1_idx):
            contribution_middle = np.sum(self.precipitation_input[
                int(t_0_idx) + 1:])
            contribution_middle += np.sum(self.precipitation_input[
                :int(t_1_idx)])

        integrated_precipitation = contribution_left + contribution_right + contribution_middle
        # Update of soil water content with new precipitation
        self.updateSoilWaterContent(integrated_precipitation)

    ## Update of soil water content (SWC) [m]
    #  @param flux - water flux into patch in [m].
    #  Positive value corresponds to influx.
    def updateSoilWaterContent(self, flux):
        ## Add infiltration to SWC
        self.soil_water_content += flux
        ## Cap SWC at maximum value
        idx = np.where(self.soil_water_content > self.max_soil_water_content)
        self.soil_water_content[idx] = self.max_soil_water_content[idx]
        ## Cut SWC at minimum value (residual water content)
        self.soil_water_content[np.where(self.soil_water_content < self.omega_r)] = self.omega_r

    ## Before being able to calculate the resources, all plant entities need
    #  to be added with their current implementation for the next timestep.
    #  @param plant
    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        self.parameter = plant.getParameter()
        growth_concept_information = plant.getGrowthConceptInformation()
        self.pf = self.parameter["pF"]
        try:
            root_surface_resistance = growth_concept_information["root_surface_resistance"]
            xylem_resistances = growth_concept_information["xylem_resistance"]
            flow = growth_concept_information["bg_resources"]
        except KeyError:
            root_surface_resistance = 0
            xylem_resistances = 0
            flow = 0
            print("WARNING: Set flow resistance & water uptake to 0 as values are not available.")
            # This should only happen in the very first timestep.

        self.flow_resistances.append(root_surface_resistance+xylem_resistances)

        if geometry["r_root"] < self._mesh_size * 1 / 2**0.5:
            print("Error: mesh not fine enough for root dimensions!")
            print("Please refine mesh or increase initial root radius above ",
                  str(self._mesh_size) + "m !")
            exit()
        if not ((self._x_1 < x < self._x_2) and (self._y_1 < y < self._y_2)):
            raise ValueError("""It appears as a plant is located outside of the
                             domain, where BC is defined. Please check domains
                             in project file!!""")

        self.r_crown = geometry["r_crown"]
        self.h_crown = geometry["h_crown"]
        self.r_root = geometry["r_root"]
        self.h_root = geometry["h_root"]

        self.r_stem = geometry["r_stem"]
        self.h_stem = geometry["h_stem"]

        self.xe.append(x)
        self.ye.append(y)
        self.r_roots.append(self.r_root)
        self.r_crowns.append(self.r_crown)
        self.h_stems.append(self.h_stem)
        delta_psi = Bettina.deltaPsi(self=self)
        self.delta_psis.append(delta_psi)
        self.flow_lengths.append(Bettina.flowLength(self=self))
        self.plant_volums.append(Bettina.treeVolume(self=self))

        ## List of plants
        self.plants.append(plant)
        ## List containing current flow for each plant [m]
        self.plant_flows.append(0)

        # Calculation of potential maximal flow for plant
        self.calculateMatrixPotential(self.max_soil_water_content)

        self.time = self.delta_t_concept

        # flow = self.bgResources(bg_factor=(delta_psi - self.psi_matrix[0, 0]) / delta_psi,
        #                         delta_time=self.t_end - self.t_ini)
        ## List containing potential flow for each plant [m]
        self.max_plant_flows.append(flow)

    ## This function returns the BelowgroundResources calculated in the
    #  subsequent timestep.\n
    #  @return: np.array with $N_plant$ scalars
    def calculateBelowgroundResources(self):
        if np.sum(self.max_plant_flows) == 0:
            print("WARNING: Set bg_factor to 1 because no plant water uptake occurred.")
            self.belowground_resources = np.full(shape=len(self.xe), fill_value=1)
        else:
            t_1 = self.t_ini
            t_2 = 0
            # Numpy array of shape [res_x, res_y, n_plants]
            # Distance of all nodes to each plant
            distance = ((self.my_grid[0][:, :, np.newaxis] - np.array(self.xe)[np.newaxis, np.newaxis, :])**2 +
                        (self.my_grid[1][:, :, np.newaxis] - np.array(self.ye)[np.newaxis, np.newaxis, :])**2)**0.5
            # While loop applies concept native timestepping
            # If delta_t_concept < delta_t, time stepping is refined
            # otherwise, delta_t is used
            while t_2 < self.t_end:
                if (t_1 + self.delta_t_concept) <= self.t_end:
                    t_2 = t_1 + self.delta_t_concept
                else:
                    t_2 = self.t_end
                # Array to store data for total water flux per timestep
                flux = np.zeros_like(self.soil_water_content)
                # Update precipitation
                self.integratePrecipitationData(t_1, t_2)
                # Calculate resulting soil potentials
                self.calculateMatrixPotential(self.soil_water_content)
                for i in range(len(self.plants)):
                    root_radius = self.r_roots[i]

                    plant_nodes = np.where(root_radius > distance[:, :, i])
                    # Actual flow for plant i
                    psi_matrix = self.psi_matrix[plant_nodes]
                    flow = self.bgResources(idx_plant=i,
                                            psi_matrix=psi_matrix,
                                            delta_time=t_2 - t_1)
                    # Contribution to the fluxes in and out of the grid
                    flux[plant_nodes] -= flow / float(len(plant_nodes[0]))
                    # Average flow for plant
                    self.plant_flows[i] += np.sum(flow) / float(len(plant_nodes[0]))
                self.updateSoilWaterContent(flux)
                t_1 = t_2
            # Belowground resources is real flow divided by potential flow
            bg_factor = np.array(self.plant_flows) / np.array(self.max_plant_flows)
            self.belowground_resources = np.where(bg_factor >= 1, 1, bg_factor)

    ## Calculates matrix potential according to equation from janosch
    # Matrix potential ~ pF value (transformed)
    # psi_matrix = -100 * 10**pF
    #  @param water_content - water content of the soil
    def calculateMatrixPotential(self, water_content):
        # ToDo: Was ist hier der richtige Code?
        base = (self.omega_s - self.omega_r) / (water_content - self.omega_r)
        exponent = 1 / (1 - 1 / self.n)
        self.psi_matrix = - (base ** exponent - 1) ** (1 / self.n) / self.alpha

        # self.psi_matrix = water_content * 0
        # self.psi_matrix = -100 * (10**self.pf) + self.psi_matrix
        # self.psi_matrix[np.where(self.psi_matrix < -7860000)] = -7860000

    def bgResources(self, idx_plant, psi_matrix, delta_time):
        delta_psi = self.delta_psis[idx_plant]
        tot_res = self.flow_resistances[idx_plant]
        bg_factor = (delta_psi - psi_matrix) / delta_psi
        bg_resources = bg_factor * (-delta_time * delta_psi / tot_res / np.pi)
        return bg_resources

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution",
                         "delta_t_concept",
                         "omega_s", "omega_r", "alpha", "n", "psi_matrix",
                         "data_file", "precipitation_col_number", "delta_t_per_row"]
        }
        super().getInputParameters(**tags)
        self._x_1 = self.x_1
        self._x_2 = self.x_2
        self._y_1 = self.y_1
        self._y_2 = self.y_2
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)
