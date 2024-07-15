Example species file to be used with ``pyMANGA.PlantModelLib.Bettina``, representing _Rhizophora mangle_ (black mangrove).

The file contains the parameterization of 
- the BETTINA tree
- the field of neighborhood (FON) of a tree 
- the response function of the tree to salinity.

Parameterization of the Bettina tree is similar to <a href="https://doi.org/10.1016/j.agrformet.2021.108547" target="_blank">Bathmann et al. (2021)</a>.

The response function to salinity (``r_salinity``) is 'bettina', indicating the use of the mechanistic approach presented in <a href="https://doi.org/10.1016/j.ecolmodel.2014.04.001" target="_blank">Peters et al. (2014)</a>  to calculate the effect of salinity on plant growth (see `pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity`).

## References

<a href="https://doi.org/10.1016/j.agrformet.2021.108547" target="_blank">Bathmann et al. (2021)</a>,
<a href="https://doi.org/10.1016/j.ecolmodel.2014.04.001" target="_blank">Peters et al. (2014)</a>

## See Also

``pyMANGA.PlantModelLib.Bettina``, `pyMANGA.ResourceLib.BelowGround.Individual.FON`, `pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity`
