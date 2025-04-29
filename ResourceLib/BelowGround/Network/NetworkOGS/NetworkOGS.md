# Description

This module is a combination of ``pyMANGA.ResourceLib.BelowGround.Network.Network`` and ``pyMANGA.ResourceLib.BelowGround.Individual.OGS``.
That is, it considers water exchange between root grafted trees, mediated by the limitation in water availability caused by porewater salinity.
Pore water salinity is calculated using the [OpenGeoSys](https://www.opengeosys.org/) approach.

The module only functions with ``pyMANGA.PlantModelLib.BettinaNetwork``.

The module does not consider any other form of competition.

# Usage

*The values shown here are examples. See Attributes for more information.*

```xml
<belowground>
    <type> NetworkOGS </type>
    <f_radius> 0.25 </f_radius>
    <ogs_project_folder>Benchmarks/ExampleSetups/OGSExampleSetup</ogs_project_folder>
    <ogs_project_file>testmodel.prj</ogs_project_file>
    <source_mesh>source_domain.vtu</source_mesh>
    <bulk_mesh>testbulk.vtu</bulk_mesh>
    <python_script>python_script.py</python_script>
    <delta_t_ogs>86400</delta_t_ogs>
    <abiotic_drivers>
        <seaward_salinity>0.035</seaward_salinity>
    </abiotic_drivers>
</belowground>
```

# Attributes

- ``type`` (string): "NetworkOGS" (no other values accepted)
- ``f_radius`` (float): proportion of stem radius to set min. radius of grafted roots. Range: >0 to 1.
- ``ogs_project_folder`` (string): path to OGS files
- ``ogs_project_file`` (string): name of OGS project file
- ``source_mesh`` (string): name of source mesh file
- ``bulk_mesh`` (string): name of bulk mesh file
- ``python_script`` (string): name of python script file defining OGS boundary condition
- ``delta_t_ogs`` (int): time step length used for OGS. Can minimize computation time.
- ``abiotic_drivers`` (nesting-tag): (optional) specification of abiotic drivers
  - ``seaward_salinity`` (float): (optional) salinity of the seawater in kg/kg
  - ``tide_daily_amplitude`` (float): (optional) amplitude of daily tide. Default: 1, i.e. the daily tide varies between -1 and 1 m around the average.
  - ``tide_daily_period`` (float): (optional) period of daily tide. Default value is 12*60*60, i.e. the daily tide has a cycle of a half day.
  - ``tide_monthly_amplitude`` (float): (optional) amplitude of monthly tide. Default: 0.5, i.e. the monthly fluctuation of means varies between -.5 and .5 m around mean sea level (0m).
  - ``tide_monthly_period`` (float): (optional) period of monthly tide. Default: 24*60*60*15, i.e. the monthly tide has a cycle of 15 days.

For additional but optional values please see the documentation for ``pyMANGA.ResourceLib.BelowGround.Network.Network`` and ``pyMANGA.ResourceLib.BelowGround.Individual.OGS``.

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

This module mainly contains functions found in ``pyMANGA.ResourceLib.BelowGround.Network.Network'' and ``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity''.
The following lists the main functions and who they inherit from.

- ``getInputParameters``: both
- ``prepareNextTimeStep``: both
- ``addPlant``: Network, calls single OGS funtion
- ``addPsiOsmo``: NEW - see below
- ``calculateBelowgroundResources``: both

### addPsiOsmo

Create an array of osmotic potential values based on the values stored in the network attributes (this is the
osmotic potential calculated at the end of the last time step). 
When a new plant is recruited with osmotic potential = 0, the initial value is approximated by averaging the osmotic potentials of the other plants.

Note: This may lead to inaccurate initial values if 
(i) the time step length of MANGA is very large and
(ii) when plants are recruited and there are no or few other plants.

## Application & Restrictions

- This module only works properly with the growth module ``pyMANGA.PlantModelLib.BettinaNetwork``.

# References

-

# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.PlantModelLib.BettinaNetwork``,
[OpenGeoSys](https://www.opengeosys.org/)

# Examples

-

