#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from PlantModelLib import PlantModel


class JabowaHPC(PlantModel):
    """
    Jabowa plant model (optimized, vectorized, float32).
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): plant module specifications from project file tags
        """
        case = args.find("vegetation_model_type").text
        super().iniMortalityConcept(args)
        self.time = np.float32(0.0)

    def prepareNextTimeStep(self, t_ini, t_end):
        self.time = np.float32(t_end - t_ini)

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        """
        Original single-tree update (kept for backward compatibility).
        """
        geometry = tree.getGeometry()
        growth_concept_information = tree.getGrowthConceptInformation()
        parameter = tree.getParameter()

        super().setMortalityVariables(growth_concept_information)
        self.survive = 1

        dbh = np.float32(geometry["r_stem"] * 200.0)  # cm
        height = np.float32(137.0 + parameter["b2"] * dbh - parameter["b3"] * dbh**2)
        self.grow = np.float32(
            parameter["max_growth"] * dbh *
            (1.0 - (dbh * height) / (parameter["max_dbh"] * parameter["max_height"])) /
            (274.0 + 3.0 * parameter["b2"] * dbh - 4.0 * parameter["b3"] * dbh**2) *
            np.float32(belowground_resources) * np.float32(aboveground_resources)
        )

        dbh = dbh + self.grow * self.time / np.float32(3600.0 * 24.0 * 365.25)
        r_zoi = np.float32(parameter["a_zoi_scaling"] * (dbh / 2.0 / 100.0)**0.5)

        geometry["r_stem"] = np.float32(dbh / 200.0)
        geometry["r_root"] = r_zoi
        geometry["r_crown"] = r_zoi
        geometry["height"] = np.float32(height / 100.0)
        geometry["h_stem"] = np.float32(height / 100.0 - 2.0 * r_zoi)

        growth_concept_information["growth"] = self.grow
        growth_concept_information["bg_factor"] = np.float32(belowground_resources)
        growth_concept_information["ag_factor"] = np.float32(aboveground_resources)
        growth_concept_information["age"] = growth_concept_information.get("age", np.float32(0.0)) + self.time

        tree.setGeometry(geometry)
        tree.setGrowthConceptInformation(growth_concept_information)

        self.volume = dbh
        super().setTreeKiller()
        super().getMortalityVariables(growth_concept_information)
        tree.setSurvival(1 if self.survive == 1 else 0)

    def progressPlants(self, trees, aboveground_resources, belowground_resources):
        """
        Optimized update for multiple trees (no broadcasting, but vectorized loops).
        Args:
            trees (list): list of tree objects
            aboveground_resources (ndarray): shape (N,)
            belowground_resources (ndarray): shape (N,)
        """
        N = len(trees)
        geometries = [t.getGeometry() for t in trees]
        parameters = [t.getParameter() for t in trees]
        gci_list = [t.getGrowthConceptInformation() for t in trees]

        # Extract parameters as float32 arrays
        b2 = np.array([p["b2"] for p in parameters], dtype=np.float32)
        b3 = np.array([p["b3"] for p in parameters], dtype=np.float32)
        max_growth = np.array([p["max_growth"] for p in parameters], dtype=np.float32)
        max_dbh = np.array([p["max_dbh"] for p in parameters], dtype=np.float32)
        max_height = np.array([p["max_height"] for p in parameters], dtype=np.float32)
        a_zoi_scaling = np.array([p["a_zoi_scaling"] for p in parameters], dtype=np.float32)

        # Precompute constants
        year_factor = np.float32(self.time / (3600.0 * 24.0 * 365.25))

        # Compute dbh, height and growth as float32
        dbh = np.array([g["r_stem"] * 200.0 for g in geometries], dtype=np.float32)  # cm
        height = np.float32(137.0) + b2 * dbh - b3 * dbh**2
        grow = (
            max_growth * dbh *
            (1.0 - (dbh * height) / (max_dbh * max_height)) /
            (274.0 + 3.0 * b2 * dbh - 4.0 * b3 * dbh**2) *
            np.array(belowground_resources, dtype=np.float32) *
            np.array(aboveground_resources, dtype=np.float32)
        )
        dbh_new = dbh + grow * year_factor
        r_zoi = a_zoi_scaling * (dbh_new / 2.0 / 100.0)**0.5
        height_m = height / 100.0
        h_stem = height_m - 2.0 * r_zoi

        # Update geometries and growth info with float32
        for geo, gci, dbh_n, rz, h, hs, gr, bg, ag in zip(
            geometries, gci_list, dbh_new, r_zoi, height_m, h_stem,
            grow, belowground_resources, aboveground_resources
        ):
            geo["r_stem"] = np.float32(dbh_n / 200.0)
            geo["r_root"] = np.float32(rz)
            geo["r_crown"] = np.float32(rz)
            geo["height"] = np.float32(h)
            geo["h_stem"] = np.float32(hs)

            gci["growth"] = np.float32(gr)
            gci["bg_factor"] = np.float32(bg)
            gci["ag_factor"] = np.float32(ag)
            gci["age"] = gci.get("age", np.float32(0.0)) + self.time

        # Apply updates and mortality
        for tree, geo, gci, vol in zip(trees, geometries, gci_list, dbh_new):
            tree.setGeometry(geo)
            tree.setGrowthConceptInformation(gci)
            self.volume = np.float32(vol)
            super().setTreeKiller()
            super().getMortalityVariables(gci)
            tree.setSurvival(1 if self.survive == 1 else 0)
