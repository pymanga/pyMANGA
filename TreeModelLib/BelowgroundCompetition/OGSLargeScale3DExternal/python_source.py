#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import OpenGeoSys
import sys
import numpy as np
import vtk as vtk

sys.path.append("/Users/admin/Documents/GRIN/git_repos/")
import pyMANGA


# initialize MANGA model
xml_file = "ExternalOGS.xml"    # AllSimple
model = pyMANGA.Model("/Users/admin/Documents/GRIN/git_repos/pyMANGA/" +
                      "test/SmallTests/Test_Setups_small/"
                      + xml_file)
model.createExternalTimeStepper()

print('MODEL  ' + str(model))
# OGS stuff
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


class FluxToTrees(OpenGeoSys.SourceTerm):
    def getFlux(self, t, coords, primary_vars):
        global tree_contributions
        global i
        # OGS Kram berechnen - Aufruf pro Zeitschritt und Zelle
        salinity = primary_vars[1]
        cell_id = cell_information.getCellId(coords[0], coords[1], coords[2])
        calls[cell_id] += 1
        cumsum_salinity[cell_id] += salinity

        # MANGA Kram berechnen - Aufruf pro Zeitschritt
        no_cells = cell_information.getCellNo()

        # letzter Aufruf der letzten Zelle
#        if cell_id == 0 and calls[0] % 5 == 1: #np.max(calls):
        if cell_id == no_cells-1 and calls[no_cells-1] == np.max(calls[0]):
            i += 1
            if i % 2 == 0:
                print(">>>< t: " + str(t/3600/24) + " d, cell id: " + str(
                    cell_id) +
                      ", np.max(calls[0]): " + str(calls[no_cells-1]) +
                      ", css/call:  " + str(np.mean(cumsum_salinity/calls)))
                model.setBelowgroundInformation(cumsum_salinity=cumsum_salinity,
                                                calls_per_cell=calls)

                model.propagateModel(t)
                tree_contributions = []
                tree_contributions = model.getBelowgroundInformation()
                print("Mean tree contr " + str(np.mean(tree_contributions)))

        positive_flux = tree_contributions[cell_id]
        Jac = [0.0, 0.0]

        # if positive_flux != 0:
        #     print(str(cell_id) +
        #           ", call: " + str(calls[cell_id]) +
        #           " - positive_flux " + str(positive_flux*3600*24))
        return -positive_flux, Jac


# counter to reduce MANGA runs - not working correctly
i = 1

# read source mesh
source_mesh = '/Users/admin/Documents/GRIN/git_repos/pyMANGA' \
              '/test/LargeTests/Test_Setups_large/external_setup' \
              '/source_domain.vtu'

# define global variables/ cell infromation
cell_information = CellInformation(source_mesh)
no_cells = cell_information.getCellNo()
cumsum_salinity = np.zeros(no_cells) + seaward_salinity
calls = np.zeros(no_cells) + 1
tree_contributions = np.zeros(no_cells)

# instantiate source term object referenced in OpenGeoSys' prj file
flux_to_trees = FluxToTrees()
