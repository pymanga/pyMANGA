#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from ResourceLib import ResourceModel


class Default(ResourceModel):

    def __init__(self, args):
        ## Default case for aboveground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @param: Tags to define Default: type
        #  @date: 2019 - Today
        case = args.find("type").text
        print("Initiate aboveground competition of type " + case + ".")

    def calculateAbovegroundResources(self):
        ## This function returns the AbovegroundResources calculated in the
        #  subsequent timestep. In the Default concept, for each plant a one
        #  is returned
        #  @return: np.array with $N_plant$ scalars
        self.aboveground_resources = self.plants

    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the competition concept for the competition
        #  concept. In the Default concept, plants are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @param: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.plants = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addPlant(self, plant):
        ## Before being able to calculate the resources, all plant enteties need
        #  to be added with their current implementation for the next timestep.
        #  Here, in the Default case, each plant is represented by a one. In
        #  general, an object containing all necessary information should be
        #  stored for each plant
        #  @param: plant
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()

        self.plants.append(1)
