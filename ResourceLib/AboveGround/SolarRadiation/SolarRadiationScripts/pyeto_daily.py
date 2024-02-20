import pyeto
import datetime

# input parameter

# latitude
lat = 0.9 # radians
# minimum temperature
tmin = 1.3 # celsius
# maximum temperature
tmax = 5.6 # celsius
# day of the year
date = datetime.date(1993, 12, 3).timetuple().tm_yday

## net incoming shortwave rad. estimated from:

# solar declination  
solDec = pyeto.sol_dec(date)

# sunset hour angle
sHA = pyeto.sunset_hour_angle(lat, solDec)

# inverse relative distance
iRD = pyeto.inv_rel_dist_earth_sun(date)

# etraterrestrial radiation
etRad = pyeto.et_rad(lat, solDec, sHA, iRD)

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
aVP = pyeto.avp_from_tmin(tmin)

# net outgoing longwave rad.
netOutLWRad = pyeto.net_out_lw_rad(tmin, tmax, solRad, CSRad, aVP)

## daily net radiation
# Based on equation 40 in Allen et al (1998)
dailyNetRad = pyeto.net_rad(netInSWRad, netOutLWRad)

print(dailyNetRad)