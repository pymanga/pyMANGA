# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 09:21:17 2023

@author: Jonas
"""

import numpy as np
import matplotlib.pyplot as plt

U = np.arange(0, 160, 5)

############################################
############### Avicennia   ################

U_i = 72
d = - 0.18

salinity_A = 1 / (1 + np.exp(d * (U_i - U)))

############################################
############### Rhizophora  ################

U_i = 58
d = - 0.25

salinity_R = 1 / (1 + np.exp(d * (U_i - U)))

############################################
############### Laguncularia ###############

U_i = 65
d = - 0.2

salinity_L = 1 / (1 + np.exp(d * (U_i - U)))

############################################
############### Saltmarsh 1 ################

U_i = 80
d = - 0.1

salinity_s1 = 1 / (1 + np.exp(d * (U_i - U)))

############################################
############### Saltmarsh 2 ################

U_i = 90
d = - 0.1

salinity_s2 = 1 / (1 + np.exp(d * (U_i - U)))

############################################
############### Saltmarsh 3 ################

U_i = 100
d = - 0.05

salinity_s3 = 1 / (1 + np.exp(d * (U_i - U)))


fig = plt.figure(figsize=(10, 5), constrained_layout=True)
ax = fig.add_subplot(111)
ax.plot(U, salinity_A, '--', label='Avicennia')
ax.plot(U, salinity_L, '--', label='Laguncularia')
ax.plot(U, salinity_R, '--', label='Rhizophora')
ax.plot(U, salinity_s1, label='Saltmarsh 1', color='peru')
ax.plot(U, salinity_s2, label='Saltmarsh 2', color='blue')
ax.plot(U, salinity_s3, label='Saltmarsh 3', color='red')
ax.set(xlabel='salinity [ppt]',
       ylabel='Belowground Resource [-]')
ax.legend()
fig.savefig('forman.png', dpi=1080)
