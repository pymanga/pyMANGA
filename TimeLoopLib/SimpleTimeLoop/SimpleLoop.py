#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""


class Loop:
    def __init__(self, args):
        ## SimpleTest case for aboveground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @VAR: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        print("Initiate time loop of type " + case + ".")
        self.t_start = float(args.find("t_start").text)
        self.t_end = float(args.find("t_end").text)
        self.t_current = self.t_start
        self.delta_t = float(args.find("delta_t").text)

    def getNextTimeStep(self):
        t_1 = self.t_current
        t_2 = t_1 + self.delta_t
        self.t_current = t_2
        if (t_1 < self.t_end):
            step_on = True
            if (t_2 > self.t_end):
                t_2 = self.t_end
        elif (t_1 >= self.t_end):
            step_on = False
        return t_1, t_2, step_on
