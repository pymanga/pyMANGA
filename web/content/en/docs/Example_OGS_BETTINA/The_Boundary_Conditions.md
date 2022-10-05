---
title: "The boundary conditions"
linkTitle: "The boundary conditions"
weight: 3
description:
---

For the groundwater flow model, boundary conditions and source terms must be specified.
In this example, the boundary conditions are defined using a python script.
Basically, there are other ways to define boundary conditions.
For information that goes beyond the examples presented, the OGS community provides a <a href="https://www.opengeosys.org/" target="_blank">detailed documentation</a>.

In this example, boundary conditions are specified along the y-z boundaries of the domain.
In addition - depending on the tide - a seawater connection is created on the surface for a limited period of time.
The script used in this example starts with package imports as usual.
We need the packages *OpenGeoSys, vtk, numpy, math* and *os*.

	import OpenGeoSys
	import vtk as vtk
	import numpy as np
	from math import pi, sin
	import os


For later introduction of tidal activity, the tides can be described as follows:

    def tidal_cycle(t):
        return (sin(2 * pi * t / tide_daily_period) *
            (tide_daily_amplitude +
             tide_monthly_amplitude * sin(2 * pi * t / tide_monthly_period)))

What really matters is how the pressure is calculated along our edge surfaces.
A simple approach would be:

    def transectElevation(x, m=1e-3):
        return float(m * x)

    def pressure_value(z,x, tidal_cycle):
        return 1000 * 9.81 * (max(tidal_cycle, transectElevation(x)) - z)

With this helper function, we can define the pressure gradient along the edges .
In each case, we introduce a boundary condition that either does not allow flow across the boundary surfaces (no connection to the seawater) or allows open mixing with the seawater in the event of overflow.

    ## Dirichlet BCs
    class BCSea_p_D(OpenGeoSys.BoundaryCondition):

        def getDirichletBCValue(self, t, coords, node_id, primary_vars):
            x, y, z = coords
            tide = tidal_cycle(t)
            value = pressure_value(z, x, tide)
            if tide < z:
                return (False, 0)
            else:
                return (True, value)

    class BCLand_p_D(OpenGeoSys.BoundaryCondition):

        def getDirichletBCValue(self, t, coords, node_id, primary_vars):
            x, y, z = coords
            value = pressure_value(z, x, 0)
            return (True, value)

For the concentration boundary conditions, we assume that mixing can take place when flooded with seawater.

    ## Dirichlet BCs
    class BCSea_C(OpenGeoSys.BoundaryCondition):

        def getDirichletBCValue(self, t, coords, node_id, primary_vars):
            x, y, z = coords
            tide = tidal_cycle(t)
            value = seaward_salinity
            if tide + 1e-6 > z:
                return (True, value)
            else:
                return (False, 0)

    class BCLand_C(OpenGeoSys.BoundaryCondition):

        def getDirichletBCValue(self, t, coords, node_id, primary_vars):
            value = landward_salinity
            return (True, value)

Now only the seawater salinity has to be assigned.
In addition, the period and amplitude can be adapted to the modes of the tide.
For this example, the tidal range is disabled (amplitude = 0).
This can be added later by changing the parameters in the *tidal_cycle* function.
These parameters may be adjusted in the pyMANGA control file.
	
Now it is only necessary to define the boundary conditions as objects for OGS:

    bc_tide_p = BCSea_p_D()
    bc_land_p = BCLand_p_D()
    bc_tide_C = BCSea_C()
    bc_land_C = BCLand_C()

PyMANGA automatically adds the functionalities required for the water absorption of the trees to this script.
