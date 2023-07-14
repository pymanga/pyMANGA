#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from ResourceLib import ResourceModel


class Default(ResourceModel):
    ## Default case for belowground competition concept. This case is
    #  defined to test the passing of information between the instances.
    #  @param: Tags to define Default: type
    #  @date: 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")

    ## This function returns the BelowgroundResources calculated in the
    #  subsequent timestep. In the Default concept, for each plant a one
    #  is returned
    #  @return: np.array with $N_plant$ scalars
    def calculateBelowgroundResources(self):
        self.belowground_resources = self.plants

    ## This functions prepares the competition concept for the competition
    #  concept. In the Default concept, plants are saved in a simple list
    #  and the timestepping is updated. In preparation for the next time-
    #  step, the list is simply resetted.
    #  @param: t_ini - initial time for next timestep \n
    #  t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        self.plants = []
        self.t_ini = t_ini
        self.t_end = t_end

    ## Before being able to calculate the resources, all plant enteties need
    #  to be added with their current implementation for the next timestep.
    #  Here, in the Default case, each plant is represented by a one. In
    #  general, an object containing all necessary information should be
    #  stored for each plant
    #  @param: position, geometry, parameter
    def addPlant(self, plant):
        self.plants.append(1)

    ## Test for external timestepper, whether the concept is optimized for ex-
    #  ternal communication
    def getOGSAccessible(self):
        return True

    ## Setter for external information - specify and document argument for each
    #  concept application
    #  (See examples from test directory)
    def setExternalInformation(self, **args):
        self.external_information = args

    ## Getter for external information
    def getExternalInformation(self):
        return self.external_information
