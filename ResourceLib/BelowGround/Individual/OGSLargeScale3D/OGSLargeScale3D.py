#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from ResourceLib import ResourceModel
from ResourceLib.BelowGround.Individual.OGS.helpers import CellInformation
from lxml import etree
from os import path
import os
import platform
import inspect


# OGS integration for below-ground competition concept. This case is
#  using the OGS software to calculate changes in pore water salinity using
#  a detailed groundwater model.
#  @param args: Please see input file tag documentation for details
#  @date: 2019 - Today
class OGSLargeScale3D(ResourceModel):

    def __init__(self, args):
        self.case = args.find("type").text
        self._abiotic_drivers = args.find("abiotic_drivers")
        print("Initiate belowground competition of type " + self.case + ".")
        self._ogs_project_folder = args.find("ogs_project_folder").text.strip()
        if not path.isabs(self._ogs_project_folder):
            self._ogs_project_folder = \
                path.join(path.abspath("./"), self._ogs_project_folder)
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

    # This function updates and returns BelowgroundResources in the current
    #  timestep. For each tree a reduction factor is calculated which is defined
    #  as: resource uptake at zero salinity/ real resource uptake.
    def calculateBelowgroundResources(self):
        # Number of trees
        self.no_trees = len(self._tree_constant_contribution)

        # Calculate contribution and salinity prefactors
        self.calculateSplittedTreeContribution()

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

    # This functions prepares the next timestep for the competition
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
        self._tree_constant_contribution = []
        self._tree_salinity_prefactor = []
        self._tree_water_uptake = []
        self._constant_contributions = np.zeros_like(self._volumes)
        self._salinity_prefactors = np.zeros_like(self._volumes)
        self._salinity = np.zeros_like(self._volumes)
        self._tree_contribution_per_cell = np.zeros_like(self._volumes)
        self._t_end_list.append(self._t_end)
        try:
            self._t_ini_zero
        except AttributeError:
            self._t_ini_zero = self._t_ini
        filename = path.join(
            self._ogs_project_folder,
            str(t_ini).replace(".", "_") + "_" + self._ogs_project_file)

        # self._tree is the xml-tree from the ogs project file
        # above (e.g. line 108) the xml tree is updated
        # here, the new project file for ogs is saved
        self._tree.write(filename)

        self.prepareOGSparameters()

    # This function initializes variables required also in OGSExternal
    # concepts.
    def prepareOGSparameters(self):
        self._total_resistance = []
        self.belowground_resources = []
        self._tree_cell_ids = []
        self._tree_salinity = np.empty(0)
        self._tree_cell_volume = []

    # Before being able to calculate the resources, all tree entities need
    #  to be added with their current implementation for the next timestep.
    #  Here, in the OGS case, each tree is represented by a contribution to
    #  python source terms in OGS. To this end, their constant and salinity
    #  dependent resource uptake is saved in numpy arrays.
    #  @param tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        root_radius = geometry["r_root"]
        parameter = tree.getParameter()

        self.addCellCharateristics(x, y, root_radius)

        # Calculate total tree resistance
        total_resistance = self.totalTreeResistance(parameter, geometry)
        self._total_resistance.append(total_resistance)

        # Calculate tree water uptake without salinity and salinity factor
        # Unit: kg per sec
        delta_psi = parameter["leaf_water_potential"] +\
            (2 * geometry["r_crown"] + geometry["h_stem"]) * 9810
        constant_contribution = -delta_psi / total_resistance * 1000 / np.pi
        self._tree_constant_contribution.append(constant_contribution)
        salinity_prefactor = -85000 * 1000 / total_resistance * 1000 / np.pi
        self._tree_salinity_prefactor.append(salinity_prefactor)

    # This function extracts the cells affected by each tree and the
    # respective volume of these cells in tree-own variables.
    # @param x: x-coordinate of tree
    # @param y: y-coordinate of tree
    # @param radius: search radius around the previously given coordinates
    #                within which the cell finder locates cells
    def addCellCharateristics(self, x, y, root_radius):
        affected_cells = self._cell_information.getCellIDsAtXY(
            x, y, root_radius)
        self._tree_cell_ids.append(affected_cells)
        # Get volume of affected cells
        v = self.getVolume(affected_cells)
        self._tree_cell_volume.append(v)

    # This function calculates the total resistance against water flow,
    # including the resistance at the root surface and the xylem resistance
    def totalTreeResistance(self, parameter, geometry):
        root_surface_resistance = self.rootSurfaceResistance(
            parameter, geometry)
        xylem_resistance = self.xylemResistance(parameter, geometry)
        return root_surface_resistance + xylem_resistance

    # This function calculates the root surface resistance.
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

    # This function calculates the root surface resistance.
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

    # This function calculates the volume of the cells affected by one tree.
    # @param affected_cells: IDs of affected cells
    # @return: numeric
    def getVolume(self, affected_cells):
        v = 0
        for cell_id in affected_cells:
            v_i = self._volumes.GetTuple(cell_id)[0]
            v += v_i
        return v

    # This function reads cumulated salinity and calls per cell from
    # external files and calculates the salinity in each cell
    def getCellSalinity(self):
        cumsum_salinity = np.load(
            path.join(self._ogs_project_folder, "cumsum_salinity.npy"))
        calls_per_cell = np.load(
            path.join(self._ogs_project_folder, "calls_in_last_timestep.npy"))
        self._salinity = cumsum_salinity / calls_per_cell

    # This function calculates the salinity below each tree as the mean of
    # all tree-affected cells
    def calculateTreeSalinity(self):
        self._tree_salinity = np.zeros(self.no_trees)
        for tree_id in range(self.no_trees):
            ids = self._tree_cell_ids[tree_id]
            mean_salinity_for_tree = np.mean(self._salinity[ids])
            self._tree_salinity[tree_id] = mean_salinity_for_tree
        self._psi_osmo = -self._tree_salinity * 1000 * 85000

    # This function calculates the water withdrawal in each cell split
    # in a constant contribution and a salinity prefactor.
    # Unit: kg per sec per cell volume
    def calculateSplittedTreeContribution(self):
        self._constant_contributions = np.zeros(len(self._salinity))
        self._salinity_prefactors = np.zeros(len(self._salinity))

        for tree_id in range(self.no_trees):
            ids = self._tree_cell_ids[tree_id]
            v = self._tree_cell_volume[tree_id]
            per_volume = 1. / v
            constant_contribution = self._tree_constant_contribution[tree_id]
            self._constant_contributions[ids] = constant_contribution * \
                per_volume
            salinity_prefactor = self._tree_salinity_prefactor[tree_id]
            self._salinity_prefactors[ids] = salinity_prefactor * \
                per_volume

    # This function calculates the water withdrawal in each cell based on
    # individual tree water uptake.
    # Unit: kg per sec per cell volume
    # The function is not called in this concept (OGSLargeScale3D) but
    # required for various child concepts
    def calculateCompleteTreeContribution(self):
        self._tree_contribution_per_cell = np.zeros(len(self._salinity))
        for tree_id in range(self.no_trees):
            ids = self._tree_cell_ids[tree_id]
            v = self._tree_cell_volume[tree_id]
            per_volume = 1. / v
            tree_contribution = self._tree_water_uptake[tree_id]
            self._tree_contribution_per_cell[ids] = tree_contribution * \
                per_volume

    # This function returns the directory of the python_source file in the
    # directory of the concept if no external source file is provided.
    def getSourceDir(self):
        return os.path.dirname(inspect.getfile(CellInformation))

    # This function copies the python script which defines BC and source terms
    #  to the ogs project folder.
    def copyPythonScript(self):
        if self._use_external_python_script:
            source = open(
                path.join(self._ogs_project_folder,
                          self._external_python_script), "r")
        else:
            raise KeyError("No python boundary conditions have been defined.")

        target = open(path.join(self._ogs_project_folder, "python_source.py"),
                      "w")

        for line in source.readlines():
            target.write(line)
        self.completePythonScript(target)
        source.close()
        target.close()

    def completePythonScript(self, target):

        # OGS
        constants_filename = path.join(self._ogs_project_folder,
                                       "constant_contributions.npy")
        prefactors_filename = path.join(self._ogs_project_folder,
                                        "salinity_prefactors.npy")
        # Network
        complete_filename = path.join(self._ogs_project_folder,
                                      "complete_contributions.npy")

        # Both
        cumsum_filename = path.join(self._ogs_project_folder,
                                    "cumsum_salinity.npy")
        calls_filename = path.join(self._ogs_project_folder,
                                   "calls_in_last_timestep.npy")

        if len(self._abiotic_drivers) is not None:
            for abiotic_factor in self._abiotic_drivers.iterchildren():
                line = (abiotic_factor.tag + " = " + abiotic_factor.text +
                        "\n")
                target.write(line)

        # OGS
        if "Network" not in self.case:
            target.write("constant_contributions = np.load(r'" +
                         constants_filename + "')\n")
            target.write("salinity_prefactors = np.load(r'" +
                         prefactors_filename + "')\n")
            target.write("complete_contributions = None\n")
        if "Network" in self.case:
            # Network
            target.write("complete_contributions = np.load(r'" +
                         complete_filename + "')\n")
        # Both
        target.write("cumsum_savename = r'" + cumsum_filename + "'\n")
        target.write("calls_savename = r'" + calls_filename + "'\n")

        target.write("t_write = " + str(self._t_end) + "\n")

        source_directories = self.getSourceDir()
        cell_information_file = open(
            os.path.join(source_directories, "CellInformation.py"))
        for line in cell_information_file.readlines():
            target.write(line)
        cell_information_file.close()
        joined_source_mesh_name = "'" + path.join(self._ogs_project_folder,
                                                  self._source_mesh_name) + "'"
        target.write("cell_information = CellInformation(r" +
                     joined_source_mesh_name + ")")
        python_source_file = open(
            os.path.join(source_directories, "python_source.txt"))
        for line in python_source_file.readlines():
            target.write(line)
        python_source_file.close()

    # This function writes a pvd collection of the below-ground grids at the
    #  tree model time steps
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

        # write each file name in pvd-file
        files = os.listdir(self._ogs_project_folder)
        for file in files:
            if (self._ogs_prefix.text in file
                    and ("_" + str(self._t_end)) in file):
                self._ogs_bulk_mesh.text = str(file)

    def runOGSandWriteFiles(self):
        current_project_file = path.join(
            self._ogs_project_folder,
            str(self._t_ini).replace(".", "_") + "_" + self._ogs_project_file)
        print("Running ogs...")
        bc_path = (path.dirname(path.dirname(path.abspath(__file__))))
        if platform.system() == "Windows":
            if not (os.system(bc_path + "/OGS/bin/ogs " +
                              current_project_file + " -o " +
                              self._ogs_project_folder + " -l error") == 0):
                raise ValueError("Ogs calculation failed!")
        elif platform.system() == "Linux":
            if not (os.system("singularity exec --home " +
                              self._ogs_project_folder + " " + bc_path +
                              "/OGS/container/ogs_container.sif ogs " +
                              current_project_file + " -o " +
                              self._ogs_project_folder + " -l error") == 0):
                raise ValueError("""Ogs calculation failed! Please check
                                 whether the ogs container is downloaded.
                                 Please also make sure that singularity is
                                 installed. Instructions are provided in
                                 pyMANGA/TreeModelLib/BelowgroundCompetition/OGS/container
                                 """)
        print("OGS-calculation done.")
        self.writePVDCollection()

    def renameParameters(self):
        parameters = self._tree.find("parameters")
        for parameter in parameters.iterchildren():
            name = parameter.find("name")
            if name.text.strip() == "c_ini":
                parameter.find("field_name").text = "concentration"

            if name.text.strip() == "p_ini":
                parameter.find("field_name").text = "pressure"
