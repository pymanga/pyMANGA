#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel
from joblib import Parallel, delayed
from multiprocessing import cpu_count


def _compute_single_tree(i, x, y, h_stem, r_ag, grid_x, grid_y, curved_crown, mesh_size, min_r_ag):
    """
        Calculate the crown height and crown cover area of a single tree.
        i: index of the tree 
        x, y: positional coordinates of the tree 
        h_stem: height of the trunk 
        r_ag: radius of the crown 
        grid_x, grid_y: grid coordinate matrix 
        curved_crown: whether to use a curved crown shape or not 
        mesh_size: size of the mesh 
        min_r_ag: threshold for the minimum value of the crown radius

        Note:
        In joblib parallelization, if _compute_single_tree were defined as a method within 
        the AsymmetricZOIHighPerformanceComputing class, the entire class instance (self) 
        would need to be serialized and copied to worker processes or threads, leading to 
        additional memory overhead and potential serialization failures due to non-pickleable objects. 

        By defining _compute_single_tree as an external standalone function, it can be treated as a 
        simple function pointer that does not require serializing the class instance, making it faster 
        and more efficient to distribute tasks across parallel workers while minimizing memory usage.

        ***Important:
        https://peps.python.org/pep-0008/#naming-conventions
        In Python, a leading underscore in a function or variable name (e.g., _compute_single_tree) is a naming convention 
        used to indicate that the function is intended for internal use only within a module or class. 

        It signals to developers that the function is part of the internal implementation and not part 
        of the public API, even though Python does not enforce strict access control. 

        This convention also helps avoid name collisions when using from module import *, 
        as names starting with an underscore are not imported by default. In short, the underscore is 
        a way to communicate that the function is a helper or private utility, rather than something meant 
        to be called directly by users.

        So, Guanzhen used a leading underscore in the new function's name to indicate that it is a helper function.
    """
    dx = grid_x - x   # Calculate the x-direction distance from the grid point to the tree location
    dy = grid_y - y   # Calculate the y-direction distance from the grid point to the tree location
    distance_sq = dx * dx + dy * dy    # Calculate the squared distance from the grid point to the tree location

    # determine crown radius
    if r_ag < min_r_ag:
        r_ag = mesh_size

    r_ag_sq = r_ag * r_ag       # Calculate the squared crown radius
    mask = distance_sq <= r_ag_sq     # Create a mask for grid points within the crown radius
    my_height = np.zeros_like(distance_sq)  # Initialize the height array to zero

    # calculate height based on distance
    if curved_crown:
        temp = np.maximum(4 * r_ag_sq - distance_sq[mask], 0)   # Calculate the height based on the distance for curved crown
        my_height[mask] = h_stem + np.sqrt(temp)   # Assign the calculated height to the mask positions
    else:
        my_height[mask] = h_stem + 2 * r_ag    # Assign the height for a flat crown

    crown_area = np.count_nonzero(mask)   # Calculate the crown area as the number of grid points within the crown radius
    return i, my_height, crown_area  


