#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition
import vtk as vtk
from lxml import etree
from os import path
import os


class OGSLargeScale3D(BelowgroundCompetition):
    def __init__(self, args):
        ## SimpleTest case for belowground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @VAR: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        self.abiotic_drivers = args.find("abiotic_driver_configuration")
        print("Initiate belowground competition of type " + case + ".")
        self.ogs_project_folder = args.find("ogs_project_folder").text.strip()
        self.ogs_project_file = args.find("ogs_project_file").text.strip()
        self.ogs_source_mesh = args.find("source_mesh").text.strip()
        self.tree = etree.parse(
            path.join(self.ogs_project_folder, self.ogs_project_file))
        self.ogs_bulk_mesh = self.tree.find("meshes").find("mesh")
        time_loop = self.tree.find("time_loop")
        time_loop__processes = time_loop.find("processes")
        time_loop__processes__process = time_loop__processes.find("process")
        time_stepping = time_loop__processes__process.find("time_stepping")
        self.xml_t_initial = time_stepping.find("t_initial")
        self.xml_t_end = time_stepping.find("t_end")

        time_loop__output = time_loop.find("output")
        self.ogs_prefix = time_loop__output.find("prefix")

        self.cell_information = CellInformation(
            path.join(self.ogs_project_folder, self.ogs_source_mesh))
        self.volumes = self.cell_information.getCellVolumes()
        self.source_mesh_name = args.find("source_mesh").text
        self.tree.find("python_script").text = "python_source.py"

    def calculateBelowgroundResources(self):
        ## This function returns the BelowgroundResources calculated in the
        #  subsequent timestep. In the SimpleTest concept, for each tree a one
        #  is returned
        #  @return: np.array with $N_tree$ scalars
        self.copyPythonScript()

        np.save(
            path.join(self.ogs_project_folder, "constant_contributions.npy"),
            self.constant_contributions)
        np.save(path.join(self.ogs_project_folder, "salinity_prefactors.npy"),
                self.salinity_prefactors)
        current_project_file = path.join(
            self.ogs_project_folder,
            str(self.t_ini).replace(".", "_") + "_" + self.ogs_project_file)
        os.system("./TreeModelLib/BelowgroundCompetition/OGS/bin/ogs " +
                  current_project_file + " -o " + self.ogs_project_folder)
        files = os.listdir(self.ogs_project_folder)
        for file in files:
            if (self.ogs_prefix.text in file
                    and ("_" + str(self.t_end)) in file):
                self.ogs_bulk_mesh.text = str(file)

        cumsum_salinity = np.load(
            path.join(path.dirname(path.dirname(path.abspath(__file__))),
                      "OGSLargeScale3D/cumsum_salinity.npy"))
        calls_per_cell = np.load(
            path.join(path.dirname(path.dirname(path.abspath(__file__))),
                      "OGSLargeScale3D/calls_in_last_timestep.npy"))
        salinity = cumsum_salinity / calls_per_cell
        for tree_id in range(len(self.tree_constant_contribution)):
            ids = self.tree_cell_ids[tree_id]
            mean_salinity_for_tree = np.mean(salinity[ids])
            belowground_resource = ((self.tree_constant_contribution[tree_id] +
                                     mean_salinity_for_tree *
                                     self.tree_salinity_prefactor[tree_id]) /
                                    self.tree_constant_contribution[tree_id])
            self.belowground_resources.append(belowground_resource)

        parameters = self.tree.find("parameters")
        for parameter in parameters.iterchildren():
            name = parameter.find("name")
            if name.text.strip() == "c_ini":
                parameter.find("field_name").text = "concentration"

            if name.text.strip() == "p_ini":
                parameter.find("field_name").text = "pressure"

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the competition concept for the competition
        #  concept. In the SimpleTest concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @VAR: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.i = 0
        self.t_ini = t_ini
        self.t_end = t_end
        self.xml_t_initial.text = str(self.t_ini)
        self.xml_t_end.text = str(self.t_end)
        self.tree_cell_ids = []
        self.tree_constant_contribution = []
        self.tree_salinity_prefactor = []
        self.constant_contributions = np.zeros_like(self.volumes)
        self.salinity_prefactors = np.zeros_like(self.volumes)
        self.calls_in_last_timestep = np.zeros_like(self.volumes)
        self.cumsum_salinity = np.zeros_like(self.volumes)
        #  TODO: rename file
        filename = path.join(
            self.ogs_project_folder,
            str(t_ini).replace(".", "_") + "_" + self.ogs_project_file)
        self.tree.write(filename)
        self.belowground_resources = []

    def addTree(self, x, y, geometry, parameter):
        ## Before being able to calculate the resources, all tree enteties need
        #  to be added with their current implementation for the next timestep.
        #  Here, in the SimpleTest case, each tree is represented by a one. In
        #  general, an object containing all necessary information should be
        #  stored for each tree
        #  @para: position, geometry, parameter
        self.i += 1
        affected_cells = self.cell_information.getCellIDsAtXY(x, y)
        v = 0
        self.tree_cell_ids.append(affected_cells)
        for cell_id in affected_cells:
            v_i = self.volumes.GetTuple(cell_id)[0]

            v += v_i
        root_surface_resistance = self.rootSurfaceResistance(
            parameter["lp"], parameter["k_geom"], geometry["r_root"],
            geometry["h_root"])
        xylem_resistance = self.xylemResistance(geometry["r_crown"],
                                                geometry["h_stem"],
                                                geometry["r_root"],
                                                parameter["kf_sap"],
                                                geometry["r_stem"])
        R = root_surface_resistance + xylem_resistance
        constant_contribution = -(
            (parameter["leaf_water_potential"] +
             (2 * geometry["r_crown"] + geometry["h_stem"]) * 9810) / R * 1000)
        self.tree_constant_contribution.append(constant_contribution)
        salinity_prefactor = -85000 * 1000 / R * 1000
        self.tree_salinity_prefactor.append(salinity_prefactor)
        for cell_id in affected_cells:
            self.constant_contributions[cell_id] += constant_contribution / v
            self.salinity_prefactors[cell_id] += salinity_prefactor / v

    ## This function calculates the root surface resistance.
    def rootSurfaceResistance(self, lp, k_geom, r_root, h_root):
        root_surface_resistance = (1 / lp / k_geom / np.pi / r_root**2 /
                                   h_root)
        return root_surface_resistance

    ## This function calculates the xylem resistance.
    def xylemResistance(self, r_crown, h_stem, r_root, kf_sap, r_stem):
        flow_length = (2 * r_crown + h_stem + 0.5**0.5 * r_root)
        xylem_resistance = (flow_length / kf_sap / np.pi / r_stem**2)
        return xylem_resistance

    def copyPythonScript(self):
        source = open(
            path.join(path.dirname(path.dirname(path.abspath(__file__))),
                      "OGSLargeScale3D/python_source.py"), "r")
        target = open(path.join(self.ogs_project_folder, "python_source.py"),
                      "w")
        constants_filename = path.join(self.ogs_project_folder,
                                       "constant_contributions.npy")
        prefactors_filename = path.join(self.ogs_project_folder,
                                        "salinity_prefactors.npy")
        for line in source.readlines():
            if self.abiotic_drivers:
                for abiotic_factor in self.abiotic_drivers.iterchildren():
                    if (abiotic_factor.tag + " = ") in line:
                        line = abiotic_factor.tag + " = " + abiotic_factor.text + "\n"
            if "constant_contributions.npy" in line:
                line = line.replace("constant_contributions.npy",
                                    constants_filename)
            if "salinity_prefactors.npy" in line:
                line = line.replace("salinity_prefactors.npy",
                                    prefactors_filename)
            if "CellInformation(source_mesh)" in line:
                line = line.replace(
                    "source_mesh", "'" +
                    path.join(self.ogs_project_folder, self.source_mesh_name) +
                    "'")
            if "t_write = t_end" in line:
                line = line.replace("t_end", str(self.t_end))
            target.write(line)
        source.close()
        target.close()


