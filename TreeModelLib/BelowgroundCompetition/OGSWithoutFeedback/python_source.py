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




##Source Terms
class FluxToTrees(OpenGeoSys.SourceTerm):
    def getFlux(self, t, coords, primary_vars):
        if t > t_min:
            salinity = primary_vars[1]
            cell_id = cell_information.getCellId(coords[0], coords[1], coords[2])
            calls[cell_id] += 1
            cumsum_salinity[cell_id] += salinity
            if t == t_write:
                counter[0] = counter[0] + 1
                if counter[0] == len(cumsum_salinity):
                    np.save(cumsum_savename, cumsum_salinity)
                    np.save(calls_savename, calls)

        Jac = [0.0, 0.0]
        return (0, Jac)



counter = np.zeros((1), dtype=int)

mangapath = os.path.join(
    os.path.abspath("."),
    "TreeModelLib/BelowgroundCompetition/OGSWithoutFeedback")
cumsum_savename = os.path.join(mangapath, "cumsum_salinity.npy")
calls_savename = os.path.join(mangapath, "calls_in_last_timestep.npy")
t_min = 1.5e7
t_write = t_end
cell_information = CellInformation(source_mesh)
n_cells = cell_information.grid.GetNumberOfCells()
cumsum_salinity = np.zeros(n_cells)
calls = np.zeros(n_cells)
# instantiate source term object referenced in OpenGeoSys' prj file
flux_to_trees = FluxToTrees()
bc_tide_p = BCSea_p_D()
bc_tide_C = BCSea_C()
