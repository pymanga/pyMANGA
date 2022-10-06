import OpenGeoSys
import vtk as vtk
import numpy as np
from math import pi, sin
import os


def tidal_cycle(t):
    daily = 12 * 60 * 60
    monthly = daily * 30
    tide_value = amplitude * (sin(2 * pi / daily * t) +
                              .2 * sin(2 * pi / monthly * t))
    return tide_value


def pressure_value(z, tidal_cycle):
    return 1000 * 9.81 * (tidal_cycle - z)


## Dirichlet BCs
class BCSea_p_D(OpenGeoSys.BoundaryCondition):

    def __init__(self):
        OpenGeoSys.BoundaryCondition.__init__(self)
        self.t_check = 0
        self.tide = 0

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        if t > self.t_check:
            self.tide = tidal_cycle(t)
            self.t_check = t
        value = pressure_value(z, self.tide)
        if self.tide < z:
            return (False, 0)
        else:
            return (True, value)


## Dirichlet BCs
class BCSea_C(OpenGeoSys.BoundaryCondition):

    def __init__(self):
        OpenGeoSys.BoundaryCondition.__init__(self)
        self.t_check = 0
        self.tide = 0

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        if t > self.t_check:
            self.tide = tidal_cycle(t)
            self.t_check = t
        value = seaward_salinity
        if self.tide > z:
            return (True, value)
        else:
            return (False, 0)


amplitude = 0.5
# instantiate source term object referenced in OpenGeoSys' prj file
bc_tide_p_D = BCSea_p_D()
bc_tide_C = BCSea_C()
