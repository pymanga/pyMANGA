import OpenGeoSys

import vtk as vtk
import numpy as np
from math import pi, sin

seaward_salinity = 0.035
tide_daily_amplitude = 1
tide_monthly_amplitude = .5
tide_daily_frequency = 60 * 60 * 12.
tide_monthly_frequency = 60. * 60 * 24 * 31 / 2.


def tidal_cycle(t):
    return (
        sin(2 * pi * t / tide_daily_frequency) *
        (tide_daily_amplitude +
         tide_monthly_amplitude * sin(2 * pi * t / tide_monthly_frequency)))


def pressure_value(z, tidal_cycle):
    return 1000 * 9.81 * (tidal_cycle - z)


# Dirichlet BCs
class BCSea_p_D(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        tide = tidal_cycle(t)
        value = pressure_value(z, tide)
        if tide < z:
            return (False, 0)
        else:
            return (True, value)


class BCSea_C(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        tide = tidal_cycle(t)
        value = seaward_salinity
        if tide > z:
            return (True, value)
        else:
            return (False, 0)


##Source Terms
class CellInformation:
    def __init__(self, source_mesh):
        meshReader = vtk.vtkXMLUnstructuredGridReader()
        meshReader.SetFileName(source_mesh)
        meshReader.Update()
        self.grid = meshReader.GetOutput()
        self.cell_finder = vtk.vtkCellLocator()
        self.cell_finder.SetDataSet(self.grid)
        self.cell_finder.LazyEvaluationOn()
        cells = self.grid.GetCellData()
        self.volumes = cells.GetArray("Volume")

    def getCellId(self, x, y, z):
        cell_id = self.cell_finder.FindCell([x, y, z])
        return cell_id


def constantContribution(coords):
    cell_id = cell_information.getCellId(coords[0], coords[1], coords[2])
    return constant_contributions[cell_id]


def salinityContribution(coords, salinity):
    cell_id = cell_information.getCellId(coords[0], coords[1], coords[2])
    return salinity_prefactors[cell_id]


class FluxToTrees(OpenGeoSys.SourceTerm):
    def getFlux(self, t, coords, primary_vars):
        salinity = primary_vars[1]
        value = constantContribution(coords) + salinityContribution(
            coords, salinity)
        Jac = [0.0, 0.0]
        return (value, Jac)


constant_contributions = np.load("constant_contributions.npy")
salinity_prefactors = np.load("salinity_prefactors.npy")
cell_information = CellInformation(source_mesh)

# instantiate source term object referenced in OpenGeoSys' prj file
flux_to_trees = FluxToTrees()
bc_tide_p = BCSea_p_D()
bc_tide_C = BCSea_C()
