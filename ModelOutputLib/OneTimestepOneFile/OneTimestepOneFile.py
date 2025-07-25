#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ModelOutputLib.ModelOutput import ModelOutput
import os
import time as time_module   # Avoid naming conflict with a parameter named 'time'
from datetime import datetime  # For formatting current time

class OneTimestepOneFile(ModelOutput):
    """
    Model output concept.
    Create one file for each time step, i.e., each file contains the complete population of a single time step.
    Filename includes time step in seconds, e.g. 'Population_t_<time_step>'.
    Each line contains plant, time, position and user selected output parameters.

    Adding for test:
    **Runtime logging:**
    - A separate `timelog.txt` file is maintained in the output directory.
    - At every call of `outputContent()`, the real elapsed wall-clock time (in seconds) since the last call is appended to `timelog.txt`.
    - On the first call, the current timestamp is recorded with the message: 
        "[YYYY-MM-DD HH:MM:SS] First output log started."

    """
    def __init__(self, args):
        super().__init__(args)
        self._last_real_time = None   # Record the previous runtime timestamp
        self._time_log_file = os.path.join(self.output_dir, "timelog.txt")  # timelog file path

    def log_runtime(self, real_dt):
        """Append the elapsed time to timelog.txt"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self._time_log_file, "a", encoding="utf-8") as f:
            f.write(f"[{current_time}] Real runtime since last output: {real_dt:.2f} seconds\n")

    def outputContent(self, plant_groups, time, **kwargs):
        #  Record the real elapsed time between calls
        now = time_module.time()
        if self._last_real_time is not None:
            real_dt = now - self._last_real_time
            self.log_runtime(real_dt)
        else:
            # For the first call, log the initial start time
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self._time_log_file, "a", encoding="utf-8") as f:
                f.write(f"[{start_time}] First output log started.\n")

        self._last_real_time = now

        # Original CSV output logic
        if not kwargs["group_died"]:
            filename = ("Population_t_%012.1f" % (time) + ".csv")
        else:
            filename = ("Population_t_%012.1f_group_died" % (time) + ".csv")

        file = open(os.path.join(self.output_dir, filename), "w")
        string = 'plant' + self.delimiter + 'time' + self.delimiter + 'x' + self.delimiter + 'y'
        string = self.addSelectedHeadings(string) + "\n"
        file.write(string)

        for group_name, plant_group in plant_groups.items():
            for plant in plant_group.getPlants():
                growth_information = plant.getGrowthConceptInformation()
                line = (group_name + "_" + "%09.0d" % (plant.getId()) +
                        self.delimiter + str(time) +
                        self.delimiter + str(plant.x) +
                        self.delimiter + str(plant.y))
                line = self.addSelectedOutputs(plant, line, growth_information) + "\n"
                file.write(line)

        file.close()
