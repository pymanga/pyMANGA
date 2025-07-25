#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib.BelowGround.Individual.FixedSalinity import FixedSalinity


class SaltFeedbackBucketHighPerformanceComputing(FixedSalinity):
    """
        High-Performance Computing version of the SaltFeedbackBucket below-ground resource concept.
        This class simulates soil salinity changes influenced by plant water uptake and mixing with 
        inflowing tidal water, with optimization for large-scale simulations.
    """

    def __init__(self, args):
        """
            Initialize the SaltFeedbackBucketHighPerformanceComputing module.
            Args:
                args (lxml.etree._Element): XML element specifying the below-ground module configuration.
        """
        self.getInputParameters(args)  # Load all input parameters from XML configuration
        self._t_ini = 0                # Initialize the start time
        super().makeGrid()             # Create the grid based on the input parameters
        self.getBorderValues()         # Determine boundary conditions for salinity and mixing rates
        self.getInflowSalinity()       # Calculate salinity of inflowing water for each cell
        self.getInflowMixingRate()     # Calculate mixing rates for each cell
        self.assignInitialCellSalinity()  # Assign initial salinity to each cell, either from a file or inflow salinity

    def assignInitialCellSalinity(self):
        """
            Assign initial cell salinity, either from a provided file or using the inflow salinity.
        """
        if hasattr(self, "initial_salinity_file"):
            # Load initial salinity matrix from file if provided
            self.sal_cell = np.loadtxt(self.initial_salinity_file, usecols=range(len(self.my_grid[0][0])))
        else:
            # Otherwise, set initial salinity to inflow salinity values
            self.sal_cell = self.sal_cell_inflow

    def prepareNextTimeStep(self, t_ini, t_end):
        """
            Prepare the model for the next simulation time step.
            Args:
                t_ini (float): start time of the time step
                t_end (float): end time of the time step
        """
        super().prepareNextTimeStep(t_ini, t_end)
        self.timesteplength = t_end - t_ini
        self.vol_sink_cell = np.zeros(np.shape(self.my_grid[0]))
        self.plant_cells = []
        self.plants = []

    def addPlant(self, plant):
        """
            Add a plant to the below-ground resource module.
            Args:
                plant: A plant object containing position, geometry, and parameters.
        """
        xp, yp = plant.getPosition()              # Get the plant's position
        geometry = plant.getGeometry()            # Get the plant's geometry
        parameter = plant.getParameter()          # Get the plant's parameters
        gci = plant.getGrowthConceptInformation() # Get the plant's growth concept information
        self.plants.append(plant)

        rrp = geometry["r_root"]                  # Root radius
        self._r_salinity.append(parameter["r_salinity"])  
        self._h_stem.append(geometry["h_stem"])
        self._r_crown.append(geometry["r_crown"])
        self._psi_leaf.append(parameter["leaf_water_potential"])
        self._xe.append(xp)

        try:
            # Water uptake per time step (m³)
            plant_water_uptake = gci["bg_resources"]  # m³ water per time step
        except KeyError:
            # If not defined, assume zero water uptake
            plant_water_uptake = 0

        if rrp < self.mesh_size:   
            rrp = self.mesh_size    # Ensure root radius is not smaller than the mesh size
        
        # Assign the plant's water uptake to the grid cells it affects
        self.calculatePlantSink(xp, yp, rrp, plant_water_uptake)


    def calculatePlantSink(self, x, y, r_root, bg_resources):
        """
            Assign plant water uptake (sink term) to affected grid cells.
            Args:
                x, y (float): Plant position
                r_root (float): Root radius
                bg_resources (float): Water uptake (m³) during this time step
        """
        idx = self.getAffectedCellsIdx(x, y, r_root)    # Get indices of affected cells
        self.plant_cells.append(idx)                    # Store affected cells for the plant
        if bg_resources != 0:
            no_cells = len(idx[0])          # Number of affected cells
            # Calculate the volume of water sink per cell
            sink_per_cell = bg_resources / (self.cell_area * no_cells) / self.timesteplength
            self.vol_sink_cell[idx] += sink_per_cell

    def calculateBelowgroundResources(self):
        """
            Compute below-ground resource factors for all plants.
        """
        self.getBorderValues()          # Update boundary conditions for salinity and mixing rates
        self.getInflowSalinity()        # Recalculate salinity of inflowing water for each cell
        self.getInflowMixingRate()      # Recalculate mixing rates for each cell
        self.calculateCellSalinity()    # Calculate salinity in each cell based on fresh water extraction and mixing with inflowing water

        salinity_plant = self.getPlantSalinity()        # Compute average salinity under each plant
        self.calculatePlantResources(salinity_plant)    # Compute below-ground resource factor

         # Update plant growth concept information with salinity values
         # IMPORTANT: also can be shifted for HPC version of the plant growth concept
         # maybe in the future  :)
        for i, plant in zip(range(0, len(self._xe)), self.plants):
            gci = plant.getGrowthConceptInformation()
            gci['salinity'] = salinity_plant[i]
            plant.setGrowthConceptInformation(gci)

    def getInflowSalinity(self):
        """
            Calculate the base salinity of inflowing water for each grid cell.
        """
        if len(self.my_grid[0]) == 1:
            # Single-cell grid: take average of left and right boundary salinity
            self.sal_cell_inflow = np.array([0.5 * (self._salinity[0] + self._salinity[1])])
        else:
            # Multi-cell grid: linearly interpolate salinity across the domain
            x_dif = self.x_2 - self.x_1
            self.sal_cell_inflow = (self.my_grid[0] - self.x_1) / x_dif * \
                                   (self._salinity[1] - self._salinity[0]) + self._salinity[0]

    def calculateCellSalinity(self):
        """
            Update salinity in each grid cell based on fresh water extraction (plants) 
            and mixing with inflowing tidal water.
        """
        ht = np.exp(- self.r_mix_inflow / self.depth * self.timesteplength)
        self.sal_cell = self.sal_cell * ht + (self.vol_sink_cell + self.r_mix_inflow) / \
                        self.r_mix_inflow * self.sal_cell_inflow * (1 - ht)
        self.writeGridSalinity(t_end=self._t_end, tsl=self.timesteplength)

    def getPlantSalinity(self):
        """
            Calculate pore-water salinity below each plant (mean value of all affected cells).
            Returns:
                numpy array with one salinity value per plant.
        """
        salinity_plant = np.zeros(len(self.plant_cells))
        for pc in range(len(self.plant_cells)):
            affected_cells = self.plant_cells[pc]
            salinity_plant[pc] = np.mean(self.sal_cell[affected_cells])
        return salinity_plant

    def writeGridSalinity(self, t_end, tsl):
        """
            Save the current salinity grid to a text file if the save option is enabled.
            Args:
                t_end (float): Current time
                tsl (float): Time step length
        """
        if hasattr(self, "save_file"):
            if t_end == 0 or t_end % (self.save_salinity_ts * tsl) == 0:
                np.savetxt(self.save_file + "_" + str(t_end) + '.txt', self.sal_cell)

    def getAffectedCellsIdx(self, xp, yp, rrp):
        """
            Identify the grid cells affected by a specific plant's root zone.
            Args:
                xp, yp (float): Plant coordinates
                rrp (float): Root radius
            Returns:
                Indices of grid cells within the plant's root zone.
        """
        distance = np.sqrt((self.my_grid[0] - xp) ** 2 + (self.my_grid[1] - yp) ** 2)
        return np.where(distance < rrp)

    def getBorderValues(self):
        """
            Determine boundary salinity and mixing rates, potentially applying time-varying or sine-based patterns.
        """
        if hasattr(self, "t_variable"):
            self.getSalinityTimeseries()
        elif hasattr(self, "amplitude"):
            if hasattr(self, "medium"):
                if "water" in self.medium.lower():
                    self.getMixingRateSine()
                if "salt" in self.medium.lower():
                    self.getSalinitySine()
            else:
                self.getSalinitySine()

    def readMixingRateTag(self):
        """
            Parse and read <r_mix> mixing rate from configuration.
        """
        if isinstance(self.r_mix, float):
            self.r_mix = [self.r_mix, self.r_mix]
        else:
            if len(self.r_mix.split()) == 2:
                try:
                    self.r_mix = self.r_mix.split()
                    self.r_mix[0] = float(eval(self.r_mix[0]))
                    self.r_mix[1] = float(eval(self.r_mix[1]))
                except NameError:
                    print("Error: Mix rate tag <r_mix> not properly defined.")
                    exit()
            else:
                print("Error: Mix rate tag <r_mix> not properly defined.")
                exit()
        self.left_bc_r_mix = self.r_mix[0]
        self.right_bc_r_mix = self.r_mix[1]

    def getInflowMixingRate(self):
        """
            Calculate mixing rate (r_mix) for each cell via linear interpolation between domain boundaries.
        """
        if len(self.my_grid[0]) == 1:
            self.r_mix_inflow = np.array([0.5 * (self.r_mix[0] + self.r_mix[1])])
        else:
            x_dif = self.x_2 - self.x_1
            self.r_mix_inflow = (self.my_grid[0] - self.x_1) / x_dif * \
                                (self.r_mix[1] - self.r_mix[0]) + self.r_mix[0]

    def getMixingRateSine(self):
        """
            Apply a sine-based variation to the mixing rate over time.
        """
        s0 = self.amplitude * np.sin(self._t_ini / self.stretch + self.offset)
        left = s0 + self.left_bc_r_mix
        self.r_mix[0] = np.random.normal(size=1, loc=left, scale=self.noise)
        self.r_mix[0] = self.r_mix[0] if self.r_mix[0] > 0 else 0
        right = s0 + self.right_bc_r_mix
        self.r_mix[1] = np.random.normal(size=1, loc=right, scale=self.noise)
        self.r_mix[1] = self.r_mix[1] if self.r_mix[1] > 0 else 0

    def getInputTags(self, args):
        """
            Define required and optional XML tags for configuration.
            Args:
                args: XML element with configuration data.
            Returns:
                Dictionary containing required and optional tags.
        """
        tags = {
            "prj_file": args,
            "required": ["type", "salinity", "x_1", "x_2", "y_1", "y_2",
                         "x_resolution", "y_resolution", "r_mix"],
            "optional": ["sine", "amplitude", "stretch", "offset", "noise",
                         "medium", "save_salinity_ts", "save_file",
                         "depth", "initial_salinity_file"]
        }
        return tags

    def getInputParameters(self, args):
        """
            Load and process input parameters from XML configuration.
        """
        tags = self.getInputTags(args)
        super(FixedSalinity, self).getInputParameters(**tags)
        self.setInputParameters()

    def setInputParameters(self):
        """
            Set default parameters if not specified in the input configuration.
        """
        super().setDefaultParameters()
        if not hasattr(self, "depth"):
            print("> Set below-ground parameter 'depth' to default: 1")
            self.depth = 1
        if hasattr(self, "sine"):
            if not hasattr(self, "medium"):
                print("> Set below-ground parameter 'medium' to default: salt")
                self.medium = "salt"
        self.readMixingRateTag()
        if hasattr(self, "save_file"):
            if not hasattr(self, "save_salinity_ts"):
                self.save_salinity_ts = 1

      