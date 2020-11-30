#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition


class SimpleHydro(BelowgroundCompetition):
    ## FON case for belowground competition concept. For details see
    #  (https://doi.org/10.1016/S0304-3800(00)00298-2). FON returns a list
    #  of multipliers for each tree for salinity and competition.\n
    #  @param: Tags to define FON, see tag documentation \n
    #  @date: 2019 - Today
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
                                       np.array(self._salinity) * 85000) /
                                      np.array(self._potential_nosal))
        print(self.belowground_resources)

    def transpire(self):
        distance = (np.array(self._r_root)[np.newaxis, np.newaxis, :] -
                    ((self._my_grid[0][:, :, np.newaxis] -
                      np.array(self._xe)[np.newaxis, np.newaxis, :])**2 +
                     (self._my_grid[1][:, :, np.newaxis] -
                      np.array(self._ye)[np.newaxis, np.newaxis, :])**2)**0.5)
        water_loss = (distance - distance)[:, :, 0]
        presence = distance > 0
        maxe = np.amax(distance, axis=(0, 1))
        self._salinity = []
        self.transpiration = []
        for ii in range(distance.shape[2]):
            closest = distance[:, :, ii] == maxe[ii]
            presence[:, :, ii] = np.fmax(closest, presence[:, :, ii])
            self._salinity.append((np.sum(presence[:, :, ii] * self.salinity) /
                                   np.sum(presence[:, :, ii])))
            self.transpiration.append(
                (-self._potential_nosal[ii] - self._salinity[ii] * 85000) /
                self._resistance[ii] / np.pi * (self._t_end - self._t_ini))
            water_loss += (self.transpiration[ii] /
                           np.sum(presence[:, :, ii])) * presence[:, :, ii]
        print(np.sum(self.transpiration))
        # dilution
        self.salinity += self._sea_salinity * water_loss / self.volume
        self.salinity += (-self.salinity * self._dilution_frac_upper +
                          self._sea_salinity * self._dilution_frac_upper)

        # diffusion
        salinity_new = self.salinity * (1 - self._diffusion_frac)
        # x-dir
        for ii in range(self.x_resolution):
            if ii == self.x_resolution - 1:
                salinity_new[:,
                             ii] += self.salinity[:,
                                                  ii] * self._diffusion_frac / 4
                salinity_new[:, ii -
                             1] += self.salinity[:,
                                                 ii] * self._diffusion_frac / 4
            elif ii == 0:
                salinity_new[:, ii +
                             1] += self.salinity[:,
                                                 ii] * self._diffusion_frac / 4
                salinity_new[:,
                             ii] += self.salinity[:,
                                                  ii] * self._diffusion_frac / 4
            else:
                salinity_new[:, ii +
                             1] += self.salinity[:,
                                                 ii] * self._diffusion_frac / 4
                salinity_new[:, ii -
                             1] += self.salinity[:,
                                                 ii] * self._diffusion_frac / 4

        # y-dir
        for ii in range(self.y_resolution):
            if ii == self.y_resolution - 1:
                salinity_new[
                    ii, :] += self.salinity[ii, :] * self._diffusion_frac / 4
                salinity_new[
                    ii -
                    1, :] += self.salinity[ii, :] * self._diffusion_frac / 4
            elif ii == 0:
                salinity_new[
                    ii +
                    1, :] += self.salinity[ii, :] * self._diffusion_frac / 4
                salinity_new[
                    ii, :] += self.salinity[ii, :] * self._diffusion_frac / 4
            else:
                salinity_new[
                    ii +
                    1, :] += self.salinity[ii, :] * self._diffusion_frac / 4
                salinity_new[
                    ii -
                    1, :] += self.salinity[ii, :] * self._diffusion_frac / 4
        self.salinity = salinity_new
        # gradient-flow
        multi_fac = self.Q_fac * (self._t_end - self._t_ini)
        salinity_new[0, :] = self.salinity[0, :] * (
            1 - multi_fac) + self._up_sal * multi_fac
        salinity_new[1:self.y_resolution, :] = (
            self.salinity[1:self.y_resolution, :] * (1 - multi_fac) +
            self.salinity[0:(self.y_resolution - 1), :] * multi_fac)
        self.salinity = salinity_new
        print(np.ndarray.round(self.salinity))

    ## This function initialises the mesh.\n
    def makeGrid(self, args):
        missing_tags = [
            "type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution",
            "y_resolution", "depth", "porosity", "dilution_frac_upper",
            "dilution_frac_lower", "diffusion_frac", "sea_salinity", "ini_sal",
            "up_sal", "slope", "k_f"
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
                self._dilution_frac_upper = float(arg.text)
            elif tag == "dilution_frac_lower":
                self._dilution_frac_lower = float(arg.text)
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
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for below-ground grid initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for below-ground grid initialisation in project file."
            )
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
        self.salinity = self._my_grid[0] - self._my_grid[0] + self._ini_sal
        self.volume = self._depth * x_step * y_step * self._porosity
        self.Q_fac = self._k_f * self._slope / y_step

    ## This functions prepares the competition concept for the competition
    #  concept. In the FON concept, tree's allometric measures are saved
    #  in simple lists and the timestepping is updated. A mesh-like array
    #  is prepared for storing all FON heights of the stand.\n
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
        print(self._t_ini / 3600 / 24 / 365)

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: position, geometry, parameter
    def addTree(self, x, y, geometry, parameter):
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
