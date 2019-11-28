#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition


class SimpleTest(BelowgroundCompetition):
    def __init__(self, args):
        ## SimpleTest case for belowground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @param: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")

    def calculateBelowgroundResources(self):
        ## This function returns the BelowgroundResources calculated in the
        #  subsequent timestep. In the SimpleTest concept, for each tree a one
        #  is returned
        #  @return: np.array with $N_tree$ scalars
        self.belowground_resources = self.trees

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the competition concept for the competition
        #  concept. In the SimpleTest concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @param: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.trees = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addTree(self, x, y, geometry, parameter):
        ## Before being able to calculate the resources, all tree enteties need
        #  to be added with their current implementation for the next timestep.
        #  Here, in the SimpleTest case, each tree is represented by a one. In
        #  general, an object containing all necessary information should be
        #  stored for each tree
        #  @param: position, geometry, parameter
        self.trees.append(1)
