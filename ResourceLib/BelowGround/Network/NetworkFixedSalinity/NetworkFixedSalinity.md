# Description

This module is a combination of ``pyMANGA.ResourceLib.BelowGround.Network.Network`` and ``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``.
That is, it considers water exchange between root grafted trees, mediated by the limitation in water availability caused by porewater salinity.

The module only functions with ``pyMANGA.PlantModelLib.BettinaNetwork``.

This module description is part of the pyNET ODD presented in <a href="https://doi.org/10.1016/j.ecolmodel.2024.110916" target="_blank">Wimmler & Berger (2024)</a>.

The module does not consider any other form of competition.


# Usage

*The values shown here are examples. See Attributes for more information.*

```xml
<belowground>
    <type> NetworkFixedSalinity </type>
    <f_radius> 0.25 </f_radius>
    <min_x>0</min_x>
    <max_x>22</max_x>
    <salinity>0.025 0.035</salinity>
</belowground>
```

# Attributes

- ``type`` (string): "NetworkFixedSalinity" (no other values accepted)
- ``f_radius`` (float): proportion of stem radius to set min. radius of grafted roots. Range: >0 to 1.
- ``min_x`` (float): x-coordinate of the left border (x = 0)
- ``max_x`` (float): x-coordinate of the right border (x = max.)
- ``salinity`` (float float or string): either two values representing the salinity (kg/kg) at ``min_x`` and ``max_x`` <strong>or</strong> the path to a csv file containing a time series of salinity (see description above and 
        example below)

For additional but optional values please see the documentation for ``pyMANGA.ResourceLib.BelowGround.Network.Network`` and ``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``.

# Value

A list of values with length = number of plant.

Each value describes the availability of below-ground resources for a plant (dimensionless). 
The factor ranges from 0 to Inf, with 1 indicating no water exchange and no water limitation, 
< 1 indicating water limitation due to salinity and/or that water flows from the focal tree to the partner and 
values > 1 indicating water flows to the focal tree and no water limitation.

# Details
## Purpose

This module describes the below-ground resource limitation caused by the presence of salt and the exchange of fresh water between root-grafted trees.
Water exchange is driven by the water potential gradient between trees.
While in ``pyMANGA.ResourceLib.BelowGround.Network.Network'' this is only influenced by tree size and distance, here the difference in pore water salinity has a major impact.
All else being equal, water would flow from the tree in the less saline soil to the tree in the more saline soil.

## Process overview

This module does not contain any functionality other than that found in ``pyMANGA.ResourceLib.BelowGround.Network.Network'' and ``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity''.
The following lists the main functions and who they inherit from.

- ``getInputParameters``: both
- ``prepareNextTimeStep``: Network
- ``addPlant``: Network
- ``calculatePsiOsmo``: FixedSalinity
- ``calculateBelowgroundResources``: Network

## Application & Restrictions

- This module only works properly with the growth module ``pyMANGA.PlantModelLib.BettinaNetwork``.

# References

<a href="https://doi.org/10.1093/aob/mcac074" target="_blank">Wimmler et al. (2022)</a>,
<a href="https://doi.org/10.1016/j.ecolmodel.2024.110916" target="_blank">Wimmler & Berger, 2024</a>

# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.PlantModelLib.BettinaNetwork``

# Examples

-
