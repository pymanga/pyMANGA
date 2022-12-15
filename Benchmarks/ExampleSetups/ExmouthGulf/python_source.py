import OpenGeoSys

import vtk as vtk
import numpy as np
from math import pi, sin
import os
from scipy.interpolate import interp1d


#seaward_salinity = 0.05
#tide_daily_amplitude = .7
#tide_monthly_amplitude = .35
#tide_yearly_amplitude = .2
#tide_daily_period = 60 * 60 * 12.
#tide_monthly_period = 60. * 60 * 24 * 31 / 2.
#tide_yearly_period = 60. * 60 * 24 * 365.25 / 2.
#def tidal_cycle(t):
#    return (sin(2 * pi * t / tide_daily_period) *
#            (tide_daily_amplitude +
#             tide_monthly_amplitude * sin(2 * pi * t / tide_monthly_period) +
#             tide_yearly_amplitude * sin(2 * pi * t / tide_yearly_period)))
def tidal_cycle(t):
    tide_value = tidal_cycle_int(t)
    return tide_value


def pressure_value(z, tidal_cycle):
    return 1000 * 9.81 * (tidal_cycle - z)


def evaporation(salinity):
    year = (365.25 * 24 * 60 * 60)

    return -3.144 / year * 1000 * (
        0.0)  #https://researchlibrary.agric.wa.gov.au/cgi/viewcontent


## Dirichlet BCs
class BCSea_p_D(OpenGeoSys.BoundaryCondition):

    def __init__(self):
        OpenGeoSys.BoundaryCondition.__init__(self)
        self.t_check = 0
        self.tide = 0

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        if t > self.t_check:
            self.tide = tidal_cycle(t % t_mod)
            self.t_check = t
        value = pressure_value(z, self.tide)
        if self.tide < z:
            return (False, 0)
        else:
            return (True, value)


class BCSea_p_N(OpenGeoSys.BoundaryCondition):

    def __init__(self):
        OpenGeoSys.BoundaryCondition.__init__(self)
        self.t_check = 0
        self.tide = 0

    def getFlux(self, t, coords, primary_vars):
        Jac = [0.0, 0.0]
        salinity = primary_vars[1]
        x, y, z = coords
        if t > self.t_check:
            self.tide = tidal_cycle(t % t_mod)
            self.t_check = t
        value = evaporation(salinity)
        #return (False, 0, Jac)
        if self.tide < z:
            return (True, value, Jac)
        else:
            return (False, 0, Jac)


## Dirichlet BCs
class BCSea_C(OpenGeoSys.BoundaryCondition):

    def __init__(self):
        OpenGeoSys.BoundaryCondition.__init__(self)
        self.t_check = 0
        self.tide = 0

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        if t > self.t_check:
            self.tide = tidal_cycle(t % t_mod)
            self.t_check = t
        value = seaward_salinity
        if self.tide > z:
            return (True, value)
        else:
            return (False, 0)



file = open(
    "Benchmarks/ExampleSetups/ExmouthGulf/EXM_Jan-Jul_2019.txt")
t_base = 0
h_s = []
t_s = []

for line in file.readlines():
    line = (line.strip("\n").strip("/").split(","))
    h = float(line[0])
    t = float(line[1].split(".")[1][:2]) * 60 + float(
        line[1].split(".")[1][2:])
    t_s.append((t + t_base) * 60)
    h_s.append(h)
    #print(h)
    if t == 1435.0:
        t_base += 24 * 60
timeList = np.array(t_s)

signalList = (np.array(h_s) - np.mean(np.array(h_s))) / 100.
tidal_cycle_int = interp1d(timeList - min(timeList), signalList)
t_mod = (max(timeList) - min(timeList))

cumsum_savename = "cumsum_salinity.npy"
calls_savename = "calls_in_last_timestep.npy"

# instantiate source term object referenced in OpenGeoSys' prj file

