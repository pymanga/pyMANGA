import pyeto
import matplotlib.pyplot as plt

# input 
lat = 0.9
tmin = 1.3 
tmax = 5.6 

# assumptions
albedo = 0.23 
altitude = 0 

yearlyNetRad = []

# iterate over 365 days starting from 0
for day in range(1, 366):
    solDec = pyeto.sol_dec(day)
    sHA = pyeto.sunset_hour_angle(lat, solDec)
    iRD = pyeto.inv_rel_dist_earth_sun(day)
    etRad = pyeto.et_rad(lat, solDec, sHA, iRD)
    solRad = pyeto.sol_rad_island(etRad)
    netInSWRad = pyeto.net_in_sol_rad(solRad, albedo=albedo)
    CSRad = pyeto.cs_rad(altitude, etRad)
    aVP = pyeto.avp_from_tmin(tmin)
    netOutLWRad = pyeto.net_out_lw_rad(tmin, tmax, solRad, CSRad, aVP)
    dailyNetRad = pyeto.net_rad(netInSWRad, netOutLWRad)

    # save dailyNetRad to list
    yearlyNetRad.append(dailyNetRad)

plt.plot(range(0,365), yearlyNetRad)
plt.xlabel('Day of the year')
plt.ylabel('Net radiation (MJ m-2 day-1)')
plt.show()