
Child class of OGSExternal and NetworkOGS to use external time stepping, e.g. to run MANGA as OGS boundary condition
The concept needs an array with cumulated cell salinity and the number of calls for each cell. It returns an array describing water
withdrawal in each cell as rate in kg per sec per cell volume.
The withdrawal is the amount of water absorbed from the soil column,
and can be different from the amount of water available to the plant du to
root graft mediated water exchange (see Network).