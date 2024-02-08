Example species file to be used with ``pyMANGA.PlantModelLib.Kiwi``.

The file contains the parameterization of 
- the KIWI tree
- the field of neighborhood (FON) of a tree 
- the response function of the tree to salinity.

Parameterization of the Kiwi tree is similar to <a href="https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>.

The response function to salinity (``r_salinity``) is 'forman', indicating the use of a sigmoid function to calculate the effect of salinity on plant growth (see `pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity`).

## References

<a href="https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>,
<a href="https://doi.org/10.1046/j.1365-2745.1998.00233.x" target="_blank">Chen & Twilley (1998)</a>

## See Also

``pyMANGA.PlantModelLib.Kiwi``, `pyMANGA.ResourceLib.BelowGround.Individual.FON`, `pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity`
