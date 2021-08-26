#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from pyMANGA.TimeLoopLib.TreeDynamicTimeStepping import TreeDynamicTimeStepping


class TreeDynamicTimeLoop:
    def __init__(self, args):
        case = args.find("type").text
        if case == "Simple":
            self.iniSimpleTimeStepping(args)
        else:
            raise KeyError("Required timestepping not implemented.")
        print(case + " time stepping successfully initiated.")
        self.step_on = True

    def iniSimpleTimeStepping(self, args):
        from .SimpleTimeLoop import SimpleLoop
        self.loop = SimpleLoop.Loop(args)

    def getNextTimeStepBoundaries(self):
        self.t_ini, self.t_end, self.step_on = self.loop.getNextTimeStep()

    def runTimeLoop(self, time_stepper):
        self.getNextTimeStepBoundaries()
        while (self.step_on):
            print("Next time step to propagate" +
                  " tree population with starting time " + str(self.t_ini) +
                  " and end time " + str(self.t_end) + ".")
            time_stepper.step(self.t_ini, self.t_end)
            self.getNextTimeStepBoundaries()
        time_stepper.finish(self.t_ini)
