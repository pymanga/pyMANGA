import OpenGeoSys
import sys
import numpy as np
import os

#### Start User Input ####
# OGS stuff
left_salinity = 0.025
right_salinity = 0.035

# pyMANGA stuff
# Imports

# Please define the path to the directory holding pyMANGA
manga_dir = os.path.abspath(os.path.join(os.path.dirname("python_script.py"),
                                         os.pardir, os.pardir, os.pardir))
ogs_project_folder = "OGS_input"
soure_mesh_name = "source_mesh.vtu"
source_mesh_path = os.path.join(ogs_project_folder, soure_mesh_name)

xml_file_name = "OGSExternal.xml"
xml_path = os.path.join(ogs_project_folder, xml_file_name)

# approx. of MANGA time step size in days
# if 0 MANGA is evaluated with each OGS time step greater than the time step
# before: t > t_before
manga_timestep_days = 6

#### End User Input ####


sys.path.append(manga_dir)
import MANGA as pyMANGA
from ResourceLib.BelowGround.Individual.OGS.helpers.CellInformation import CellInformation


def transectElevation(x, m=-0.1/22.):
    return float(m * x)


def pressure_value(z,x):
    return 1000 * 9.81 * (transectElevation(x) - z)


## Dirichlet BCs for pressure
class BC_p_D(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        value = pressure_value(z, x)
        # Returns two values. First is to indicate whether BC is 
        # assembled. 2nd is providing the actual value
        return (True, value)


## Dirichlet BCs for concentration
class BC_left_C_D(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        # Salinity is provided in the project file (abiotic_factors)
        # Parsing is tested here
        value = left_salinity
        # Returns two values. First is to indicate whether BC is 
        # assembled. 2nd is providing the actual value
        return (True, value)


class BC_right_C_D(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        # Salinity is provided in the project file (abiotic_factors)
        # Parsing is tested here
        value = right_salinity
        # Returns two values. First is to indicate whether BC is 
        # assembled. 2nd is providing the actual value
        return (True, value)


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


# pyMANGA as BC
# Initialize model
model = pyMANGA.Model(xml_path)
model.createExternalTimeStepper()
model.setSteps(step_ag=1, step_bg=1)


class FluxToTrees(OpenGeoSys.SourceTerm):
    def getFlux(self, t, coords, primary_vars):
        global tree_contributions
        global i
        global t_before
        # OGS stuff - call per time step and cell
        salinity = primary_vars[1]
        cell_id = cell_information.getCellId(coords[0], coords[1], coords[2])
        calls[cell_id] += 1
        cumsum_salinity[cell_id] += salinity

        # MANGA stuff - ones each time step
        # calculation in last call of las cell
        no_cells = cell_information.getNCells()
        if cell_id == no_cells - 1 and calls[no_cells - 1] == np.max(calls[0]):
            progress_Manga = False
            if manga_timestep_days == 0:
                # update MANGA-BC only if time increased
                if t > t_before:
                    progress_Manga = True
            else:
                # update MANGA-BC only after a certain time
                time_diff = t - t_before
                if time_diff >= manga_timestep_days * 3600 * 24:
                    progress_Manga = True

            if progress_Manga:
                print(">> MANGA step: " + str(i) + ", t: " +
                      str(np.round(t / 3600 / 24 / 365, 1)) +
                      " years, max. S: " +
                      str(np.round(np.max(cumsum_salinity / calls) * 1000, 1)))
                model.setBelowgroundInformation(
                    cumsum_salinity=cumsum_salinity, calls_per_cell=calls)

                model.propagateModel(t)
                tree_contributions = model.getBelowgroundInformation()
                t_before = t
                i += 1

        positive_flux = tree_contributions[cell_id]
        Jac = [0.0, 0.0]

        return -positive_flux, Jac


# counter to monitor number of MANGA executions
i = 1
# time of last time step
t_before = 0

# define global variables/ cell information
cell_information = CellInformation(source_mesh_path)
no_cells = cell_information.getNCells()
cumsum_salinity = np.zeros(no_cells) + right_salinity
calls = np.zeros(no_cells) + 1
tree_contributions = np.zeros(no_cells)

# instantiate source term object referenced in OpenGeoSys' prj file

bc_left_p = BC_p_D()
bc_right_p = BC_p_D()
bc_left_C = BC_left_C_D()
bc_right_C = BC_right_C_D()

flux_to_trees = FluxToTrees()
bc_source_helper = SourceTermHelper()
