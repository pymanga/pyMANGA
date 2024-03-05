#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024-January
@author: github.com/rbnmj/
"""
import datetime
import numpy as np
from scipy.optimize import curve_fit
from ResourceLib import ResourceModel

class SolarRadiation(ResourceModel):
    """
    Solar radiation model based on Allen et al. 1998.
    Requires daily minimum and maximum temperature, latitude and day of the year.
    Fits a sine curve to monthly average minimum and maximum temperature.
    Sine parameters are then used to estimate net radiation for any day of the year skipping the calculations.
    """
    def __init__(self, args):
        case = args.find("SolarRadiation").text
        self.getInputParameters(args)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["radiation", "day_of_year", "latitude", "tmin", "tmax"]
        }
        super().getInputParameters(**tags)
        self._doy = self.day_of_year #day of the year
        self._latitude = self.latitude
        self._tmin = self.tmin
        self._tmax = self.tmax

    def calculateMonthlyRadiation(self):
        """ 
        Calculates daily net radiation based on Allen et al 1998.
        """
        self.monthly_net_rad = []
        self.doy15 = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349] # 15th of each month
        for doy, tmin, tmax in zip(self.doy15, self.tmin, self.tmax):
            a = 0.23 # green vegetation has an albedo of about 0.20-0.25 (Allen et al, 1998).
            # solar declination
            d = 0.409*np.sin((2*np.pi/365)*doy-1.39)
            # sunset hour angle 
            w_s_temp = -np.tan(self._latitude)*np.tan(d) # if >= 1, 24hrs of daylight, if <= -1, 24hrs of darkness (see pyeto docs)
            w_s = np.arccos(min(max(w_s_temp, -1), 1))
            # inverse relative distance Earth-Sun based on doy
            ird = 1 + (0.033*np.cos((2*np.pi/365)*doy))
            # extraterrestrial radiation
            r_a_temp1 = ((24*60)/np.pi)
            r_a_temp2 = w_s * np.sin(self._latitude) * np.sin(d)
            r_a_temp3 = np.cos(self._latitude) * np.cos(d) * np.sin(w_s)
            r_a = r_a_temp1 * 0.0820 * ird * (r_a_temp2 + r_a_temp3)
            # incoming solar radiation 
            r_s = (0.7*r_a)-4 # assuming island #(0.25 + (0.5 * N))*R_a
            # net shortwave radiation
            r_ns = (1-a)*r_s
            # actual vapor pressure (substract 2 deg C from tmin in arid/semi arid areas)
            e_a = 0.611 * np.exp((17.27 * tmin) / (tmin + 237.3)) 
            # clear sky radiation
            altitude = 0
            r_so = (0.00002 * altitude + 0.75)*r_a
            # net longwave radiation
            r_nl = 0.000000004903*(((tmax)**4+(tmin)**4)/2)*(0.34-(0.14*np.sqrt(e_a)))*(1.35*(r_s/r_so)-0.35)

            # daily net radiation
            r_n = r_ns - r_nl  

            self.monthly_net_rad.append(r_n)
    
    def sineFunction(self, t, amplitude, frequency, phase_shift, vertical_shift):
        """
        Sine function to fit to the monthly net radiation
        """
        return amplitude * np.sin(2 * np.pi * frequency * t + phase_shift) + vertical_shift

    def fitRadiation(self):
        """ 
        Fits a sine curve to the calculated monthly net radiation to estimate daily net radiation 
        """
        popt, pcov = curve_fit(self.sineFunction(), self.doy15, self.monthly_net_rad)
        self.sinus_params = popt
    
    def estimateDailyRadiation(self, doy):
        """ 
        Estimates net radiation for any day of the year based on the fitted sine curve and adds noise.
        """
        noise = np.random.normal(0,0.15) # +- 15% 
        net_rad_raw = self.sineFunction(doy, *self.sinus_params)
        self.net_rad = np.clip(net_rad_raw + noise, 0, net_rad_raw)

        return self.net_rad
    
    def factorDailyRadiaton(self):
        """ 
        Scales radiation between 0 and 1 to make it accessable for the resource model.
        """
        self.net_rad_factor = self.net_rad / max(self.net_rad)
        return self.daily_net_rad_factor