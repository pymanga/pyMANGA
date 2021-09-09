#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib import TreeModel
from TreeModelLib.BelowgroundCompetition.OGS.helpers import CellInformation
import vtk as vtk
from lxml import etree
from os import path
import os


## OGS integration for belowground competition concept. This case is
#  using the OGS software to calculate changes in pore water salinity using
#  a detailed groundwater model.
#  @param args: Please see input file tag documentation for details
#  @date: 2019 - Today
class OGSLargeScale3D(TreeModel):
    def __init__(self, args):
        case = args.find("type").text
        self._abiotic_drivers = args.find("abiotic_drivers")
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

        self._use_external_python_script = False
        if args.find("python_script") is not None:
            print("Using external python script")
            self._external_python_script = (
                args.find("python_script").text.strip())
            self._use_external_python_script = True

        self._use_fixed_ogs_delta_t = False
        if args.find("delta_t_ogs") is not None:
            print("Using predefined ogs timesteps")
            self._fixed_ogs_delta_t = float(
                args.find("delta_t_ogs").text.strip())
            self._use_fixed_ogs_delta_t = True
        self._tree.find("python_script").text = "python_source.py"
        self._t_end_list = []

    ## This function updates and returns BelowgroundResources in the current
    #  timestep. For each tree a reduction factor is calculated which is defined
    #  as: resource uptake at zero salinity/ real resource uptake.
    def calculateBelowgroundResources(self):
        # Number of trees
        self.no_trees = len(self._tree_constant_contribution)

        self.copyPythonScript()
        # Write contributions to file
        np.save(
            path.join(self._ogs_project_folder, "constant_contributions.npy"),
            self._constant_contributions)
        np.save(path.join(self._ogs_project_folder, "salinity_prefactors.npy"),
                self._salinity_prefactors)
        # Start OGS
        self.runOGSandWriteFiles()
        # Read salinity from OGS results file
        self.getCellSalinity()
        # Calculate salinity below each tree
        self.calculateTreeSalinity()
        # Calculate tree water uptake in kg per sec
        self._tree_water_uptake = self._tree_constant_contribution + \
                                 self._tree_salinity_prefactor * \
                                 self._tree_salinity
        # Calculate below ground resource factor
        self.belowground_resources = self._tree_water_uptake / \
                                     self._tree_constant_contribution

        self.renameParameters()

    ## This functions prepares the next timestep for the competition
    #  concept. In the OGS concept, information on t_ini and t_end is stored.
    #  Additionally, arrays are prepared to store information on water uptake
    #  of the participating trees. Moreover, the ogs-prj-file for the next
    #  timestep is updated and saved in the ogs-project folder.
    #  @param t_ini: initial time of next timestep
    #  @param t_end: end time of next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self._t_ini = t_ini
        if self._use_fixed_ogs_delta_t:
            self._t_end = t_ini + self._fixed_ogs_delta_t
        else:
            self._t_end = t_end
        self._xml_t_initial.text = str(self._t_ini)
        self._xml_t_end.text = str(self._t_end)
        self._tree_cell_ids = []
        self._tree_constant_contribution = []
        self._tree_salinity_prefactor = []
        self._constant_contributions = np.zeros_like(self._volumes)
        self._salinity_prefactors = np.zeros_like(self._volumes)
        self._salinity = np.zeros_like(self._volumes)
        self._t_end_list.append(self._t_end)
        try:
            self._t_ini_zero
        except AttributeError:
            self._t_ini_zero = self._t_ini
        filename = path.join(
            self._ogs_project_folder,
            str(t_ini).replace(".", "_") + "_" + self._ogs_project_file)
        self._tree.write(filename) # ToDo @JB: Was passiert hier?
        ## List containing reduction factor for each tree
        self.belowground_resources = []
        self._tree_salinity = []

    ## Before being able to calculate the resources, all tree enteties need
    #  to be added with their current implementation for the next timestep.
    #  Here, in the OGS case, each tree is represented by a contribution to
    #  python source terms in OGS. To this end, their constant and salinity
    #  dependent resource uptake is saved in numpy arrays.
    #  @param tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()

        affected_cells = self._cell_information.getCellIDsAtXY(x, y)
        self._tree_cell_ids.append(affected_cells)

        root_surface_resistance = self.rootSurfaceResistance(
            parameter, geometry)
        xylem_resistance = self.xylemResistance(parameter, geometry)
        R = root_surface_resistance + xylem_resistance

        # Calculate tree water uptake without salinity and salinity factor
        # Unit: kg per sec
        constant_contribution = -(
            (parameter["leaf_water_potential"] +
             (2 * geometry["r_crown"] + geometry["h_stem"]) * 9810) / R *
            1000) / np.pi
        self._tree_constant_contribution.append(constant_contribution)
        salinity_prefactor = -85000 * 1000 / R * 1000 / np.pi
        self._tree_salinity_prefactor.append(salinity_prefactor)

        # Get volume of affected cells
        v = self.getVolume(affected_cells)
        per_volume = 1. / v
        for cell_id in affected_cells:
            self._constant_contributions[
                cell_id] += constant_contribution * per_volume
            self._salinity_prefactors[
                cell_id] += salinity_prefactor * per_volume

    ## This function calculates the root surface resistance.
    #  @param parameter: list of hydraulic and initial tree parameters
    #  @param geometry: tree geometry
    def rootSurfaceResistance(self, parameter, geometry):
        lp = parameter["lp"]
        k_geom = parameter["k_geom"]
        r_root = geometry["r_root"]
        h_root = geometry["h_root"]
        root_surface_resistance = (1 / lp / k_geom / np.pi / r_root**2 /
                                   h_root)
        return root_surface_resistance

    ## This function calculates the root surface resistance.
    #  @param parameter: list of hydraulic and initial tree parameters
    #  @param geometry: tree geometry
    def xylemResistance(self, parameter, geometry):
        r_crown = geometry["r_crown"]
        h_stem = geometry["h_stem"]
        r_root = geometry["r_root"]
        kf_sap = parameter["kf_sap"]
        r_stem = geometry["r_stem"]
        flow_length = (2 * r_crown + h_stem + 0.5**0.5 * r_root)
        xylem_resistance = (flow_length / kf_sap / np.pi / r_stem**2)
        return xylem_resistance

    ## This function calculates the volume of the cells affected by one tree.
    # @param affected_cells: IDs of affected cells
    # @return: numeric
    def getVolume(self, affected_cells):
        v = 0
        for cell_id in affected_cells:
            v_i = self._volumes.GetTuple(cell_id)[0]
            v += v_i
        return v

    ## This function reads cumulated salinity and calls per cell from
    # external files and calculates the salinity in each cell
    def getCellSalinity(self):
        cumsum_salinity = np.load(
            path.join(self._ogs_project_folder, "cumsum_salinity.npy"))
        calls_per_cell = np.load(
            path.join(self._ogs_project_folder, "calls_in_last_timestep.npy"))
        self._salinity = cumsum_salinity / calls_per_cell

    ## This function calculates the salinity below each tree as the mean of
    # all tree-affected cells
    def calculateTreeSalinity(self):
        self._tree_salinity = np.zeros(self.no_trees)
        for tree_id in range(self.no_trees):
            ids = self._tree_cell_ids[tree_id]
            mean_salinity_for_tree = np.mean(self._salinity[ids])
            self._tree_salinity[tree_id] = mean_salinity_for_tree
        self._psi_osmo = -self._tree_salinity * 1000 * 85000

    ## This function calculates the water withdrawal in each cell based on
    # individual tree water uptake.
    # Unit: kg per sec per cell volume
    # The function is not called in this concept (OGSLargeScale3D) but
    # required for various child concepts
    def calculateTreeContribution(self):
        self.tree_contribution_per_cell = np.zeros(len(self._salinity))
        for tree_id in range(self.no_trees):
            ids = self._tree_cell_ids[tree_id]
            v = self.getVolume(affected_cells=ids)
            per_volume = 1. / v
            tree_contribution = self._tree_water_uptake[tree_id]
            self.tree_contribution_per_cell[ids] = tree_contribution * \
                                                    per_volume

    ## This function returns the directory of the python_source file in the
    # directory of the concept if no external source file is provided.
    def getSourceDir(self):
        return path.join(path.dirname(path.abspath(__file__)),
                          "python_source.py")

    ## This function copies the python script which defines BC and source terms
    #  to the ogs project folder.
    def copyPythonScript(self):
        if self._use_external_python_script:
            source = open(
                path.join(self._ogs_project_folder,
                          self._external_python_script), "r")
        else:
            source_dir = self.getSourceDir()
            source = open(source_dir, "r")
        target = open(path.join(self._ogs_project_folder, "python_source.py"),
                      "w")

        # OGS
        try:
            constants_filename = path.join(self._ogs_project_folder,
                                           "constant_contributions.npy")
            prefactors_filename = path.join(self._ogs_project_folder,
                                            "salinity_prefactors.npy")
        except:
            pass

        # Network
        try:
            complete_filename = path.join(self._ogs_project_folder,
                                               "complete_contributions.npy")
        except:
            pass

        cumsum_filename = path.join(self._ogs_project_folder,
                                    "cumsum_salinity.npy")
        calls_filename = path.join(self._ogs_project_folder,
                                   "calls_in_last_timestep.npy")
        # Iterates through each line in the python_source.py to replace
        # directories
        for line in source.readlines():
            if self._abiotic_drivers:
                for abiotic_factor in self._abiotic_drivers.iterchildren():
                    if (abiotic_factor.tag + " = ") in line:
                        line = (abiotic_factor.tag + " = " +
                                abiotic_factor.text + "\n")

            # OGS
            if "constant_contributions.npy" in line:
                line = line.replace("constant_contributions.npy",
                                    constants_filename)
            if "salinity_prefactors.npy" in line:
                line = line.replace("salinity_prefactors.npy",
                                    prefactors_filename)
            # Network
            if "complete_contributions.npy" in line:
                line = line.replace("complete_contributions.npy",
                                    complete_filename)
            # Both
            if "cumsum_salinity.npy" in line:
                line = line.replace("cumsum_salinity.npy", cumsum_filename)
            if "calls_in_last_timestep.npy" in line:
                line = line.replace("calls_in_last_timestep.npy",
                                    calls_filename)
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

    ## This function writes a pvd collection of the belowground grids at the
    #  tree model timesteps
    def writePVDCollection(self):
        pvd_file = open(
            os.path.join(self._ogs_project_folder, "vtu_collection.pvd"), "w")
        pvd_file.write('<?xml version="1.0"?>\n')
        pvd_file.write(
            '<VTKFile type="Collection" version="0.1"' +
            ' byte_order="LittleEndian" compressor="vtkZLibDataCompressor">\n')
        pvd_file.write('\t<Collection>\n')
        time = self._t_ini_zero
        pvd_file.write('\t\t<DataSet timestep="' + str(time) +
                       '" group="" part="0" file="' + self._ogs_prefix.text +
                       '_pcs_0_ts_0_t_%1.6f.vtu"/>\n' % time)
        for time in self._t_end_list:
            vtu_files = os.listdir(self._ogs_project_folder)
            for filename in vtu_files:
                if ("_" + str(time) in filename
                        and self._ogs_prefix.text in filename
                        and "_pcs_0_ts_0_t_" not in filename):
                    pvd_file.write('\t\t<DataSet timestep="' + str(time) +
                                   '" group="" part="0" file="' + filename +
                                   '"/>\n')
        pvd_file.write("\t</Collection>\n")
        pvd_file.write("</VTKFile>\n")
        pvd_file.close()

    def runOGSandWriteFiles(self):
        current_project_file = path.join(
            self._ogs_project_folder,
            str(self._t_ini).replace(".", "_") + "_" + self._ogs_project_file)
        print("Running ogs...")
        bc_path = (path.dirname(path.dirname(path.abspath(__file__))))

        if not (os.system(bc_path + "/OGS/bin/ogs " + current_project_file +
                          " -o " + self._ogs_project_folder + " -l error")
                == 0):
            raise ValueError("Ogs calculation failed!")
        print("OGS-calculation done.")
        self.writePVDCollection()
        # ToDo: @JB: Was passiert hier?
        files = os.listdir(self._ogs_project_folder)
        for file in files:
            if (self._ogs_prefix.text in file
                    and ("_" + str(self._t_end)) in file):
                self._ogs_bulk_mesh.text = str(file)

    def renameParameters(self):
        parameters = self._tree.find("parameters")
        for parameter in parameters.iterchildren():
            name = parameter.find("name")
            if name.text.strip() == "c_ini":
                parameter.find("field_name").text = "concentration"

            if name.text.strip() == "p_ini":
                parameter.find("field_name").text = "pressure"
