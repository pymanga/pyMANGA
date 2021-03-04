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
        self.getInputParameters(args)

    def progressTree(self, tree, aboveground_resources, belowground_resources):
        network = tree.getNetwork()
        ## counter to track or define the time required for root graft formation,
        # if -1 no root graft formation takes place at the moment
        self.rgf = network['rgf']
        self.partner = network['partner']
        self.potential_partner = network['potential_partner']
        self.psi_osmo = network["psi_osmo"]

        self.r_gr_min = network['r_gr_min']
        self.r_gr_rgf = network['r_gr_rgf']
        self.l_gr_rgf = network['l_gr_rgf']
        self.weight_gr = network['weight_gr']

        self.name = str(tree.group_name) + str(tree.tree_id)
        # Simple bettina tree progress
        SimpleBettina.progressTree(self, tree, aboveground_resources,
                                   belowground_resources)

        network['rgf'] = self.rgf
        network['potential_partner'] = self.potential_partner
        network['partner'] = self.partner

        network['r_gr_min'] = self.r_gr_min
        network['r_gr_rgf'] = self.r_gr_rgf
        network['l_gr_rgf'] = self.l_gr_rgf
        network['weight_gr'] = self.weight_gr

        tree.setNetwork(network)
        if self.survive == 1:
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

    ## This functions calculates the growths weights for distributing
    # biomass increment to the geometric (allometric) tree measures as
    # defined in SimpleBettina. In addition, the function calls the root
    # graft formation function, if the tree is currently in the process of
    # root graft formation.
    def treeGrowthWeights(self):
        # Simple bettina get growth weigths
        SimpleBettina.treeGrowthWeights(self)

        # If self.r_gr_min exists the tree is currently in the process of rgf
        if self.r_gr_min:
            self.rootGraftFormation()
        else:
            self.weight_gr = 0


    ## This function simulated root graft formation and thereby reduces girth
    # growth during this process.
    def rootGraftFormation(self):
        # check if rgf is finished
        if self.r_gr_rgf >= self.r_gr_min[0]:
            print('RGF is finished after ' + str(self.rgf) + ' time '
                 'steps. Years: ' + str(self.rgf * self.time / 3600 / 24 /
                                        365))
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
            self.weight_gr = self.weight_girthgrowth * self.f_wgr
            inc_r_gr = (self.weight_gr * self.grow /
                        (2 * np.pi * self.l_gr_rgf * self.r_gr_rgf))
            self.r_gr_rgf += inc_r_gr
            # reduce girth growth factor
            self.weight_girthgrowth = self.weight_girthgrowth * (1 -
                                                                 self.f_wgr)
            self.rgf += 1

    def getInputParameters(self, args):
        missing_tags = ["type", "f_wgr"]
        for arg in args.iterdescendants():
            tag = arg.tag
            print('tag ' + str(tag))
            if tag == "f_wgr":
                self.f_wgr = float(args.find("f_wgr").text)
            try:
                missing_tags.remove(tag)
            except ValueError:
                raise ValueError(
                    "Tag " + tag +
                    " not specified for growth and death initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not given for growth and death initialisation in "
                "project file."
            )
