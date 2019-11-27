#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from matplotlib import patches as patch
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
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
        patches = []
        left, bottom = 99999, 99999
        rigth, top = -99999, -99999
        a, b = tree_groups.items()
        colors = cm.get_cmap('viridis', len(b))
        i = 0
        patches, group_names = [], []
        for group_name, tree_group in tree_groups.items():
            patches_group = []
            for tree in tree_group.getTrees():
                x, y = tree.getPosition()
                left = min(left, x)
                rigth = max(rigth, x)
                top = max(top, y)
                bottom = min(bottom, y)
                geo = tree.getGeometry()
                r = geo["r_crown"]
                patches_group.append(patch.Circle((x, y), r))
            patches.append(patches_group)
            group_names.append(group_name)
        handles = []
        for patches_group, group_name in zip(patches, group_names):

            p = PatchCollection(patches_group,
                                alpha=1,
                                linewidths=1,
                                facecolors=colors.colors[i],
                                edgecolors="k",
                                label=tree_group.name)
            leg = patch.Patch(color=colors.colors[i], label=group_name)
            handles.append(leg)

            i += 1
            self.ax.add_collection(p)
        plt.legend(handles=handles, loc=1)

        timestring = self.createTimestring(time)

        ex_x = rigth - left
        ex_y = top - bottom
        if ex_y > ex_x:
            left = rigth - ex_y
        elif ex_x > ex_y:
            bottom = top - ex_x
        self.ax.set_xlim(left, rigth)
        self.ax.set_ylim(bottom, top)
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
