import OpenGeoSys
import vtk as vtk
import numpy as np
from math import pi, sin
import os


#seaward_salinity = 0.05
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


def constantContribution(cell_id):
    return constant_contributions[cell_id]


def salinityContribution(cell_id, salinity):
    return salinity_prefactors[cell_id] * salinity


##Source Terms
class FluxToTrees(OpenGeoSys.SourceTerm):

    def getFlux(self, t, coords, primary_vars):
        salinity = primary_vars[1]
        cell_id = cell_information.getCellId(coords[0], coords[1], coords[2])
        calls[cell_id] += 1
        cumsum_salinity[cell_id] += salinity
        if t == t_write:
            counter[0] = counter[0] + 1
            if counter[0] == len(cumsum_salinity):
                np.save(cumsum_savename, cumsum_salinity)
                np.save(calls_savename, calls)
        positive_flux = constantContribution(cell_id) + salinityContribution(
            cell_id, salinity)
        Jac = [0.0, 0.0]
        return (-positive_flux, Jac)


constant_contributions = np.load("constant_contributions.npy")
salinity_prefactors = np.load("salinity_prefactors.npy")
cumsum_salinity = np.zeros_like(salinity_prefactors)
calls = np.zeros_like(salinity_prefactors)
counter = np.zeros((1), dtype=int)

cumsum_savename = "cumsum_salinity.npy"
calls_savename = "calls_in_last_timestep.npy"

amplitude = 0.5
t_write = t_end
cell_information = CellInformation(source_mesh)
# instantiate source term object referenced in OpenGeoSys' prj file
flux_to_trees = FluxToTrees()
bc_tide_p_D = BCSea_p_D()
bc_tide_C = BCSea_C()
