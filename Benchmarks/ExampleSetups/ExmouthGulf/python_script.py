import OpenGeoSys

import vtk as vtk
import numpy as np
from math import pi, sin
import os
from scipy.interpolate import interp1d


#seaward_salinity = 0.05
#tide_daily_amplitude = .7
#tide_monthly_amplitude = .35
#tide_yearly_amplitude = .2
#tide_daily_period = 60 * 60 * 12.
#tide_monthly_period = 60. * 60 * 24 * 31 / 2.
#tide_yearly_period = 60. * 60 * 24 * 365.25 / 2.
#def tidal_cycle(t):
#    return (sin(2 * pi * t / tide_daily_period) *
#            (tide_daily_amplitude +
#             tide_monthly_amplitude * sin(2 * pi * t / tide_monthly_period) +
#             tide_yearly_amplitude * sin(2 * pi * t / tide_yearly_period)))
def tidal_cycle(t):
    tide_value = tidal_cycle_int(t)
    return tide_value


def pressure_value(z, tidal_cycle):
    return 1000 * 9.81 * (tidal_cycle - z)


def evaporation(salinity):
    year = (365.25 * 24 * 60 * 60)

    return -3.144 / year * 1000 * (
        0.0)  #https://researchlibrary.agric.wa.gov.au/cgi/viewcontent


## Dirichlet BCs
class BCSea_p_D(OpenGeoSys.BoundaryCondition):

    def __init__(self):
        OpenGeoSys.BoundaryCondition.__init__(self)
        self.t_check = 0
        self.tide = 0

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        if t > self.t_check:
            self.tide = tidal_cycle(t % t_mod)
            self.t_check = t
        value = pressure_value(z, self.tide)
        if self.tide < z:
            return (False, 0)
        else:
            return (True, value)


class BCSea_p_N(OpenGeoSys.BoundaryCondition):

    def __init__(self):
        OpenGeoSys.BoundaryCondition.__init__(self)
        self.t_check = 0
        self.tide = 0

    def getFlux(self, t, coords, primary_vars):
        Jac = [0.0, 0.0]
        salinity = primary_vars[1]
        x, y, z = coords
        if t > self.t_check:
            self.tide = tidal_cycle(t % t_mod)
            self.t_check = t
        value = evaporation(salinity)
        #return (False, 0, Jac)
        if self.tide < z:
            return (True, value, Jac)
        else:
            return (False, 0, Jac)


## Dirichlet BCs
class BCSea_C(OpenGeoSys.BoundaryCondition):

    def __init__(self):
        OpenGeoSys.BoundaryCondition.__init__(self)
        self.t_check = 0
        self.tide = 0

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        if t > self.t_check:
            self.tide = tidal_cycle(t % t_mod)
            self.t_check = t
        value = seaward_salinity
        if self.tide > z:
            return (True, value)
        else:
            return (False, 0)



file = open("Benchmarks/ExampleSetups/ExmouthGulf/EXM_Jan-Jul_2019.txt")
t_base = 0
h_s = []
t_s = []

for line in file.readlines():
    line = (line.strip("\n").strip("/").split(","))
    h = float(line[0])
    t = float(line[1].split(".")[1][:2]) * 60 + float(
        line[1].split(".")[1][2:])
    t_s.append((t + t_base) * 60)
    h_s.append(h)
    #print(h)
    if t == 1435.0:
        t_base += 24 * 60
timeList = np.array(t_s)

signalList = (np.array(h_s) - np.mean(np.array(h_s))) / 100.
tidal_cycle_int = interp1d(timeList - min(timeList), signalList)
t_mod = (max(timeList) - min(timeList))

cumsum_savename = "cumsum_salinity.npy"
calls_savename = "calls_in_last_timestep.npy"

# instantiate source term object referenced in OpenGeoSys' prj file

bc_tide_p_D = BCSea_p_D()
bc_tide_p_N = BCSea_p_N()
bc_tide_C = BCSea_C()
