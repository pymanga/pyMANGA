#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PlantModelLib.Bettina import Bettina
import numpy as np


class BettinaNetwork(Bettina):
    def __init__(self, args):
        """
        Plant model concept.
        This module inherits the tree growth functionality of Bettina, but can account for resource loss and water
        transfer through root grafts.
        MRO: BettinaNetwork, Bettina, TreeModel, object
        Args:
            args: BettinaNetwork module specifications from project file tags
        """
        super().__init__(args=args)
        self.getInputParameters(args=args)

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        """
        Manage growth procedures for a timestep --- read tree geometry and parameters, schedule computations, and update tree geometry and survival
        Args:
            tree (dict): tree object
            aboveground_resources (float): above-ground resource growth reduction factor
            belowground_resources (float): below-ground resource growth reduction factor
        Sets:
            dictionary containing network information
        """
        network = tree.getNetwork()
        ## counter to track or define the time required for root graft formation,
        # if -1 no root graft formation takes place at the moment
        self.rgf = network['rgf']
        self.partner = network['partner']
        self.potential_partner = network['potential_partner']
        self.psi_osmo = network["psi_osmo"]

        # parameters for rgf variant "V2_adapted"
        self.r_gr_min = network['r_gr_min']
        self.r_gr_rgf = network['r_gr_rgf']
        self.l_gr_rgf = network['l_gr_rgf']
        self.weight_gr = network['weight_gr']

        self.name = str(tree.group_name) + str(tree.plant_id)
        # Simple bettina tree progress
        super().progressPlant(tree=tree,
                             aboveground_resources=aboveground_resources,
                             belowground_resources=belowground_resources)

        network['variant'] = self.variant
        network['rgf'] = self.rgf
        network['potential_partner'] = self.potential_partner
        network['partner'] = self.partner
        network['node_degree'] = len(self.partner)

        # parameters for rgf variant "V2_adapted"
        network['r_gr_min'] = self.r_gr_min
        network['r_gr_rgf'] = self.r_gr_rgf
        network['l_gr_rgf'] = self.l_gr_rgf
        network['weight_gr'] = self.weight_gr  # only required for csv
        # output

        tree.setNetwork(network=network)
        if self.survive == 1:
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

    def treeGrowthWeights(self):
        """
        Calculate the growth weights for distributing biomass increment to the tree geometries.
        See `pyMANGA.PlantModelLib.Bettina.Bettina`
        If resources for root graft formation are required, the respective module is called.
        Sets:
            multiple float
        """
        if self.variant == 'V2_adapted':
            self.treeGrowthWeightsV2()
        else:
            super().treeGrowthWeights()

    def growthResources(self):
        """
        Calculate the available resources and the biomass increment.
        See `pyMANGA.PlantModelLib.Bettina.Bettina`
        If resources for root graft formation are required, the respective module is called.
        Sets:
            multiple float
        """
        super().growthResources()
        if self.variant == "V0_instant":
            self.rootGraftFormationV0()
        if self.variant == "V1_fixed":
            self.rootGraftFormationV1()

    def treeGrowthWeightsV2(self):
        """
        Calculate the growth weights for distributing biomass increment to the tree geometries.
        See `pyMANGA.PlantModelLib.Bettina.Bettina`
        In addition, the function calls the root graft formation function, if the tree is currently
        in the process of root graft formation and root graft formation follows variant V2.
        Sets:
            multiple float
        """
        # Simple bettina get growth weigths
        super().treeGrowthWeights()

        # If self.r_gr_min exists the tree is currently in the process of rgf
        if self.r_gr_min:
            self.rootGraftFormationV2()
        else:
            self.weight_gr = 0

    def rootGraftFormationV0(self):
        """
        Manage root graft formation.
        Immediate root grafting, i.e. roots in contact are immediately grafted and no resources are required.
        Sets:
            multiple float
        """
        if self.rgf != -1:
            self.rgf = -1
            self.partner.append(self.potential_partner)
            self.potential_partner = []

    def rootGraftFormationV1(self):
        """
        Manage root graft formation.
        Growth reduction during root graft formation.
        It is assumed that the process will take 2 years.
        Sets:
            multiple float
        """
        if self.rgf != -1:
            self.grow = self.grow * (1 - self.f_growth)
            self.rgf = self.rgf + 1
            if round(self.rgf * self.time / 3600 / 24 / 365, 3) >= 2:
                self.rgf = -1
                self.partner.append(self.potential_partner)
                self.potential_partner = []

    def rootGraftFormationV2(self):
        """
        Manage root graft formation.
        Girth growth reduction during root graft formation.
        The duration of the process is variable, depending on the size and resource availability of the plants involved.        Sets:
            multiple float
        """
        # check if rgf is finished
        if self.r_gr_rgf >= self.r_gr_min[0]:
            # Append partner
            self.partner.append(self.potential_partner)
            # Reset rgf parameters
            self.r_gr_rgf = 0.004
            self.rgf = -1
            # analyse rgf duration
            self.potential_partner = []
            self.r_gr_min = []
        else:
            # if rgf is not finished, the grafted roots must grow
            self.weight_gr = self.weight_girthgrowth * self.f_growth
            inc_r_gr = (self.weight_gr * self.grow /
                        (2 * np.pi * self.l_gr_rgf * self.r_gr_rgf))
            self.r_gr_rgf += inc_r_gr
            # reduce girth growth factor
            self.weight_girthgrowth = self.weight_girthgrowth * (1 -
                                                                 self.f_growth)
            self.rgf += 1

    def getInputParameters(self, args):
        required_tags = ["type", "variant", "f_growth"]
        super().getInputParameters(args, required_tags)
