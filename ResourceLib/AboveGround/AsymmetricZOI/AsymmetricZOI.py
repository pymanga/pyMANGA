#!/usr/bin/env python3  # Shebang for Unix-like systems to run the script with Python 3
# -*- coding: utf-8 -*-  # File encoding declaration

import numpy as np  
from ResourceLib import ResourceModel  
from ResourceLib.AboveGround.AsymmetricZOI import asymzoi  # Import compiled C++ core module (pybind11)

class AsymmetricZOI(ResourceModel):  
    """
    AsymmetricZOI above-ground resource concept using the C++ core.  
    The class computes per-plant aboveground resource factors via asymzoi.compute_aboveground_resources.  
    """

    def __init__(self, args):  # Constructor accepting XML element 'args'
        self.getInputParameters(args)  # Parse and load parameters from XML into attributes
        super().makeGrid()  # Build spatial grid; expects self.my_grid = (grid_x, grid_y)

        # Determine mesh size: prefer attribute provided by the parent; otherwise infer from grid spacing
        if hasattr(self, "mesh_size") and self.mesh_size is not None:  # Check if mesh_size is available
            self._mesh_size = float(self.mesh_size)  # Store mesh size as float for downstream use
        else:  # If mesh_size is not provided, infer it from the grid arrays
            gx, gy = self._require_grid()  # Ensure grid exists and retrieve grid arrays
            _dx = np.median(np.diff(gx[0, :]).astype(np.float64)) if gx.shape[1] > 1 else np.nan  # Median x-spacing
            _dy = np.median(np.diff(gy[:, 0]).astype(np.float64)) if gy.shape[0] > 1 else np.nan  # Median y-spacing
            self._mesh_size = float(np.nanmedian([_dx, _dy]) if not np.isnan(_dx) or not np.isnan(_dy) else 1.0)  # Fallback to 1.0 if spacing is undefined

        self.prepareNextTimeStep(t_ini=None, t_end=None)  # Initialize per-timestep containers

    def calculateAbovegroundResources(self):  # Public method to compute aboveground resource factors
        n_plants = len(self.xe)  # Number of plants currently registered
        if n_plants == 0:  # Handle empty case to avoid unnecessary work
            self.aboveground_resources = np.array([], dtype=np.float32)  # Set empty result array
            return  # Exit early when there are no plants

        gx, gy = self._require_grid()  # Retrieve validated grid arrays (2D and same shape)

        # Convert inputs to C-contiguous float32 arrays to match the C++ interface and save memory
        xe = np.ascontiguousarray(np.asarray(self.xe, dtype=np.float32))  # X positions of plants
        ye = np.ascontiguousarray(np.asarray(self.ye, dtype=np.float32))  # Y positions of plants
        h_stem = np.ascontiguousarray(np.asarray(self.h_stem, dtype=np.float32))  # Stem heights per plant
        r_ag = np.ascontiguousarray(np.asarray(self.r_ag, dtype=np.float32))  # Crown radii per plant
        grid_x = np.ascontiguousarray(gx.astype(np.float32, copy=False))  # Grid X coordinates as float32
        grid_y = np.ascontiguousarray(gy.astype(np.float32, copy=False))  # Grid Y coordinates as float32

        # Call the C++ core to compute per-plant resource factors (wins / crown_area)
        out = asymzoi.compute_aboveground_resources(  # Invoke compiled kernel
            xe, ye, h_stem, r_ag,  # Per-plant vectors for geometry and position
            grid_x, grid_y,  # Grid coordinate matrices
            bool(self.curved_crown),  # Whether to use curved crown height profile
            float(self._mesh_size)  # Mesh size for minimum crown-radius handling
        )  # End of C++ call

        self.aboveground_resources = np.asarray(out, dtype=np.float32)  # Store result as float32 numpy array

    def getInputParameters(self, args):  # Parse XML configuration for the module
        tags = {  # Define required and optional XML tags
            "prj_file": args,  # Pass the XML element to the parent parser
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"],  # Mandatory fields
            "optional": ["allow_interpolation", "curved_crown"]  # Optional fields
        }  # End of tag specification
        super().getInputParameters(**tags)  # Delegate parsing to the parent implementation

        self._x_1 = self.x_1  # Cache domain minimum X
        self._x_2 = self.x_2  # Cache domain maximum X
        self._y_1 = self.y_1  # Cache domain minimum Y
        self._y_2 = self.y_2  # Cache domain maximum Y
        self.x_resolution = int(self.x_resolution)  # Ensure X resolution is integer
        self.y_resolution = int(self.y_resolution)  # Ensure Y resolution is integer

        self.allow_interpolation = super().makeBoolFromArg("allow_interpolation")  # Parse boolean for interpolation allowance
        if not hasattr(self, "curved_crown"):  # If curved_crown flag is absent
            self.curved_crown = True  # Default to True for curved crown shape
            print("INFO: set above-ground parameter curved_crown to default:", self.curved_crown)  # Inform about default
        else:  # If attribute exists from XML
            self.curved_crown = super().makeBoolFromArg("curved_crown")  # Parse boolean value

    def prepareNextTimeStep(self, t_ini, t_end):  # Reset data containers for a new simulation time step
        self.xe, self.ye, self.h_stem, self.r_ag = [], [], [], []  # Initialize per-plant arrays
        self.t_ini, self.t_end = t_ini, t_end  # Store time window for the step

    def addPlant(self, plant):  # Register one plant's geometry and position into buffers
        x, y = plant.getPosition()  # Get plant position (x, y)
        geometry = plant.getGeometry()  # Get plant geometry dictionary
        try:  # Try preferred key names
            r_ag = geometry["r_crown"]  # Crown radius if available
            h_stem = geometry["h_stem"]  # Stem height if available
        except KeyError:  # Fallback to legacy key names if needed
            r_ag = geometry["r_ag"]  # Legacy crown radius
            h_stem = geometry["height"] - 2 * r_ag  # Derive stem height from total height minus crown diameter

        _min_r_ag = float(self._mesh_size) * (1.0 / np.sqrt(2.0))  # Minimum allowed crown radius per cell-size rule
        if r_ag < _min_r_ag and not getattr(self, "allow_interpolation", False):  # Enforce minimum radius unless interpolation is allowed
            print("Error: mesh not fine enough for crown dimensions!")  # Error message for insufficient mesh resolution
            print(  # Additional guidance on how to proceed
                "Please refine mesh or increase initial crown radius above "
                f"{self._mesh_size:.6f} m !"  # Include numeric threshold in message
            )  # End of message
            raise SystemExit(1)  # Abort execution as configuration is invalid

        self.xe.append(float(x))  # Append plant x-position as float
        self.ye.append(float(y))  # Append plant y-position as float
        self.h_stem.append(float(h_stem))  # Append stem height as float
        self.r_ag.append(float(r_ag))  # Append crown radius as float

    def _require_grid(self):  # Internal helper to validate and return grid arrays
        if not hasattr(self, "my_grid") or self.my_grid is None or len(self.my_grid) != 2:  # Ensure grid exists and has two components
            raise RuntimeError("Grid not initialized. Did super().makeGrid() run?")  # Raise clear error if missing
        gx, gy = self.my_grid  # Unpack grid components
        if gx.ndim != 2 or gy.ndim != 2 or gx.shape != gy.shape:  # Validate dimensionality and shape consistency
            raise RuntimeError("grid_x and grid_y must be 2D arrays with the same shape.")  # Raise error if invalid
        return gx, gy  # Return validated grid arrays
