#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from matplotlib import pyplot as plt
from VisualizationLib.Visualization import Visualization


class SimplePyplot(Visualization):
    def __init__(self, args):
        self.case = args.find("type").text

        print("Initiate visualization of type " + self.case + ".")
        try:
            self.max_fps = float(args.find("max_fps").text)
        except AttributeError:
            self.max_fps = 50
            print("Tag 'max_fps' in '" + self.case +
                  "' visualization is missing! max_fps set to 50.")
        fig, self.ax = plt.subplots(figsize=(10, 10))

    def update(self, tree_groups, time):
        self.ax.clear()
        for group_name, tree_group in tree_groups.items():
            xs, ys, rs = [], [], []
            for tree in tree_group.getTrees():
                x, y = tree.getPosition()
                xs.append(x), ys.append(y)
                geo = tree.getGeometry()
                rs.append(geo["r_crown"])
            self.ax.scatter(xs, ys, s=rs, label=tree_group.name)
        plt.legend(loc=1)
        timestring = self.createTimestring(time)
        left, rigth = plt.xlim()
        ex_x = rigth - left
        bottom, top = plt.ylim()
        ex_y = top - bottom
        if ex_y > ex_x:
            left = rigth - ex_y
        elif ex_x > ex_y:
            bottom = top - ex_x
        plt.title("Time = " + timestring + "years")
        plt.draw()
        plt.pause(1 / self.max_fps)

    def show(self, time):
        plt.title("Time = " + str(time) + "years")
        plt.show()

    def createTimestring(self, arg):
        timestring = ""
        if (type(arg) == float):
            arg = arg / (60 * 60 * 24 * 365.25)
            timestring = "%2.2f" % arg
        else:
            timestring = str(arg)
        return timestring
