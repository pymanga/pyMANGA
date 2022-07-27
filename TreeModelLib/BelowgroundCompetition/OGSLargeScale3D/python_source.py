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
        self.number_of_cells = meshReader.GetNumberOfCells()

    def getCellId(self, x, y, z):
        cell_id = self.cell_finder.FindCell([x, y, z])
        return cell_id

    def getCellNo(self):
        return self.number_of_cells


def constantContribution(cell_id):
    return constant_contributions[cell_id]


def salinityContribution(cell_id, salinity):
    return salinity_prefactors[cell_id] * salinity


##Source Terms
class FluxToTrees(OpenGeoSys.SourceTerm):

    def getFlux(self, t, coords, primary_vars):
        salinity = primary_vars[1]
        cell_id = cell_information.getCellId(coords[0], coords[1], coords[2])
        # total number of cells to call
        no_cells = cell_information.getCellNo()
        calls[cell_id] += 1
        cumsum_salinity[cell_id] += salinity

        if t == t_write:
            # check if all cells have been called
            if (no_cells - 1) == cell_id:
                # control variable to count how many times each cell was called
                max_calls = np.max(calls[cell_id - 1])
                if calls[cell_id] == max_calls:
                    np.save(cumsum_savename, cumsum_salinity)
                    np.save(calls_savename, calls)
        positive_flux = constantContribution(cell_id) + salinityContribution(
            cell_id, salinity)
        Jac = [0.0, 0.0]
        return (-positive_flux, Jac)


constant_contributions = np.load(
    "test/LargeTests/Test_Setups_large/ogs_example_setup/constant_contributions.npy"
)
salinity_prefactors = np.load(
    "test/LargeTests/Test_Setups_large/ogs_example_setup/salinity_prefactors.npy"
)
cumsum_salinity = np.zeros_like(salinity_prefactors)
calls = np.zeros_like(salinity_prefactors)
counter = np.zeros((1), dtype=int)
max_calls = np.zeros_like(constant_contributions)

cumsum_savename = "test/LargeTests/Test_Setups_large/ogs_example_setup/cumsum_salinity.npy"
calls_savename = "test/LargeTests/Test_Setups_large/ogs_example_setup/calls_in_last_timestep.npy"

t_write = t_end
cell_information = CellInformation(source_mesh)
# instantiate source term object referenced in OpenGeoSys' prj file
flux_to_trees = FluxToTrees()
bc_tide_p = BCSea_p_D()
bc_tide_C = BCSea_C()
