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
        self.t_current = self.t_start
        self.delta_t = float(args.find("delta_t").text)

        ## The following variables determine the frequencies when to
        # update particular concepts (e.g. below-ground c.)
        self.n_step_ag, self.n_step_bg, self.n_step_gd = 1, 1, 1
        if args.find("n_step_ag") is not None:
            self.n_step_ag = int(args.find("n_step_ag").text)
        if args.find("n_step_bg") is not None:
            self.n_step_bg = int(args.find("n_step_bg").text)
        self.step_counter = 0

    def getUpdateBools(self):
        update_ag = True if self.step_counter % self.n_step_ag == 0 else False
        update_bg = True if self.step_counter % self.n_step_bg == 0 else False
        return update_ag, update_bg

    def getNextTimeStep(self):
        update_ag, update_bg = self.getUpdateBools()
        t_1 = self.t_current
        t_2 = t_1 + self.delta_t
        self.t_current = t_2
        if (t_1 < self.t_end):
            step_on = True
            if (t_2 > self.t_end):
                t_2 = self.t_end
        elif (t_1 >= self.t_end):
            step_on = False
        self.step_counter += 1
        return t_1, t_2, step_on, update_ag, update_bg
