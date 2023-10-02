#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from ResourceLib import ResourceModel


class Default(ResourceModel):

    def __init__(self, args):
        ## Default case for death and growth dynamics. This case is
        #  defined to test the passing of information between the instances.
        #  @param: Tags to define Default: type
        #  @date: 2019 - Today
        case = args.find("vegetation_model_type").text

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the cgrowth and death concept.
        #  In the Default concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @param: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.plants = []
        self.t_ini = t_ini
        self.t_end = t_end

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        tree.setGeometry(geometry)
        tree.setSurvival(1)
