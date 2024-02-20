#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024-January
@author: github.com/rbnmj/
"""
import pyeto
import datetime
import numpy as np
from ResourceLib import ResourceModel

class SolarRadiation(ResourceModel):
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

    def calculateRadiation(self):
        """ 
        Calculates daily net radiation based on Allen et al 1998
        """
       
       # solar declination  
        solDec = pyeto.sol_dec(self._doy)

        # sunset hour angle
        sHA = pyeto.sunset_hour_angle(self._latitude, solDec)

        # inverse relative distance
        iRD = pyeto.inv_rel_dist_earth_sun(self._doy)

        # etraterrestrial radiation
        etRad = pyeto.et_rad(self._latitude, solDec, sHA, iRD)

        # solar shortwave radiation
        # An island is defined as a land mass with width perpendicular to the coastline <= 20 km. 
        # This method is only applicable for low altitudes (0-100 m) and monthly calculations.
        solRad = pyeto.sol_rad_island(etRad)

        # Default value is 0.23, which is the value used by the FAO for a short grass reference crop.
        # A green vegetation over has an albedo of about 0.20-0.25 (Allen et al, 1998).
        albedo = 0.23 

        # net incoming shortwave rad.
        netInSWRad = pyeto.net_in_sol_rad(solRad, albedo=albedo)

        ## net outgoing longwave rad estimated from:

        # clear sky radiation
        altitude = 0 # estimate for sea level
        CSRad = pyeto.cs_rad(altitude, etRad)

        # actual vapor pressure (usually from tdeq or humdity data but can be estimated from tmin)
        # recommended to substract 2 °C from tmin for arid areas (Allen et al, 1998; Annex 6)
        aVP = pyeto.avp_from_tmin(self._tmin)

        # net outgoing longwave rad.
        netOutLWRad = pyeto.net_out_lw_rad(self._tmin, self._tmax, solRad, CSRad, aVP)

        ## daily net radiation
        # Based on equation 40 in Allen et al (1998)
        dailyNetRad = pyeto.net_rad(netInSWRad, netOutLWRad)

        return dailyNetRad

        # Scale to maximal daily mean solar irradiance
        # max_rad = 
        # rad_scaled = dailyNetRad / max_rad

        # return rad_scaled

    def calculateRadiation_yearly(self):
        yearlyNetRad = []
        for self._doy in range(1, 366):
            dailyNetRad = self.calculateRadiation()
            yearlyNetRad.append(dailyNetRad)
        # plt.plot(range(0,365), yearlyNetRad)
        # plt.xlabel('Day of the year')
        # plt.ylabel('Net radiation (MJ m-2 day-1)')
        # plt.show()