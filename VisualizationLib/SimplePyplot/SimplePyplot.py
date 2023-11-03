#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from matplotlib import patches as patch
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib import lines
from matplotlib.collections import PatchCollection
from VisualizationLib.Visualization import Visualization


class SimplePyplot(Visualization):

    def __init__(self, args):
        self.case = args[0].find("type").text

        try:
            self._fps = float(args.find("fps").text)
        except AttributeError:
            self._fps = 50
            print("Tag 'fps' in '" + self.case +
                  "' visualization is missing! fps set to 50.")
        fig, self._ax = plt.subplots(figsize=(10, 10))

    ## Update function necessary for all visualization classes.
    #  This function updates the subplot displaying positions
    #  and crown radius of all individual trees. Hereby, the
    #  distinct tree groups are indicated by varying colors. The
    #  Plotsize is derived from the distribution of trees, such
    #  that all tree centers a shown.
    #  @param plant_groups - list of tree groups as processes by
    #  Manga.\n
    #  @param time - double indicating current time
    def update(self, plant_groups, time):
        self._ax.clear()
        patches = []
        left, bottom = 99999, 99999
        rigth, top = -99999, -99999
        colors = cm.get_cmap('viridis', len(plant_groups.items()))
        i = 0
        patches, group_names, we = [], [], []
        for group_name, plant_group in plant_groups.items():
            patches_group = []
            for tree in plant_group.getPlants():
                x, y = tree.getPosition()
                left = min(left, x)
                rigth = max(rigth, x)
                top = max(top, y)
                bottom = min(bottom, y)
                geo = tree.getGeometry()
                r = geo["r_crown"]
                patches_group.append(patch.Circle((x, y), r))
                # network
                network = tree.getNetwork()
                partners = network['partner']
                we.append(network['water_exchanged'])
                for partner in partners:
                    for group_name, plant_group in plant_groups.items():
                        for tree in plant_group.getPlants():
                            foundpartner = str(tree.group_name) + str(
                                tree.plant_id)
                            if partner == foundpartner:
                                x2, y2 = tree.getPosition()
                                line = lines.Line2D([x, x2], [y, y2])
                                self._ax.add_line(line)

            patches.append(patches_group)
            group_names.append(group_name)
        handles = []
        for patches_group, group_name in zip(patches, group_names):
            p = PatchCollection(patches_group,
                                alpha=1,
                                linewidths=1,
                                facecolors=colors.colors[i],
                                edgecolors="k",
                                label=plant_group.name)
            leg = patch.Patch(color=colors.colors[i], label=group_name)
            handles.append(leg)

            i += 1
            self._ax.add_collection(p)

        plt.legend(handles=handles, loc=1)

        timestring = self.createTimestring(time)

        ex_x = rigth - left
        ex_y = top - bottom
        if ex_y > ex_x:
            left = rigth - ex_y / 2.
            rigth = left + ex_y
        elif ex_x > ex_y:
            bottom = top - ex_x / 2.
            top = bottom + ex_x
        self._ax.set_xlim(left, rigth)
        self._ax.set_ylim(bottom, top)
        plt.title("Time = " + timestring + "years")
        plt.draw()
        plt.pause(1 / self._fps)

    ## Show function necessary for all visualization classes.
    #  This function displays the current state of the subplot.\n
    #  @param time - current time.
    def show(self, time):
        plt.title("Time = " + str(time) + "years")
        plt.show()

    ## This member function converts the argument to a string.
    #  Used in update()
    def createTimestring(self, arg):
        timestring = ""
        if (type(arg) == float):
            arg = arg / (60 * 60 * 24 * 365.25)
            timestring = "%2.2f" % arg
        else:
            timestring = str(arg)
        return timestring
