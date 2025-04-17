Example species file to be used with ``pyMANGA.PlantModelLib.Saltmarsh``, representing a PFT or species of saltmarh species.

The file contains the parameterization of 
- the initial saltmarsh plant geometry
- the response function of the plant to salinity.

The response function to salinity (``r_salinity``) is 'forman', indicating the use of the phenomenological approach presented in <a href="https://doi.org/10.1046/j.1365-2745.1998.00233.x" target="_blank">Chen and Twilley (1998)</a>  to calculate the effect of salinity on plant growth (see `pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity`).