class AsymmetricZOIHighPerformanceComputing(ResourceModel):
    """
        High-performance computing version of the Asymmetric Zone of Influence (Asymmetric ZOI).
        Batch parallel processing and memory optimization strategies are adopted to improve speed and efficiency during large-scale tree calculations.
    """

    def __init__(self, args):
        case = args.find("type").text   # Get the case type from the arguments
        self.getInputParameters(args)   # Get input parameters from the arguments
        super().makeGrid()              # Create the grid based on the input parameters

    def _determine_n_jobs(self, n_plants):
        """
            Dynamically determine the number of parallel threads.
            n_plants: Number of plants
            Returns: Recommended number of threads (no more than 10 or the number of CPU cores)
        """
        max_threads = min(10, cpu_count())  #   Limit to 10 threads or available CPU cores
        return min(16, max_threads) if n_plants < 10_000 else max_threads   

    def _determine_batch_size(self, n_plants, grid_size, force_batch_size=None):
        """
        Dynamically adjust the batch size based on the grid size. The larger the grid, the smaller the batch size to avoid memory overflow.
        force_batch_size: If not None, a fixed batch size will be enforced.
        """
        if force_batch_size is not None:
            return min(force_batch_size, n_plants)

        if grid_size > 2_000_000:       # Extra-large grid
            base_size = 500
        elif grid_size > 1_000_000:     # Large grid
            base_size = 5000
        elif grid_size > 500_000:       # Medium grid
            base_size = 10000
        else:                           # Small grid
            base_size = 20000          # Default batch size for small grids
        return min(base_size, n_plants)

    def calculateAbovegroundResources(self):
        """
        Calculate above-ground resources allocation.
        """
        n_plants = len(self.xe)
        if n_plants == 0:
            self.aboveground_resources = np.array([])
            return

        grid_x, grid_y = self.my_grid
        canopy_height = np.zeros_like(grid_x)
        highest_plant = np.full_like(grid_x, fill_value=-1, dtype=np.int64)
        crown_areas = np.zeros(n_plants)
        wins = np.zeros(n_plants)

        n_jobs = self._determine_n_jobs(n_plants)
        grid_size = grid_x.size
        batch_size = self._determine_batch_size(n_plants, grid_size, force_batch_size=8000)
        n_batches = (n_plants + batch_size - 1) // batch_size
        print(f"[INFO] Using {n_jobs} threads for {n_plants} plants (batch_size={batch_size}, total_batches={n_batches}).")

        min_r_ag = self.mesh_size * (1 / 2 ** 0.5)
        mask_buffer = np.zeros_like(canopy_height, dtype=bool)

        # Parallel computation in batches
        for batch_idx, start in enumerate(range(0, n_plants, batch_size), start=1):
            end = min(start + batch_size, n_plants)
            percent = batch_idx / n_batches * 100
            print(f"[INFO] Processing batch {batch_idx}/{n_batches} ({start} to {end-1}) ... {percent:.2f}% done.")

            results = Parallel(n_jobs=n_jobs, prefer="threads")(
                delayed(_compute_single_tree)(
                    i, self.xe[i], self.ye[i],
                    self.h_stem[i], self.r_ag[i],
                    grid_x, grid_y, self.curved_crown,
                    self.mesh_size, min_r_ag
                )
                for i in range(start, end)
            )

            # Serial merging of batch results
            for i, my_height, crown_area in results:
                crown_areas[i] = crown_area
                mask_buffer[:] = my_height > canopy_height
                np.copyto(canopy_height, my_height, where=mask_buffer)
                np.copyto(highest_plant, i, where=mask_buffer)

        # Vectorized wins statistics
        valid_idx = highest_plant[highest_plant >= 0]
        counts = np.bincount(valid_idx, minlength=n_plants)
        wins[:] = counts

        self.aboveground_resources = wins / crown_areas

        # check NaN
        if np.any(np.isnan(self.aboveground_resources)):
            nan_indices = np.where(np.isnan(self.aboveground_resources))[0]
            print(f"ERROR: NaN detected in aboveground_resources for plants at indices: {nan_indices}")
            exit()

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"],
            "optional": ["allow_interpolation", "curved_crown"]
        }
        super().getInputParameters(**tags)
        self._x_1 = self.x_1
        self._x_2 = self.x_2
        self._y_1 = self.y_1
        self._y_2 = self.y_2
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)

        self.allow_interpolation = super().makeBoolFromArg("allow_interpolation")

        if not hasattr(self, "curved_crown"):
            self.curved_crown = True
            print("INFO: set above-ground parameter curved_crown to default: ", self.curved_crown)
        else:
            self.curved_crown = super().makeBoolFromArg("curved_crown")

    def prepareNextTimeStep(self, t_ini, t_end):
        self.xe = []
        self.ye = []
        self.h_stem = []
        self.r_ag = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        try:
            r_ag = geometry["r_crown"]
            h_stem = geometry["h_stem"]
        except KeyError:
            r_ag = geometry["r_ag"]
            h_stem = geometry["height"] - 2 * r_ag

        if r_ag < (self.mesh_size * 1 / 2 ** 0.5):
            if not hasattr(self, "allow_interpolation") or not self.allow_interpolation:
                print("Error: mesh not fine enough for crown dimensions!")
                print("Please refine mesh or increase initial crown radius above " +
                      str(self.mesh_size) + "m !")
                exit()

        self.xe.append(x)
        self.ye.append(y)
        self.h_stem.append(h_stem)
        self.r_ag.append(r_ag)
