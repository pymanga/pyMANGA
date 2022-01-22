#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de, marie-christin.wimmler@tu-dresden.de
"""
from TimeLoopLib.TreeDynamicTimeStepping import TreeDynamicTimeStepping


class ExternalDynamicTimeStepping(TreeDynamicTimeStepping):
    def __init__(self, project, t_0):
        super().__init__(project)
        ## Usability for OGS & check if BG concept works with OGS
        self.t_step_begin = t_0

        #TODO: We need a nice check for ogs usability?!
        try:
            self.belowground_competition.getOGSAccessible()
        except AttributeError:
            print("""
                    #####################WARNING###########################
                    
                    In order to use MANGA as OGS python boundary condition,
                    one has to use a corresponding belowground competition
                    concept. Please see documentation for further details!
                    
                    #####################WARNING###########################""")

    ## This functions sets the step size defined externally, as nth time
    # step for each concept.
    # If, for example, steps are defined as follows: n_step_ag = 2,
    # n_step_bg = 1, n_step_gd = 1, then above-ground competition is updated
    # every 2nd step while the other concepts are updated in each time step.
    def setSteps(self, n_step_ag, n_step_bg, n_step_gd):
        self.n_step_ag = n_step_ag
        self.n_step_bg = n_step_bg
        self.n_step_gd = n_step_gd

    ## This progresses one time step, by updating tree population and above-
    # and below-ground resources depending on the associated bools
    def step(self, t_end, update_ag, update_bg, update_gd):
        t_start = self.t_step_begin
        super().step(t_start, t_end, update_ag, update_bg, update_gd)
        t_end = self.t_step_begin