class CellInformation:
    def __init__(self, source_mesh):
        self.mesh_name = source_mesh
        meshReader = vtk.vtkXMLUnstructuredGridReader()
        meshReader.SetFileName(self.mesh_name)
        meshReader.Update()

        self.grid = meshReader.GetOutput()
        self.cells = self.grid.GetCells()
        self.cell_finder = vtk.vtkCellLocator()
        self.cell_finder.SetDataSet(self.grid)
        self.cell_finder.LazyEvaluationOn()
        cells = self.grid.GetCellData()
        self.volumes = cells.GetArray("Volume")

    def getCellId(self, x, y, z):
        cell_id = self.cell_finder.FindCell([x, y, z])
        return cell_id

    ## This function returns all the cell ids of the grid at a given x,y-
    #  coordinate. At the moment, the implementation is a bit weird.
    #  Suggestions to improveme the implementation are most welcome.
    def getCellIDsAtXY(self, x, y):
        bounds = self.grid.GetBounds()
        p1 = [x, y, bounds[-1]]
        p2 = [x, y, bounds[-2]]
        cell_ids = vtk.vtkIdList()
        self.cell_finder.FindCellsAlongLine(p1, p2, 1, cell_ids)

        def linepoints(y):
            return np.array(p1)[np.newaxis, :] + y[:, np.newaxis] * (
                np.array(p2)[np.newaxis, :] - np.array(p1)[np.newaxis, :])

        search = 1
        yi = np.array([0, .5, 1])
        points = (linepoints(yi))
        ids = []
        i = 0
        for point in points:
            iD = (self.getCellId(point[0], point[1], point[2]))
            if (iD not in ids) and (iD != -1):
                ids.append(iD)
        while (search):
            new_yi = (yi[:-1] + yi[1:]) / 2.
            points = linepoints(new_yi)
            for point in points:
                iD = (self.getCellId(point[0], point[1], point[2]))
                if (iD not in ids) and (iD != -1):
                    ids.append(iD)
            i += 1
            dist = np.abs((points[:-1] - points[1:]))[0, 2]
            if len(ids) == 3:
                search = 0
            elif dist < 1e-3:
                search = 0
                if len(ids) < 1:
                    raise ValueError("It seems like some trees are located " +
                                     "outside the ogs bulk mesh!" +
                                     " Please check for consistency.")
            elif i == 1e4:
                search = 0
                raise ValueError("Search algorithm failed! Please improve" +
                                 " algorithm!")
            yi = np.concatenate((yi, new_yi))
            yi.sort()
        return ids

    def getCellVolumes(self):
        return self.volumes
