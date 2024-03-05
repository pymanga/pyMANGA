import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# input: lat (radians), monthly tmin and tmax (deg C) 
tmin = [23.1,23.2,23.6,24.6,25.2,24.9,24.7,24.7,25.1,24.8,24.4,23.7]
tmax = [29.9,29.8,30.2,30.6,31,30.9,30.8,31.2,31.5,31.3,30.9,30.3]
lat = 0.65
doy15 = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349] # may to november doy[4:11]

monthlyNetRad = []
for doy, tmin, tmax in zip(doy15, tmin, tmax): #not 365 because we want 12x1st of month
    a = 0.23 # green vegetation has an albedo of about 0.20-0.25 (Allen et al, 1998).
    # solar declination
    d = 0.409*np.sin((2*np.pi/365)*doy-1.39)
    # sunset hour angle 
    w_s_temp = -np.tan(lat)*np.tan(d) # if >= 1, 24hrs of daylight, if <= -1, 24hrs of darkness (see pyeto docs)
    w_s = np.arccos(min(max(w_s_temp, -1), 1))
    # inverse relative distance Earth-Sun based on doy
    ird = 1 + (0.033*np.cos((2*np.pi/365)*doy))
    # extraterrestrial radiation
    R_a_temp1 = ((24*60)/np.pi)
    R_a_temp2 = w_s * np.sin(lat) * np.sin(d)
    R_a_temp3 = np.cos(lat) * np.cos(d) * np.sin(w_s)
    R_a = R_a_temp1 * 0.0820 * ird * (R_a_temp2 + R_a_temp3)
    # incoming solar radiation 
    R_s = (0.7*R_a)-4 # assuming island #(0.25 + (0.5 * N))*R_a
    # net shortwave radiation
    R_ns = (1-a)*R_s
    # actual vapor pressure
    e_a = 0.611 * np.exp((17.27 * tmin) / (tmin + 237.3)) # substract 2 deg C from tmin in arid/semi arid areas
    # clear sky radiation
    altitude = 0
    R_so = (0.00002 * altitude + 0.75)*R_a
    # net longwave radiation
    R_nl = 0.000000004903*(((tmax)**4+(tmin)**4)/2)*(0.34-(0.14*np.sqrt(e_a)))*(1.35*(R_s/R_so)-0.35)

    # daily net radiation
    R_n = R_ns - R_nl   

    # save dailyNetRad to list
    monthlyNetRad.append(R_n)

monthlyNetRad_factor = [x / max(monthlyNetRad) for x in monthlyNetRad]
# time = [int(365 / 11 * i) for i in range(12)]

# define the sine function

def sine_function(t, amplitude, frequency, phase_shift, vertical_shift):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase_shift) + vertical_shift # 2pi for radians

# fit the sine function to the data
popt, pcov = curve_fit(sine_function, doy15, monthlyNetRad_factor)

# extrapolate over a year
timespan = np.arange(1, 365, 1)#range(1, 366)
NetRad_fit = sine_function(timespan, *popt) 

# adding noise 
# noise can only produce values below the sine function since the sine function assumes clear sky radiation and with that the maximum possible radiation
# noise is currently  based on standard deviation of the fitted function. 
# Barr et al (2014) suggest that radiation can approach 0 and also suggests average radiation to be nearly constant from May to November
# The nearly constant moving average is not ecplicitly implemented but can be sufficiently assumed.   
# https://doi.org/10.1002/2013JD021083
noise = 0.5*np.std(NetRad_fit)
NetRad_fit_noise = NetRad_fit + np.random.normal(scale = noise, size = NetRad_fit.shape)


# add higher noise to values in summer to more closely resemble near constant moving average from May to November (Barr et al, 2014)
condition = (timespan >= 105) & (timespan <= 250)
higher_noise = 4*np.std(NetRad_fit[condition])
NetRad_fit_noise[condition] -= + np.random.normal(scale = higher_noise, size = NetRad_fit[condition].shape) 

NetRad_fit_noise = np.clip(NetRad_fit_noise, 0, NetRad_fit)

# plot
plt.figure()
plt.scatter(doy15, monthlyNetRad_factor, label='input data', color="tab:blue")
plt.plot(timespan, NetRad_fit, '-', label='fitted sine function', color="tab:blue")
plt.plot(timespan, NetRad_fit_noise, '-', label='noise', color="grey", alpha = 0.5, linewidth = 0.5)
# plt.scatter(doy15, pyeto_monthlyNetRad_factor, color="tab:orange", label='pyeto reference')
# plt.plot(timespan, pyeto_NetRad_fit, '-', color="tab:orange", label='pyeto fit')
plt.xlabel('doy')
plt.ylabel('NetRad (factor)')
plt.legend()
plt.title("Grenada")
plt.show()