bc_tide_p_D = BCSea_p_D()
bc_tide_p_N = BCSea_p_N()
bc_tide_C = BCSea_C()
seaward_salinity = 0.05
constant_contributions = np.load(r'C:\Users\marie\Documents\GRIN\git_repos\pyMANGA\Benchmarks/ExampleSetups/ExmouthGulf/constant_contributions.npy')
salinity_prefactors = np.load(r'C:\Users\marie\Documents\GRIN\git_repos\pyMANGA\Benchmarks/ExampleSetups/ExmouthGulf/salinity_prefactors.npy')
complete_contributions = None
cumsum_savename = r'C:\Users\marie\Documents\GRIN\git_repos\pyMANGA\Benchmarks/ExampleSetups/ExmouthGulf/cumsum_salinity.npy'
calls_savename = r'C:\Users\marie\Documents\GRIN\git_repos\pyMANGA\Benchmarks/ExampleSetups/ExmouthGulf/calls_in_last_timestep.npy'
t_write = 1500000.0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import vtk as vtk
import numpy as np


## Helper class providing information on given mesh. The mesh needs to contain
#  an array with name "Volume"
class CellInformation:
    ## Constructor reading source_mesh and creating id_finder for this
    #  @param source_mesh: vtkUnstructuredGrid of interest
    def __init__(self, source_mesh):
        self._mesh_name = source_mesh
        meshReader = vtk.vtkXMLUnstructuredGridReader()
        meshReader.SetFileName(self._mesh_name)
        meshReader.Update()

        self._grid = meshReader.GetOutput()
        self._cells = self._grid.GetCells()
        self._cell_finder = vtk.vtkCellLocator()
        self._cell_finder.SetDataSet(self._grid)
        self._cell_finder.LazyEvaluationOn()
        cells = self._grid.GetCellData()
        self._volumes = cells.GetArray("Volume")
        self._source_counter = None
        self._highest_node = -9999
        self._cell_ids = np.zeros((0), dtype=int)
        self._n_cells = self._grid.GetNumberOfCells()

    ## Lookup funktion for cell_id
    #  @param x: x-coordinate
    #  @param y: y-coordinate
    #  @param z: z-coordinate
    #  @return int giving cell id
    def getCellId(self, x, y, z):
        cell_id = self._cell_finder.FindCell([x, y, z])
        return cell_id

    ## Alternative lookup funktion for cell_id
    #  @param x: x-coordinate
    #  @param y: y-coordinate
    #  @param z: z-coordinate
    #  @param int_point: number of integration point
    #  @return int giving cell id
    def getCellIdAtIntPoint(self, x, y, z, int_point):
        if len(self._cell_ids) > int_point:
            cell_id = self._cell_ids[int_point]
        else:
            cell_id = self._cell_finder.FindCell([x, y, z])
            self._cell_ids = np.concatenate(
                (self._cell_ids, np.array([cell_id])))
        return cell_id

    ## This function returns all the cell ids of the grid at a given x,y-
    #  coordinate. At the moment, the implementation is a bit weird.
    #  Suggestions to improveme the implementation are most welcome.
    #  @param x: x-coordinate for tree search
    #  @param y: y-coordinate for tree search
    #  @param radius: search radius around the previously given coordinates
    #                 within which the cell finder locates cells
    def getCellIDsAtXY(self, x, y, radius):
        bounds = self._grid.GetBounds()
        # If the mesh is in 2D and in the x-y plane, it is probably so as OGS
        # only processes 2D meshes in the x-y- plane. Hence, a rotation is per-
        # formed here.
        if np.abs(bounds[-1] - bounds[-2]) < 0.0001:
            p1 = [x, bounds[2], bounds[-1]]
            p2 = [x, bounds[3], bounds[-2]]
            print("""WARNING! pyMANGA is transforming the subsurface mesh in a
                  vertical slice. In case one would like to provide a 2d
                  horizontal mesh, please review code! """)
        else:
            # Check if the mesh is 2D in
            # x-z plane
            if np.abs(bounds[2] - bounds[3]) < 0.0001:
                y = 0
            # y-z plane
            elif np.abs(bounds[0] - bounds[1]) < 0.0001:
                x = 0
            p1 = [x, y, bounds[-1]]
            p2 = [x, y, bounds[-2]]

        cell_ids = vtk.vtkIdList()
        self._cell_finder.FindCellsAlongLine(p1, p2, radius, cell_ids)
        ids = []
        for i in range(cell_ids.GetNumberOfIds()):
            ids.append(cell_ids.GetId(i))
        return ids

    ## Returns cell volumes
    #  @return np.array of shape = (len(cells))
    def getCellVolumes(self):
        return self._volumes

    ## Helper for ogs-python-source terms
    #  @param value: sets a counter for source nodes
    def setSourceCounter(self, value):
        self._source_counter = value

    ## Helper for ogs-python-source terms
    #  @return int value of internal counter for source nodes
    def getSourceCounter(self):
        return self._source_counter

    ## Helper for ogs-python-source terms
    #  @param value: sets a counter to identify highest node
    def setHighestNode(self, value):
        self._highest_node = value

    ## Helper for ogs-python-source terms
    #  @return int value of internal counter for highest node
    def getHighestNode(self):
        return self._highest_node

    ## Helpter for ogs-python-source terms
    #  @return number of cells in the source mesh
    def getNCells(self):
        return self._n_cells
