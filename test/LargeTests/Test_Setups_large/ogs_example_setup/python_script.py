## This is an example for an OGS python boundary condition
# The setup can be ran with:
# test/LargeTests/Test_Setups_large/ogs_example_setup/OGS3D_SAZOI_BETTINA.xml
# In this example, 2 trees are placed in the center of a 20 x 10 m domain.
# Boundary conditions are defined on the left and right sight as 'Dirichlet'
# boundary conditions for pressure and salinity concentration.
# Tidal activity is not considered. The functions below serve as example an
# can be enabled by modifying the OGS project file `testmodel.prj`.

import OpenGeoSys

import vtk as vtk
import numpy as np
from math import pi, sin
import os

seaward_salinity = 0.035
tide_daily_amplitude = .7
tide_monthly_amplitude = .37
tide_daily_period = 60 * 60 * 12.
tide_monthly_period = 60. * 60 * 24 * 31 / 2.


def tidal_cycle(t):
    return (sin(2 * pi * t / tide_daily_period) *
            (tide_daily_amplitude +
             tide_monthly_amplitude * sin(2 * pi * t / tide_monthly_period)))


def pressure_value(z, tidal_cycle):
    return 1000 * 9.81 * (tidal_cycle - z)


## Dirichlet BCs
class BCSea_p_D(OpenGeoSys.BoundaryCondition):

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        tide = tidal_cycle(t)
        value = pressure_value(z, tide)
        if tide < z:
            return (False, 0)
        else:
            return (True, value)


## Dirichlet BCs
class BCSea_C(OpenGeoSys.BoundaryCondition):

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        tide = tidal_cycle(t)
        value = seaward_salinity
        if tide > z:
            return (True, value)
        else:
            return (False, 0)

bc_tide_p = BCSea_p_D()
bc_tide_C = BCSea_C()
