#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ModelOutputLib.ModelOutput import ModelOutput
import os
import time as time_module  # 避免与参数 time 冲突
from datetime import datetime  # 用于格式化当前时间

class OneTimestepOneFile(ModelOutput):
    """
    Model output concept.
    Create one file for each time step, i.e., each file contains the complete population of a single time step.
    Filename includes time step in seconds, e.g. 'Population_t_<time_step>'.
    Each line contains plant, time, position and user selected output parameters.
    """
    def __init__(self, args):
        super().__init__(args)
        self._last_real_time = None  # 记录上一次运行时间
        self._time_log_file = os.path.join(self.output_dir, "timelog.txt")  # timelog 文件路径

    def log_runtime(self, real_dt):
        """将时间差记录到 timelog.txt"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self._time_log_file, "a", encoding="utf-8") as f:
            f.write(f"[{current_time}] Real runtime since last output: {real_dt:.2f} seconds\n")

    def outputContent(self, plant_groups, time, **kwargs):
        # 记录真实运行时间差
        now = time_module.time()
        if self._last_real_time is not None:
            real_dt = now - self._last_real_time
            self.log_runtime(real_dt)
        else:
            # 第一次调用时也记录一个启动时间点
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self._time_log_file, "a", encoding="utf-8") as f:
                f.write(f"[{start_time}] First output log started.\n")

        self._last_real_time = now

        # 原有 CSV 输出逻辑
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
