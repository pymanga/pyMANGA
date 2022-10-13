import OpenGeoSys
import vtk as vtk
import numpy as np
from math import pi, sin
import os

def transectElevation(x, m=-0.1/22.):
    return float(m * x)

def pressure_value(z,x):
    return 1000 * 9.81 * (transectElevation(x) - z)

## Dirichlet BCs for pressure
class BC_p_D(OpenGeoSys.BoundaryCondition):

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        value = pressure_value(z, x)
        return (True, value)

## Dirichlet BCs for concentration
class BC_left_C_D(OpenGeoSys.BoundaryCondition):

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        value = left_salinity
        return (True, value)

class BC_right_C_D(OpenGeoSys.BoundaryCondition):

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        value = right_salinity
        return (True, value)

bc_left_p = BC_p_D()
bc_right_p = BC_p_D()
bc_left_C = BC_left_C_D()
bc_right_C = BC_right_C_D()
