# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:57:54 2022

@author: Jonas
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as patch

# filepath_examplesetups = path.join(path.dirname(path.abspath(__file__)),
#                                    "testSetupsWithoutOGS/*.xml")

outputs = glob.glob(r".\Gradient\*.csv")

datas = []

for output in outputs:
    datas.append(pd.read_csv(output, sep='\t'))



all_datas = pd.concat(datas)

all_datas = all_datas.sort_values("time")

time = all_datas['time'].drop_duplicates(ignore_index=True)

for n in time:

    data = all_datas[all_datas['time'] == n].sort_values('h_ag',
                                                         ignore_index=True)

    fig = plt.figure(figsize=(10, 5), constrained_layout=True)
    ax = fig.add_subplot(111)
    ax.set(xlim=(0, 20),
           ylim=(0, 5),
           xlabel='x [m]',
           ylabel='y [m]',
           aspect='equal')

    k = 0
    for k in range(data.shape[0]):

        species = data['plant'][k][0:11]

        if species == 'saltmarsh_1':
            label = 'Saltmarsh 1'
            color = 'peru'
        elif species == 'saltmarsh_2':
            label = 'Saltmarsh 2'
            color = 'green'
        elif species == 'saltmarsh_3':
            label = 'Saltmarsh 3'
            color = 'red'

        circle = patch.Circle((data['x'][k],
                              data['y'][k]),
                              radius=data['r_ag'][k],
                              color=color,
                              label=label)
        ax.add_patch(circle)
    fig.savefig('gradient/fig/ts_' + str(n) + '.png')
    plt.close('all')
    k += 1


    # saltmarsh_detail[0].append(temp[0])
    # saltmarsh_detail[1].append(temp[1])
    # saltmarsh_detail[2].append(temp[2])
    # saltmarsh_detail[3].append(temp[3])

    # if avicennia[n].shape[0] > 0:
    #     temp = [0, 0, 0, 0]
    #     for k in range(avicennia[n].shape[0]):
    #         circle = patch.Circle((avicennia[n]['x'][k],
    #                               avicennia[n]['y'][k]),
    #                               radius=avicennia[n]['r_crown'][k],
    #                               color='peru')
    #         ax.add_patch(circle)
    #         circle = patch.Circle((avicennia[n]['x'][k],
    #                               avicennia[n]['y'][k]),
    #                               radius=avicennia[n]['r_crown'][k],
    #                               color='brown',
    #                               fill=False)
    #         ax.add_patch(circle)

    #         if float(avicennia[n]['volume'][k]) > 0:

    #             if avicennia[n]['x'][k] < 25:
    #                 temp[0] += float(avicennia[n]['volume'][k])
    #             elif avicennia[n]['x'][k] < 50:
    #                 temp[1] += float(avicennia[n]['volume'][k])
    #             elif avicennia[n]['x'][k] < 75:
    #                 temp[2] += float(avicennia[n]['volume'][k])
    #             elif avicennia[n]['x'][k] < 100:
    #                 temp[3] += float(avicennia[n]['volume'][k])

    # avicennia_detail[0].append(temp[0])
    # avicennia_detail[1].append(temp[1])
    # avicennia_detail[2].append(temp[2])
    # avicennia_detail[3].append(temp[3])

    # text = ('Avicennia: ' + str(avicennia[n].shape[0]))
    # ax.text(0.01, 0.95, text, transform=ax.transAxes, fontsize=14,
    #         color='brown', verticalalignment='top', bbox=box)
    # text = 'Saltmarsh: ' + str(saltmarsh[n].shape[0])
    # ax.text(0.99, 0.95, text, transform=ax.transAxes, fontsize=14,
    #         color='green', verticalalignment='top',
    #         horizontalalignment='right', bbox=box)
    # ax.set(xlim=(0, 100), ylim=(0, 20),
    #        xlabel='x [$m$]',
    #        ylabel='y [$m$]',
    #        title='Time: %4.2f a' % (float(avicennia[n]['time'][0])/86400/365))
    # ax.set_aspect('equal')
    # fig.savefig(
    #     'post/Time_%4.2f_a.png' % (float
    #                                (avicennia[n]['time'][0])/86400/365))
    # x_max = max(max
    #             (max(saltmarsh_detail[0]),
    #              max(saltmarsh_detail[1]),
    #              max(saltmarsh_detail[2]),
    #              max(saltmarsh_detail[3])),
    #             max(
    #                 (max(avicennia_detail[0]),
    #                  max(avicennia_detail[1]),
    #                  max(avicennia_detail[2]),
    #                  max(avicennia_detail[3]))))
    # fig_2 = plt.figure(figsize=(10, 5), constrained_layout=True)
    # ax = fig_2.add_subplot(141)
    # ax.plot(saltmarsh_detail[0], label='x_1')
    # ax.plot(avicennia_detail[0], label='x_1')
    # ax_2 = fig_2.add_subplot(142)
    # ax_2.plot(saltmarsh_detail[1], label='x_2')
    # ax_2.plot(avicennia_detail[1], label='x_2')
    # ax_3 = fig_2.add_subplot(143)
    # ax_3.plot(saltmarsh_detail[2], label='x_3')
    # ax_3.plot(avicennia_detail[2], label='x_3')
    # ax_4 = fig_2.add_subplot(144)
    # ax_4.plot(saltmarsh_detail[3], label='x_4')
    # ax_4.plot(avicennia_detail[3], label='x_4')
    # ax.set(ylim=(1E-1, x_max), yscale='log')
    # ax_2.set(ylim=(1E-1, x_max), yscale='log')
    # ax_3.set(ylim=(1E-1, x_max), yscale='log')
    # ax_4.set(ylim=(1E-1, x_max), yscale='log')
    # fig_2.savefig(r'post/biomass.png', dpi=1080)



# middle_index = int(len(datas) / 2)

# avicennia = datas[:middle_index]
# saltmarsh = datas[middle_index:]

# box = dict(boxstyle='round', facecolor='white')

# saltmarsh_detail = [[], [], [], []]
# avicennia_detail = [[], [], [], []]

# if float(saltmarsh[n]['volume'][k]) > 0:

#     if saltmarsh[n]['x'][k] < 25:
#         temp[0] += float(saltmarsh[n]['volume'][k])
#     elif saltmarsh[n]['x'][k] < 50:
#         temp[1] += float(saltmarsh[n]['volume'][k])
#     elif saltmarsh[n]['x'][k] < 75:
#         temp[2] += float(saltmarsh[n]['volume'][k])
#     elif saltmarsh[n]['x'][k] < 100:
#         temp[3] += float(saltmarsh[n]['volume'][k])
