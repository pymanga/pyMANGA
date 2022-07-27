#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de, marie-christin.wimmler@tu-dresden.de
"""


class Loop:

    def __init__(self, args):
        ## SimpleTest case for aboveground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @param: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        print("Initiate time loop of type " + case + ".")
        self.t_start = float(args.find("t_start").text)
        self.t_end = float(args.find("t_end").text)
        self.t_2 = self.t_start
        self.delta_t = float(args.find("delta_t").text)

        ## The following variables determine the frequencies when to
        # update particular concepts (e.g. below-ground c.)
        self.n_step_ag, self.n_step_bg, self.n_step_gd = 1, 1, 1
        if args.find("n_step_ag") is not None:
            self.n_step_ag = int(args.find("n_step_ag").text)
        if args.find("n_step_bg") is not None:
            self.n_step_bg = int(args.find("n_step_bg").text)
        self.step_counter = 0
        self.t_1 = self.t_start

    ## This checks and stores whether above- and belowground competition should
    #  be recalculated in the following timestep.
    def getUpdateBools(self):
        self.update_ag = True if self.step_counter % self.n_step_ag == 0 else False
        self.update_bg = True if self.step_counter % self.n_step_bg == 0 else False

    ## Calculates the initial and end time of next timestep and evaluates which
    #  concepts are supposed to be updated
    def getNextTimeStep(self):
        self.getUpdateBools()
        self.t_1 = self.t_2  # assigns t2 from previous timestep as new t1
        self.t_2 = self.t_1 + self.delta_t
        if (self.t_1 < self.t_end):
            self.step_on = True
            if (self.t_2 > self.t_end):
                self.t_2 = self.t_end
        elif (self.t_1 >= self.t_end):
            self.step_on = False
        self.step_counter += 1
