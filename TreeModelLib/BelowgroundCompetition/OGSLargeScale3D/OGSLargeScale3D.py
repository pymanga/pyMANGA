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


## OGS integration for belowground competition concept. This case is
#  using the OGS software to calculate changes in pore water salinity using
#  a detailed groundwater model.
#  @param args: Please see input file tag documentation for details
#  @date: 2019 - Today
class OGSLargeScale3D(BelowgroundCompetition):
    def __init__(self, args):
        case = args.find("type").text
        self._abiotic_drivers = args.find("abiotic_driver_configuration")
        print("Initiate belowground competition of type " + case + ".")
        self._ogs_project_folder = args.find("ogs_project_folder").text.strip()
        self._ogs_project_file = args.find("ogs_project_file").text.strip()
        self._ogs_source_mesh = args.find("source_mesh").text.strip()
        self._tree = etree.parse(
            path.join(self._ogs_project_folder, self._ogs_project_file))
        self._ogs_bulk_mesh = self._tree.find("meshes").find("mesh")
        time_loop = self._tree.find("time_loop")
        time_loop__processes = time_loop.find("processes")
        time_loop__processes__process = time_loop__processes.find("process")
        time_stepping = time_loop__processes__process.find("time_stepping")
        self._xml_t_initial = time_stepping.find("t_initial")
        self._xml_t_end = time_stepping.find("t_end")

        time_loop__output = time_loop.find("output")
        self._ogs_prefix = time_loop__output.find("prefix")

        self._cell_information = CellInformation(
            path.join(self._ogs_project_folder, self._ogs_source_mesh))
        self._volumes = self._cell_information.getCellVolumes()
        self._source_mesh_name = args.find("source_mesh").text
        self._tree.find("python_script").text = "python_source.py"

    ## This function updates and returns BelowgroundResources in the current
    #  timestep. For each tree a reduction factor is calculated which is defined
    #  as: resource uptake at zero salinity/ real resource uptake.
    def calculateBelowgroundResources(self):
        self.copyPythonScript()

        np.save(
            path.join(self._ogs_project_folder, "constant_contributions.npy"),
            self._constant_contributions)
        np.save(path.join(self._ogs_project_folder, "salinity_prefactors.npy"),
                self._salinity_prefactors)
        current_project_file = path.join(
            self._ogs_project_folder,
            str(self._t_ini).replace(".", "_") + "_" + self._ogs_project_file)
        os.system("./TreeModelLib/BelowgroundCompetition/OGS/bin/ogs " +
                  current_project_file + " -o " + self._ogs_project_folder)
        files = os.listdir(self._ogs_project_folder)
        for file in files:
            if (self._ogs_prefix.text in file
                    and ("_" + str(self._t_end)) in file):
                self._ogs_bulk_mesh.text = str(file)

        cumsum_salinity = np.load(
            path.join(path.dirname(path.dirname(path.abspath(__file__))),
                      "OGSLargeScale3D/cumsum_salinity.npy"))
        calls_per_cell = np.load(
            path.join(path.dirname(path.dirname(path.abspath(__file__))),
                      "OGSLargeScale3D/calls_in_last_timestep.npy"))
        salinity = cumsum_salinity / calls_per_cell
        for tree_id in range(len(self._tree_constant_contribution)):
            ids = self._tree_cell_ids[tree_id]
            mean_salinity_for_tree = np.mean(salinity[ids])
            belowground_resource = (
                (self._tree_constant_contribution[tree_id] +
                 mean_salinity_for_tree *
                 self._tree_salinity_prefactor[tree_id]) /
                self._tree_constant_contribution[tree_id])
            self.belowground_resources.append(belowground_resource)

        parameters = self._tree.find("parameters")
        for parameter in parameters.iterchildren():
            name = parameter.find("name")
            if name.text.strip() == "c_ini":
                parameter.find("field_name").text = "concentration"

            if name.text.strip() == "p_ini":
                parameter.find("field_name").text = "pressure"

    ## This functions prepares the next timestep for the competition
    #  concept. In the OGS concept, information on t_ini and t_end is stored.
    #  Additionally, arrays are prepared to store information on water uptake
    #  of the participating trees. Moreover, the ogs-prj-file for the next
    #  timestep is updated and saved in the ogs-project folder.
    #  @param t_ini: initial time of next timestep
    #  @param t_end: end time of next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self._t_ini = t_ini
        self._t_end = t_end
        self._xml_t_initial.text = str(self._t_ini)
        self._xml_t_end.text = str(self._t_end)
        self._tree_cell_ids = []
        self._tree_constant_contribution = []
        self._tree_salinity_prefactor = []
        self._constant_contributions = np.zeros_like(self._volumes)
        self._salinity_prefactors = np.zeros_like(self._volumes)
        filename = path.join(
            self._ogs_project_folder,
            str(t_ini).replace(".", "_") + "_" + self._ogs_project_file)
        self._tree.write(filename)
        ## List containing reduction factor for each tree
        self.belowground_resources = []

    ## Before being able to calculate the resources, all tree enteties need
    #  to be added with their current implementation for the next timestep.
    #  Here, in the OGS case, each tree is represented by a contribution to
    #  python source terms in OGS. To this end, their constant and salinity
    #  dependent resource uptake is saved in numpy arrays.
    #  @param x: x-coordinate of tree
    #  @param y: y-coordinate of tree
    #  @param geometry: geometric properties of tree
    #  @param parameter: dict containing tree parameters
    def addTree(self, x, y, geometry, parameter):
        affected_cells = self._cell_information.getCellIDsAtXY(x, y)
        v = 0
        self._tree_cell_ids.append(affected_cells)
        for cell_id in affected_cells:
            v_i = self._volumes.GetTuple(cell_id)[0]

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
        self._tree_constant_contribution.append(constant_contribution)
        salinity_prefactor = -85000 * 1000 / R * 1000
        self._tree_salinity_prefactor.append(salinity_prefactor)
        for cell_id in affected_cells:
            self._constant_contributions[cell_id] += constant_contribution / v
            self._salinity_prefactors[cell_id] += salinity_prefactor / v

    ## This function calculates the root surface resistance.
    #  @param lp: lp value must exist in tree parameters
    #  @param k_geom: k_geom value must exist in tree parameters
    #  @param r_root: r_root value must exist in tree geometry
    #  @param h_root: h_root value must exist in tree geometry
    def rootSurfaceResistance(self, lp, k_geom, r_root, h_root):
        root_surface_resistance = (1 / lp / k_geom / np.pi / r_root**2 /
                                   h_root)
        return root_surface_resistance

    ## This function calculates the root surface resistance.
    #  @param r_crown: r_crown value must exist in tree geometry
    #  @param h_stem: r_stem value must exist in tree geometry
    #  @param r_root: r_root value must exist in tree geometry
    #  @param kf_sap: kf_sap value must exist in tree parameters
    #  @param r_stem: r_stem value must exist in tree geometry
    def xylemResistance(self, r_crown, h_stem, r_root, kf_sap, r_stem):
        flow_length = (2 * r_crown + h_stem + 0.5**0.5 * r_root)
        xylem_resistance = (flow_length / kf_sap / np.pi / r_stem**2)
        return xylem_resistance

    ## This function copies the python script which defines BC and source terms
    #  to the ogs project folder.
    def copyPythonScript(self):
        source = open(
            path.join(path.dirname(path.dirname(path.abspath(__file__))),
                      "OGSLargeScale3D/python_source.py"), "r")
        target = open(path.join(self._ogs_project_folder, "python_source.py"),
                      "w")
        constants_filename = path.join(self._ogs_project_folder,
                                       "constant_contributions.npy")
        prefactors_filename = path.join(self._ogs_project_folder,
                                        "salinity_prefactors.npy")
        for line in source.readlines():
            if self._abiotic_drivers:
                for abiotic_factor in self._abiotic_drivers.iterchildren():
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
                    "source_mesh",
                    "'" + path.join(self._ogs_project_folder,
                                    self._source_mesh_name) + "'")
            if "t_write = t_end" in line:
                line = line.replace("t_end", str(self._t_end))
            target.write(line)
        source.close()
        target.close()


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

    ## Lookup funktion for cell_id
    #  @param x: x-coordinate
    #  @param y: y-coordinate
    #  @param z: z-coordinate
    #  @return int giving cell id
    def getCellId(self, x, y, z):
        cell_id = self._cell_finder.FindCell([x, y, z])
        return cell_id

    ## This function returns all the cell ids of the grid at a given x,y-
    #  coordinate. At the moment, the implementation is a bit weird.
    #  Suggestions to improveme the implementation are most welcome.
    #  @param x: x-coordinate for tree search
    #  @param y: y-coordinate for tree search
    def getCellIDsAtXY(self, x, y):
        bounds = self._grid.GetBounds()
        p1 = [x, y, bounds[-1]]
        p2 = [x, y, bounds[-2]]
        cell_ids = vtk.vtkIdList()
        self._cell_finder.FindCellsAlongLine(p1, p2, 1, cell_ids)

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

    ## Returns cell volumes
    #  @return np.array of shape = (len(cells))
    def getCellVolumes(self):
        return self._volumes
