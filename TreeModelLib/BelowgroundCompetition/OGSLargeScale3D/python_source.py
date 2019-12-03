import OpenGeoSys

import vtk as vtk
import numpy as np


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
