# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:48:29 2023

@author: Jonas
"""

import os
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patch
from scipy.interpolate import griddata
import matplotlib.patches as patch


def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles,
                                                    labels)
                                                ) if l not in labels[:i]]
    ax.legend(*zip(*unique), framealpha=1, shadow=False, loc=1)


result_files =\
    glob.glob(r'C:\Users\Jonas\Documents\MASCOT\SourceCode\pyMANGA-1\MyModel\Outputs\OnePlant\*.csv')

pj = '0.7_0.3_0.3'

if not os.path.exists('fig/OnePlant_ill/' + pj):

    os.makedirs('fig/OnePlant_ill/' + pj)

# result_files_avi = glob.glob('A*.csv')
# result_files_rhi = glob.glob('R*.csv')

files_avi = []
files_rhi = []
salt_lims = []
files = []

# for result_file in result_files_avi:
#     file = pd.read_csv(result_file, sep='\t')
#     files_avi.append(file)
#     salt_lims.append((min(file['salinity']), max(file['salinity'])))

# for result_file in result_files_rhi:
#     file = pd.read_csv(result_file, sep='\t')
#     files_rhi.append(file)
#     salt_lims.append((min(file['salinity']), max(file['salinity'])))


# all_trees = pd.concat([pd.concat(files_rhi),
#                        pd.concat(files_avi)]).sort_values('time',
#                                                           ignore_index=True)

for result_file in result_files:
    file = pd.read_csv(result_file, sep='\t')
    files.append(file)
    # salt_lims.append((min(file['salinity']), max(file['salinity'])))

# salt_lim = (np.nanmin(salt_lims), np.nanmax(salt_lims))
# levels = np.linspace(np.nanmin(salt_lims),
#                      np.nanmax(salt_lims), num=11).round(3)

x, y = np.meshgrid(np.linspace(0, 50, 51), np.linspace(0, 10, 11))

all_trees = pd.concat(files)

all_trees['time'] = all_trees['time'] / 3600 / 24

n = 1

for result_file in result_files:

    fig = plt.figure(figsize=(10, 16), constrained_layout=False)

    gs = GridSpec(23, 8)

    ax1 = fig.add_subplot(gs[0:5, :])
    ax2 = fig.add_subplot(gs[6:11, :])
    ax3 = fig.add_subplot(gs[12:17, :])
    ax4 = fig.add_subplot(gs[18:23, :])

    ax1.plot(all_trees['time'], all_trees['h_ag'])
    ax1.set_title('$h_{ag}$')
    ax1.set(ylabel='l [m]')

    ax2.plot(all_trees['time'], all_trees['r_ag'])
    ax2.set_title('$r_{ag}$')
    ax2.set(ylabel='l [m]')

    ax3.plot(all_trees['time'], all_trees['h_bg'])
    ax3.set_title('$h_{bg}$')
    ax3.set(ylabel='l [m]')

    ax4.plot(all_trees['time'], all_trees['r_bg'])
    ax4.set_title('$r_{bg}$')
    ax4.set(xlabel='t [d]',
            ylabel='l [m]')

    plt.savefig('geometry_plant_' + str(n))
    plt.close('all')
    n += 1

    ts = 0

    while not all_trees['r_ag'][ts] == all_trees['r_ag'][ts+1] and \
        ts < all_trees.shape[0]:

        fig = plt.figure(figsize=(4, 4), constrained_layout=True)

        ax = fig.add_subplot(111)

        ax.set(xlim=(-3, 3),
               ylim=(-3, 3),
               xlabel='x [m]',
               ylabel='y [m]',
               aspect='equal',
               title='Time: ' + str(int(all_trees['time'][ts])) + ' d')

        soil = patch.Rectangle((-5,
                                -5),
                               10,
                               5,
                               color='sandybrown')

        sky = patch.Rectangle((-5,
                               0),
                              10,
                              5,
                              color='deepskyblue')

        sun = patch.Circle((2.5, 2.5), radius=0.4, color='yellow')

        above = patch.Rectangle((-all_trees['r_ag'][ts], 0),
                                2*all_trees['r_ag'][ts],
                                all_trees['h_ag'][ts],
                                color='green')

        below = patch.Rectangle((-all_trees['r_bg'][ts],
                                 -all_trees['h_bg'][ts]),
                                2*all_trees['r_bg'][ts],
                                all_trees['h_bg'][ts],
                                color='brown')

        ax.add_patch(sky)
        ax.add_patch(sun)
        ax.add_patch(soil)
        ax.add_patch(above)
        ax.add_patch(below)

        ts += 1

        plt.savefig('fig/OnePlant_ill/' + pj + '/ts_' + str(int(all_trees['time'][ts]))
                    + '.png')
        plt.close('all')
