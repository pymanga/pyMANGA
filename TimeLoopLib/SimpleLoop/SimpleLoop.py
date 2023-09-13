#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class SimpleLoop:

    def __init__(self, args):
        """
        Default time step module.
        Time step length is constant.
        Args:
            args: module specifications from project file tags
        """
        case = args.find("type").text
        print("Time loop: {}.".format(case))
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

    def getUpdateBools(self):
        """
        Check whether to calculate above- and below-ground resources.
        Sets:
            multiple bools
        """
        self.update_ag = True if self.step_counter % self.n_step_ag == 0 else False
        self.update_bg = True if self.step_counter % self.n_step_bg == 0 else False

    def getNextTimeStep(self):
        """
        Calculate the start and end time of the next timestep and evaluate which modules should be updated.
        Sets:
            multiple float
        """
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
