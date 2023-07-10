#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class DynamicTimeLoop:
    def __init__(self, args):
        """
        Time step management.
        Create time stepper object based on selected time loop concept.
        Args:
            args: time loop module specifications from project file tags
        """
        case = args.find("type").text
        if case == "Simple":
            self.iniSimpleTimeStepping(args)
        else:
            raise KeyError("Required time stepping not implemented.")
        # If terminal_print is defined as 'days' or 'years' the respective
        # value for the conversion of time unit gets defined in 'print_unit'.
        try:
            self.terminal_print = args.find('terminal_print').text
            if self.terminal_print == 'years':
                self.print_unit = 86400 * 365.25
            elif self.terminal_print == 'days':
                self.print_unit = 86400
        except:
            self.terminal_print = False

        print(case + " time stepping successfully initiated.")

    def iniSimpleTimeStepping(self, args):
        """
        Initialize time stepping of type "Default".
        Args:
            args: time module specifications from project file tags
        """
        from .SimpleLoop import SimpleLoop
        self.loop = SimpleLoop(args)

    def getNextTimeStepBoundaries(self):
        """
        Get boundaries of time step from selected time loop module.
        Sets:
            multiple float
        """
        self.loop.getNextTimeStep()

    def runTimeLoop(self, time_stepper):
        """
        Run time loop with selected time stepper.
        Manages terminal prints during run.
        Args:
            time_stepper: time stepper object
        """
        self.getNextTimeStepBoundaries()
        while (self.loop.step_on):
            # If terminal_print is defined as 'years' or 'day' the
            # respective text gets printed after each time step
            abb = False
            if self.terminal_print == 'years':
                abb = "a"
            elif self.terminal_print == 'days':
                abb = "d"
            if abb:
                print("Next time step to propagate" +
                      " plant population with starting time " + '%4.2f' %
                      (float(self.loop.t_1) / self.print_unit) + " " +
                      abb + " and end time " + '%4.2f' %
                      (float(self.loop.t_2) / self.print_unit) + " " + abb + "." +
                      '\nCalculated timesteps: ' +
                      str(int((self.loop.t_1 / self.loop.t_end) * 100)) + ' %')
            time_stepper.step(t_start=self.loop.t_1,
                              t_end=self.loop.t_2,
                              update_ag=self.loop.update_ag,
                              update_bg=self.loop.update_bg)
            self.getNextTimeStepBoundaries()
        time_stepper.finish(self.loop.t_1)
