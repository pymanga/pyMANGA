#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de, marie-christin.wimmler@tu-dresden.de
"""


class TreeDynamicTimeLoop:
    def __init__(self, args):
        case = args.find("type").text
        if case == "Simple":
            self.iniSimpleTimeStepping(args)
        else:
            raise KeyError("Required time stepping not implemented.")
        try:
            self.terminal_print = args.find('terminal_print').text
            print('worked')
        except:
            self.terminal_print = False
            print('did not work')
        print(case + " time stepping successfully initiated.")


    def iniSimpleTimeStepping(self, args):
        from .SimpleTimeLoop import SimpleLoop
        self.loop = SimpleLoop.Loop(args)

    def getNextTimeStepBoundaries(self):
        self.loop.getNextTimeStep()

    ## Runs the predefined timeloop using a specific timestepper.
    def runTimeLoop(self, time_stepper):
        self.getNextTimeStepBoundaries()
        while (self.loop.step_on):
            if self.terminal_print == 'years':
                print("Next time step to propagate" +
                      " tree population with starting time " +
                      '%4.2f' % (float(self.loop.t_1)/86400/365.25) +
                      " a and end time " +
                      '%4.2f' % (float(self.loop.t_2)/86400/365.25) + " a." +
                      '\nCalculated timesteps: ' +
                      str(int((self.loop.t_2/self.loop.t_end)*100)) + ' %')
            elif self.terminal_print == 'days':
                print("Next time step to propagate" +
                      " tree population with starting time " +
                      '%4.2f' % (float(self.loop.t_1)/86400) +
                      " d and end time " +
                      '%4.2f' % (float(self.loop.t_2)/86400) + " d." +
                      '\nCalculated timesteps: ' +
                      str(int((self.loop.t_1/self.loop.t_end)*100)) + ' %')
            time_stepper.step(t_start=self.loop.t_1, t_end=self.loop.t_2,
                              update_ag=self.loop.update_ag,
                              update_bg=self.loop.update_bg)
            self.getNextTimeStepBoundaries()
        time_stepper.finish(self.loop.t_1)
