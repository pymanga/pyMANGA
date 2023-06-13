#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from matplotlib import patches as patch
from matplotlib import pyplot as plt
from VisualizationLib.Visualization import Visualization
import pandas as pd
import numpy as np
from matplotlib.gridspec import GridSpec

class ComplexPyplot(Visualization):

    def __init__(self, args):
        self.case = args.find("type").text

        print("Initiate visualization of type " + self.case + ".")
        try:
            self._pause = float(args.find("max_fps").text)
        except AttributeError:
            self._pause = 3
            print("Tag 'max_fps' in '" + self.case +
                  "' visualization is missing! max_fps set to 50.")

        fig = plt.figure(figsize=(4, 4),
                         constrained_layout=False)
        gs = GridSpec(4, 4)
        self._ax1 = fig.add_subplot(gs[:, :])


    ## Update function necessary for all visualization classes.
    #  This function updates the subplot displaying positions
    #  and crown radius of all individual trees. Hereby, the
    #  distinct tree groups are indicated by varying colors. The
    #  Plotsize is derived from the distribution of trees, such
    #  that all tree centers a shown.
    #  @param tree_groups - list of tree groups as processes by
    #  Manga.\n
    #  @param time - double indicating current time
    def update(self, tree_groups, time):
        def legend_without_duplicate_labels(ax):

            handles, labels = ax.get_legend_handles_labels()
            unique = [(h, l) for i, (h, l) in enumerate(zip(handles,
                                                            labels)
                                                        ) if l not in labels[:i]]
            ax.legend(*zip(*unique), framealpha=1, shadow=False, loc=1)

        max_x = []
        min_x = []
        max_y = []
        min_y = []
        trees = []
        random = True

        for group_name, tree_group in tree_groups.items():

            if tree_group.distribution_type == 'Random':

                if random is True:
                    max_x.append(tree_group.x_1 + tree_group.l_x)
                    min_x.append(tree_group.x_1)
                    max_y.append(tree_group.y_1 + tree_group.l_y)
                    min_y.append(tree_group.y_1)
                else:
                    random = False
            else:
                random = False

            species = tree_group.species
            n = []
            x = []
            y = []
            r = []
            s = []
            c = []

            for tree in tree_group.getTrees():
                n.append(species + ': ' + group_name)
                if species == 'Avicennia':
                    color = 'darkolivegreen'
                elif species == 'Rhizophora':
                    color = 'greenyellow'
                else:
                    color = 'black'

                xx, yy = tree.getPosition()
                x.append(xx)
                y.append(yy)
                r.append(tree.getGeometry()["r_crown"])
                c.append(color)
                try:
                    s.append(tree.getGrowthConceptInformation()['salinity'])
                except:
                    s.append(np.nan)
            trees.append(pd.DataFrame(list(zip(n, x, y, r, s, c)),
                         columns=['name', 'x', 'y', 'r', 's', 'c']))

        for group in trees:

            if random is False:
                max_x.append(max(group['x']))
                min_x.append(min(group['x']))
                max_y.append(max(group['y']))
                min_y.append(min(group['y']))
            for n in group.index:
                circle = patch.Circle((group['x'][n], group['y'][n]),
                                      radius=group['r'][n],
                                      label=group['name'][n],
                                      color=group['c'][n])
                self._ax1.add_patch(circle)

                legend_without_duplicate_labels(self._ax1)

        max_x = max(max_x) + 2
        min_x = min(min_x) - 2
        max_y = max(max_y) + 2
        min_y = min(min_y) - 2

        self._ax1.set(
            aspect='equal',
            xlim=(min_x, max_x),
            ylim=(min_y, max_y),
            xlabel='x [m]',
            ylabel='y [m]',
            title='Time: ' + self.createTimestring(time))

        plt.draw()
        plt.pause(self._pause)

    ## Show function necessary for all visualization classes.
    #  This function displays the current state of the subplot.\n
    #  @param time - current time.
    def show(self, time):

        plt.show()

    ## This member function converts the argument to a string.
    #  Used in update()
    def createTimestring(self, arg):

        timestring = ""
        if (type(arg) == float):
            arg = arg / (60 * 60 * 24 * 365.25)
            timestring = "%2.2f" % arg + ' a'
        else:
            timestring = str(arg)
        return timestring
