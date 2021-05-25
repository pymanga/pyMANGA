import OpenGeoSys

import vtk as vtk
import numpy as np
from math import pi, sin
import os

seaward_salinity = 0.035


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
        self.number_of_cells = meshReader.GetNumberOfCells()

    def getCellId(self, x, y, z):
        cell_id = self.cell_finder.FindCell([x, y, z])
        return cell_id

    def getCellNo(self):
        return self.number_of_cells


## Source Terms
class FluxToTrees(OpenGeoSys.SourceTerm):
    def getFlux(self, t, coords, primary_vars):
        salinity = primary_vars[1]
        cell_id = cell_information.getCellId(coords[0], coords[1], coords[2])
        # total number of cells to call
        no_cells = cell_information.getCellNo()
        calls[cell_id] += 1
        cumsum_salinity[cell_id] += salinity

        # control variable to count how many times each cell was called
        max_calls[cell_id] = np.max(calls[cell_id])

        if t == t_write:
            counter[0] = counter[0] + 1
            # check if all cells have been called
            if (no_cells - 1) == cell_id:
                # print('SAVE NOW ' + str(np.mean(max_calls)))
                np.save(cumsum_savename, cumsum_salinity)
                np.save(calls_savename, calls)
        positive_flux = contributions[cell_id]
        Jac = [0.0, 0.0]
        return (-positive_flux, Jac)


contributions = np.load("contributions.npy")

cumsum_salinity = np.zeros_like(contributions)
calls = np.zeros_like(contributions)
max_calls = np.zeros_like(contributions)
counter = np.zeros(1, dtype=int)

cumsum_savename = "cumsum_salinity.npy"
calls_savename = "calls_in_last_timestep.npy"

t_write = t_end
cell_information = CellInformation(source_mesh)

# instantiate source term object referenced in OpenGeoSys' prj file
flux_to_trees = FluxToTrees()
