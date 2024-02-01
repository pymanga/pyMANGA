#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024-January
@author: github.com/rbnmj/
"""

import pysolar.solar as ps
import datetime
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
        Calculates the solar irradiance for the given date, latitude and longitude.  
        Returns solar irradiance in W/m^2 a time independent measure of solar radiation.  
        Daily irradiation in Wh/m^2 can be calculated by taking the sum of the hourly irradiance values.  
        The same principle applies to yearly irradiance or mean yearly irradiance.  
        """
        altitude = ps.get_altitude(self._latitude, self._longitude, self._date)
        
        rad = ps.radiation.get_radiation_direct(self._date, altitude)
        
        return rad 
    