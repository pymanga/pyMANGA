# Description

This module is a combination of ``pyMANGA.BelowGround.Individual.SaltFeedbackBucket`` and ``pyMANGA.BelowGround.Network.Network``.
That is, it calculates the reduction in below-ground resource availability caused by pore water salinity below a plant, taking into account the feedback between plant water uptake and pore water salinity AND the exchange of water between root grafted plants.

There is no direct competition.

# Usage

```xml
<belowground>
    <type> NetworkSaltFeedbackBucket </type>
    <f_radius> 0.5 </f_radius>
    <exchange> on </exchange>
        <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 88 </x_resolution>
        <y_resolution> 88 </y_resolution>
    </domain>
    <salinity> 0.035 0.035 </salinity>
    <r_mix> 0.01/3600/24 0.015/3600/24 </r_mix>
    <depth> 1 </depth>
    <sine>
        <medium> water </medium>
        <amplitude> 0.1 </amplitude>
    </sine>
    <save_salinity_ts> 120 </save_salinity_ts>
</belowground>
```

# Attributes

- ``type`` (string): "SaltFeedbackBucket" (no other values accepted)
- ``domain`` (nesting-tag): coordinates to define the model domain (as mesh)
    - ``x_1`` (float): x-coordinate of left bottom border of grid
    - ``x_2`` (float): x-coordinate of right bottom border of grid
    - ``y_1`` (float): x-coordinate of left top border of grid
    - ``y_2`` (float): x-coordinate of right top border of grid
    - ``x_resolution`` (float): x-resolution of the grid
    - ``y_resolution`` (float): y-resolution of the grid
- ``salinity`` (float float or string): either two values representing the salinity (kg/kg) at ``min_x`` and ``max_x`` <strong>or</strong> the path to a csv file containing a time series of salinity (see description above and 
        example below)
- ``r_mix`` (float or float float): one or two values defining the mixing rate (m per second) at ``x_1`` and ``x_2``. If only one value is given, the rate at ``x_1`` and ``x_2`` is equal .
- ``depth`` (float): Cell depth (corresponding to theoretical aquifer thickness). Default: 1.
- ``sine`` (nesting-tag): (optional) calculate salinity for each time step based on a sine function. See notes for details.
  - ``medium`` (string): (optional) medium to which the sinusoidal option is applied. Possible values: "salt", "water", "salt water". Default: "salt"
  - ``amplitude`` (float): (optional) amplitude of the sine function. Default: 0
  - ``stretch`` (float): (optional) stretch of the sine function, i.e., length of a full period. Default: 24\*3600\*58 (approx. 1 year)
  - ``offset`` (float): (optional) offset of the sine function (along the time axis). Default: 0
  - ``noise`` (float): (optional) standard deviation to pick salinity value from sine function. Default: 0
- ``save_salinity_ts`` (int): (optional) number indicating at which nth timestep the salinity in each cell is written to a text file. 


# Value

A list of values with length = number of plant.

Each value describes the availability of below-ground resources for a plant (dimensionless).
The factor ranges from 0 to 1, with 1 indicating no limitations and 0 indicating full limitations.


# Details
## Purpose


## Process overview

## Sub-processes

## Application & Restrictions


# References

<a href="https://doi.org/" target="_blank">Link</a>,


# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.ResourceLib.BelowGround.Network.Network``,
``pyMANGA.ResourceLib.BelowGround.Network.NetworkFixedSalinity``,
``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``,
``pyMANGA.ResourceLib.BelowGround.Individual.SaltFeedbackBucket``

# Examples


