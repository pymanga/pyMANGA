#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from TreeModelLib.GrowthAndDeathDynamics import GrowthAndDeathDynamics


class SimpleTest(GrowthAndDeathDynamics):
    def __init__(self, args):
        ## SimpleTest case for death and growth dynamics. This case is
        #  defined to test the passing of information between the instances.
        #  @VAR: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the cgrowth and death concept.
        #  In the SimpleTest concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @VAR: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.trees = []
        self.t_ini = t_ini
        self.t_end = t_end

    def progressTree(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        tree.setGeometry(geometry)
        tree.setSurvival(1)
