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
