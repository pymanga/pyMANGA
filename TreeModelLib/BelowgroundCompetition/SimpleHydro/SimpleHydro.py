#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
import math
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition


class SimpleHydro(BelowgroundCompetition):
    ## Simple approach to reduce water availability due to osmotic potential.
    #  Processes are gradient flow, salinisation by plant transpiration,
    #  dilution by tides and horizontal mixing (diffusion).\n
    #  @param: Tags to define SimpleHydro, see tag documentation \n
    #  @date: 2021 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.makeGrid(args)

    ## This function returns a list of the growth reduction factors of all trees.
    #  calculated in the subsequent timestep.\n
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        self.transpire()
        self.belowground_resources = ((np.array(self._potential_nosal) +
                                       np.array(self._salinity) * 85000000) /
                                      np.array(self._potential_nosal))

    ## This function calculates the water balance of each grid cell.
    # Transpiration, dilution (tidal flooding), exchange between neighbouring
    # grid cells and gradient flow is regarded for.
    def transpire(self):
        ## time step length
        tsl = (self._t_end - self._t_ini)
        ## seconds per day
        s_d = 3600 * 24
        ## number of days
        ndays = int(tsl / s_d)
        ## fraction of the last day
        rest = tsl / s_d - int(tsl / s_d)
        ##calculate water uptake from grid cells
        ####negative distance of gridcells to root zone, positive values -> grid cell inside root zone
        distance = (np.array(self._r_root)[np.newaxis, np.newaxis, :] -
                    ((self._my_grid[0][:, :, np.newaxis] -
                      np.array(self._xe)[np.newaxis, np.newaxis, :])**2 +
                     (self._my_grid[1][:, :, np.newaxis] -
                      np.array(self._ye)[np.newaxis, np.newaxis, :])**2)**0.5)
        ###initialise water loss matrix from gridcells (transpiration)
        water_loss = np.zeros(np.shape(distance[:, :, 0]))
        ### which tree is present where?
        presence = distance > 0
        ### what is the distance to the closest gridcell
        maxe = np.amax(distance, axis=(0, 1))
        ### initialise things
        self._salinity = []
        self.transpiration = []
        ### for the trees ...
        for ii in range(distance.shape[2]):
            ### making the tree being present at the closest gridcell (to define at least one grid cell for the tree to be present)
            closest = distance[:, :, ii] == maxe[ii]
            presence[:, :, ii] = np.fmax(closest, presence[:, :, ii])
            ### average salinity in the root zone
            self._salinity.append((np.sum(presence[:, :, ii] * self.salinity) /
                                   np.sum(presence[:, :, ii])))
            ### transpiration for the tree
            self.transpiration.append(
                (-self._potential_nosal[ii] - self._salinity[ii] * 85000000) /
                self._resistance[ii] / np.pi * tsl)
            ### transpiration per grid cell
            water_loss += (self.transpiration[ii] /
                           np.sum(presence[:, :, ii])) * presence[:, :, ii]
        ## what OGS would do:
        for ii in range(ndays):
            ## refill transpiration losses with seawater
            self.salinity += self._sea_salinity * water_loss / self.volume / (
                tsl / s_d)
            ## do all the other stuff, see there. argument "1" means entire day
            self.updateSalinity(1)

        ## refill (if there are fractions of a day left)
        self.salinity += self._sea_salinity * water_loss / self.volume / (
            tsl / s_d) * rest
        self.updateSalinity(rest)

    def updateSalinity(self, rest):
        s_d = 3600 * 24
        ## dilution
        ### the fraction of diluted water gets replaced with sea water
        self.salinity += (-self.salinity * self.dilution_frac +
                          self._sea_salinity * self.dilution_frac) * rest
        ## diffusion
        ### keep water that is not diffusing to neighbouring cells
        salinity_new = self.salinity * (1 - self._diffusion_frac * rest)
        ### distribute a quarter of the diffused water to the neighbours or keep it, if at the edge
        # diff in x-dir
        for ii in range(self.x_resolution):
            if ii == self.x_resolution - 1:
                salinity_new[:, ii] += (self.salinity[:, ii] *
                                        self._diffusion_frac * rest / 4)
                salinity_new[:, ii - 1] += (self.salinity[:, ii] *
                                            self._diffusion_frac * rest / 4)
            elif ii == 0:
                salinity_new[:, ii + 1] += (self.salinity[:, ii] *
                                            self._diffusion_frac * rest / 4)
                salinity_new[:, ii] += (self.salinity[:, ii] *
                                        self._diffusion_frac * rest / 4)
            else:
                salinity_new[:, ii + 1] += (self.salinity[:, ii] *
                                            self._diffusion_frac * rest / 4)
                salinity_new[:, ii - 1] += (self.salinity[:, ii] *
                                            self._diffusion_frac * rest / 4)

        # diff in y-dir
        for ii in range(self.y_resolution):
            if ii == self.y_resolution - 1:
                salinity_new[ii, :] += (self.salinity[ii, :] *
                                        self._diffusion_frac * rest / 4)
                salinity_new[ii - 1, :] += (self.salinity[ii, :] *
                                            self._diffusion_frac * rest / 4)
            elif ii == 0:
                salinity_new[ii + 1, :] += (self.salinity[ii, :] *
                                            self._diffusion_frac * rest / 4)
                salinity_new[ii, :] += (self.salinity[ii, :] *
                                        self._diffusion_frac * rest / 4)
            else:
                salinity_new[ii + 1, :] += (self.salinity[ii, :] *
                                            self._diffusion_frac * rest / 4)
                salinity_new[ii - 1, :] += (self.salinity[ii, :] *
                                            self._diffusion_frac * rest / 4)
        self.salinity = salinity_new
        ## gradient-flow hilldown
        multi_fac = self.q_fac * s_d * rest
        salinity_new[0, :] = self.salinity[0, :] * (
            1 - multi_fac) + self._up_sal * multi_fac
        salinity_new[1:self.y_resolution, :] = (
            self.salinity[1:self.y_resolution, :] * (1 - multi_fac) +
            self.salinity[0:(self.y_resolution - 1), :] * multi_fac)
        self.salinity = salinity_new

    ## This function initialises the mesh.\n
    def makeGrid(self, args):
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution",
            "y_resolution", "depth", "porosity", "dilution_frac_upper",
            "dilution_frac_lower", "diffusion_frac", "sea_salinity", "ini_sal",
            "up_sal", "slope", "k_f", "flooding_duration"
        ]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "x_resolution":
                self.x_resolution = int(arg.text)
            elif tag == "y_resolution":
                self.y_resolution = int(arg.text)
            elif tag == "x_1":
                x_1 = float(arg.text)
            elif tag == "x_2":
                x_2 = float(arg.text)
            elif tag == "y_1":
                y_1 = float(arg.text)
            elif tag == "y_2":
                y_2 = float(arg.text)
            elif tag == "depth":
                self._depth = float(arg.text)
            elif tag == "porosity":
                self._porosity = float(arg.text)
            elif tag == "dilution_frac_upper":
                _dilution_frac_upper = float(arg.text)
            elif tag == "dilution_frac_lower":
                _dilution_frac_lower = float(arg.text)
            elif tag == "diffusion_frac":
                self._diffusion_frac = float(arg.text)
            elif tag == "sea_salinity":
                self._sea_salinity = float(arg.text)
            elif tag == "ini_sal":
                self._ini_sal = float(arg.text)
            elif tag == "up_sal":
                self._up_sal = float(arg.text)
            elif tag == "slope":
                self._slope = float(arg.text)
            elif tag == "k_f":
                self._k_f = float(arg.text)
            elif tag == "flooding_duration":
                from ast import literal_eval
                self._flooding_duration = np.array(literal_eval(arg.text))
            try:
                missing_tags.remove(tag)
            except:
                print("WARNING: Tag " + tag +
                      " not specified for below-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground grid initialisation in "
                "project file.")
        l_x = x_2 - x_1
        l_y = y_2 - y_1
        x_step = l_x / self.x_resolution
        y_step = l_y / self.y_resolution
        self._mesh_size = np.maximum(x_step, y_step)
        xe = np.linspace(x_1 + x_step / 2.,
                         x_2 - x_step / 2.,
                         self.x_resolution,
                         endpoint=True)
        ye = np.linspace(y_1 + y_step / 2.,
                         y_2 - y_step / 2.,
                         self.y_resolution,
                         endpoint=True)
        self._my_grid = np.meshgrid(xe, ye)
        self.salinity = np.ones(np.shape(self._my_grid[0])) * self._ini_sal
        self.volume = self._depth * x_step * y_step * self._porosity
        self.q_fac = self._k_f * self._slope / y_step
        inds = np.arange(
            (self._flooding_duration.shape[0] - 1) *
            (self.y_resolution - 1), 0,
            -(self._flooding_duration.shape[0] - 1)) / (self.y_resolution - 1)
        inds = np.append(inds, 0)
        inds_int = np.trunc(inds).astype(int)
        inds_frac = inds - inds_int
        raw_flodur = np.append(self._flooding_duration, 0)
        flodur = (raw_flodur[inds_int] + inds_frac *
                  (raw_flodur[inds_int + 1] - raw_flodur[inds_int])) / 24
        dilu_vec = (_dilution_frac_upper +
                    (-_dilution_frac_upper + _dilution_frac_lower) * flodur)
        self.dilution_frac = (np.repeat(np.array([dilu_vec]),
                                        self.x_resolution,
                                        axis=0)).transpose()

    ## This functions prepares the tree variables for the SimpleHydro
    #  concept.\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self._t_ini = t_ini
        self._t_end = t_end
        self._r_root = []
        self._r_crown = []
        self._r_stem = []
        self._h_stem = []
        self._xe = []
        self._ye = []
        self._resistance = []
        self._potential_nosal = []

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()

        self._xe.append(x)
        self._ye.append(y)
        self._r_root.append(geometry["r_root"])
        self._r_crown.append(geometry["r_crown"])
        self._r_stem.append(geometry["r_stem"])
        self._h_stem.append(geometry["h_stem"])
        root_surface_resistance = self.rootSurfaceResistance(
            parameter["lp"], parameter["k_geom"], geometry["r_root"],
            geometry["h_root"])
        xylem_resistance = self.xylemResistance(geometry["r_crown"],
                                                geometry["h_stem"],
                                                geometry["r_root"],
                                                parameter["kf_sap"],
                                                geometry["r_stem"])
        self._resistance.append(root_surface_resistance + xylem_resistance)
        self._potential_nosal.append(
            (parameter["leaf_water_potential"] +
             (2 * geometry["r_crown"] + geometry["h_stem"]) * 9810))

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
