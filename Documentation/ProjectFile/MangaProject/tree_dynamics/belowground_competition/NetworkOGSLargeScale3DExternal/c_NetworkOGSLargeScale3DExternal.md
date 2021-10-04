

`NetworkOGSLargeScale3DExternal` below-ground competition concept.   
The concept allows the usage of MANGA as boundary condition in OGS.
Example files to start OGS (`runModel.py`) and to define MANGA as boundary condition (`python_source.py`) can be found in the directory of below-ground concept `OGSLargeScale3DExternal`.  

The concept returns a value between 0 and 1 for each tree added to it. 
Hereby, the reduction factor is calculated as the fraction of real resource uptake due to salinity dependent reduction of water uptake and the hypothetical maximal water uptake at zero salinity.   

All files and parameters required are similar to `NetworkOGSLargeScale3D`.

