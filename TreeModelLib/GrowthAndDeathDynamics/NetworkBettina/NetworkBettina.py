#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
from TreeModelLib.GrowthAndDeathDynamics import GrowthAndDeathDynamics
from TreeModelLib.GrowthAndDeathDynamics.SimpleBettina import SimpleBettina
import numpy as np


class NetworkBettina(SimpleBettina):
    ## NetworkBettina for death and growth dynamics. This module is implements ...
    #  @param Tags to define SimpleBettina: type
    #  @date 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Growth and death dynamics of type " + case + ".")

    def progressTree(self, tree, aboveground_resources, belowground_resources):
        network = tree.getNetwork()
        ## counter to track or define the time required for root graft formation,
        # if -1 no root graft formation takes place at the moment
        self.rgf = network['rgf']
        self.partner = network['partner']
        self.potential_partner = network['potential_partner']
        self.psi_osmo = network["psi_osmo"]
        self.name = str(tree.group_name) + str(tree.tree_id)
        # Simple bettina tree progress
        SimpleBettina.progressTree(self, tree, aboveground_resources, belowground_resources)
        network['rgf'] = self.rgf
        network['potential_partner'] = self.potential_partner
        network['partner'] = self.partner
        tree.setNetwork(network)
        if (self.survive == 1):
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

    ## This function calculates the available resources and the biomass increment.
    # In addition, this function reduces the available resources if trees are in the grafting process
    # and calls the root graft formation manager
    def growthResources(self):
        # Simple bettina get growth resources
        SimpleBettina.growthResources(self)
        self.rootGraftFormation()

    ## This function reduces growth during the process of root graft formation.
    # It is assumed that the process will take 2 years (this is subject to change).
    def rootGraftFormation(self):
        if self.rgf != -1:
            self.grow = self.grow / 2
            self.rgf = self.rgf + 1
            if round(self.rgf * self.time / 3600 / 24 / 365, 3) >= 2:
                self.rgf = -1
                self.partner.append(self.potential_partner)
                self.potential_partner = []