cell_information = CellInformation(r'Benchmarks/ExampleSetups/ExmouthGulf/source_domain.vtu')
# Returns, depending on the cell_id, the constant contribution of a tree to the
# water flux in the root zone.
def constantContribution(cell_id):
    return constant_contributions[cell_id]

# Returns, depending on the cell_id, the salinity dependent contribution of a 
# tree to the water flux in the root zone.
def salinityContribution(cell_id, salinity):
    return salinity_prefactors[cell_id] * salinity

# Returns, depending on the cell_id, the complete contribution of a 
# tree to the water flux in the root zone. If a network system is used, only
# the complete contribution is constant. Otherwise, it depends on the salinty.
def completeContribution(cell_id, salinity):
    if complete_contributions is not None:
        return complete_contributions[cell_id]
    else:
        return (constantContribution(cell_id) + salinityContribution(
            cell_id, salinity))
        

# Source Term Helper
# This class is necessary in order to check, whether a new iteration started.
class SourceTermHelper(OpenGeoSys.BoundaryCondition):
    def __init__(self):
        super().__init__()
        self.first_node = None
            
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        # Identification of the first node's id
        if self.first_node is None:
            self.first_node = node_id
        # Reset of node counter for the source mesh with first nodes call
        if node_id == self.first_node:
            cell_information.setSourceCounter(0)
        return (False, 0)


# Source Term
# This source term describes the water fux from the bulk domain into the roots
# of trees. 
class FluxToTrees(OpenGeoSys.SourceTerm):
    def __init__(self):
        super().__init__()
        self.t = -999999
        self._cumsum_salinity = np.zeros(cell_information.getNCells())
        self._calls = np.zeros(cell_information.getNCells())
        self._first_iteration = False

    def getFlux(self, t, coords, primary_vars):
        # In the first iteration over the souce mesh, cll id_s need to be 
        # connected to coordinates in order to speedup the script. Thus, source
        # mesh cell ids are counted
        old_count = cell_information.getSourceCounter()
        new_count = old_count + 1
        cell_id = cell_information.getCellIdAtIntPoint(coords[0], coords[1], coords[2],
                                             old_count)
        cell_information.setSourceCounter(new_count)

        salinity = primary_vars[1]

        # Identification of first iteration of a new timestep
        if t > self.t:
            self.t = t
            self._first_iteration = True
        # Identification of the last timestep of the ogs model run
        if t == t_write:
            # Identification of the call of the last node in the last timestep
            if cell_information.getHighestNode() == new_count:
                np.save(cumsum_savename, self._cumsum_salinity)
                np.save(calls_savename, self._calls)
        # Values for averaring are only saved in the first iteration of each
        # timestep.
        if self._first_iteration:
            if new_count > cell_information.getHighestNode():
              cell_information.setHighestNode(new_count)
            elif cell_information.getHighestNode() == new_count:
                self._first_iteration = False
            self._calls[cell_id] += 1
            self._cumsum_salinity[cell_id] += salinity

        positive_flux = completeContribution(cell_id, salinity)
        Jac = [0.0, 0.0]
        return (-positive_flux, Jac)
# These two objects need to be defined in the ogs project file.
flux_to_trees = FluxToTrees()
bc_source_helper = SourceTermHelper()
