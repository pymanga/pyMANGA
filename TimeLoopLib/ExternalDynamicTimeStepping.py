#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
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
            raise AttributeError(
                """In order to use MANGA as OGS python boundary condition,
                    one has to use a corresponding belowground competition
                    concept. Please see documentation for further details!""")

    def step(self, t_end):
        t_start = self.t_step_begin
        super().step(t_start, t_end)
        t_end = self.t_step_begin
