#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024-January
@author: github.com/rbnmj/
"""
import pysolar.solar as ps
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
            "required": ["radiation", "date", "latitude", "longitude"]
        }
        super().getInputParameters(**tags)
        self._date = datetime.datetime(*self.date, tzinfo=datetime.timezone.utc)
        self._latitude = self.latitude
        self._longitude = self.longitude

    def calculateRadiation(self):
        """ 
        Calculates the daily mean solar irradiance (W/m2) for a given location and date.  
        Clear sky daily mean solar irradiance is assumed to be 1000 W/m2.  
        Calculating solar irradiance over 24 hours prevents time zone issues.  
        """
       
        irradiance = []
        for i in range(0,24):
            date = self._date + datetime.timedelta(hours=i)
            altitude = ps.get_altitude(self._latitude, self._longitude, date)
            irradiance.append(ps.radiation.get_radiation_direct(date, altitude))

        # Daily mean solar irradiance
        daily_rad = np.mean(irradiance)

        # Scale to maximal daily mean solar irradiance
        max_rad = 1000 # on a clear day
        rad_scaled = daily_rad / max_rad

        return rad_scaled