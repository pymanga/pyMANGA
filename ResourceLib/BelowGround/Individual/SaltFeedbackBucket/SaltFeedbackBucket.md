# Description

This module calculates the reduction in below-ground resource availability caused by pore water salinity below a plant, taking into account the feedback between plant water uptake and pore water salinity.
When a plant absorbs water from the soil, it leaves behind salt, which in turn increases the salt concentration below the plant, thereby reducing water availability to the plant.
This feedback is calculated assuming that each cell is an individual bucket (1D) that does not interact with its neighbors (i.e., there is no lateral or vertical flow in the soil).

The salinity in each bucket (cell) is based on the salinity and a mixing rate at the left and right boundaries of the model.
The mixing rate describes how much water in a cell is exchanged with incoming water (where the two may have different salinities).
The salinity is based on ``pyMANGA.BelowGround.Individual.FixedSalinity``, but takes into account the feedback between plant and soil.
There is no direct competition.

# Usage

```xml
<belowground>
    <type> SaltFeedbackBucket </type>
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

See <a href="https://github.com/pymanga/sensitivity/blob/main/ResourceLib/BelowGround/Individual/SaltFeedbackBucket/SaltFeedbackBucket.md" target="_blank">this example</a> for the effect discretization parameters. 


# Value

A list of values with length = number of plant.

Each value describes the availability of below-ground resources for a plant (dimensionless).
The factor ranges from 0 to 1, with 1 indicating no limitations and 0 indicating full limitations.


# Details
## Purpose

The purpose of this module is to simulate the feedback between pore water salinity and plant water uptake.
When a plant takes up (fresh) water, the salinity remains in the soil, thus salinizing the soil.
This in turn makes it more difficult for the plant to take up water (i.e. reduces water availability).

## Process overview

Initialize the module
- *makeGrid*: create regular grid (see ``pyMANGA.ResourceLib``)
- *getInflowSalinity*: calculate salinity in each cell
- *getInflowMixingRate*: calculate mixing rate in each cell
- *writeGridSalinity*: write cell salinity to file

During each time step:
- *prepareNextTimeStep*: technical method
- *addPlant*: add plants to the resource matrix
- *calculateBelowgroundResources*: calculate below-ground factor

## Sub-processes
#### getInflowSalinity

The salinity at the boundaries of the model is calculated as described in ``pyMANGA.BelowGround.Individual.FixedSalinity``.

The salinity in each cell is linearly interpolated.
If the model domain consists of only 1 cell, the average of the left and right boundaries is taken.

#### getInflowMixingRate

The mixing rate in each cell (`r_mix_inflow`) is linearly interpolated based on the mixing rate at the left and right boundaries (`r_mix`).

#### writeGridSalinity/readGridSalinity

The salinity of each cell is written to and read from a txt file at the end and beginning of each time step.
The file will be overwritten each time.

#### addPlant

Add plant attributes such as position, size, and growth parameters to the resource module.

*getAffectedCellsIdx* returns the indices of cells affected by a plant.
Affected cells are those that are within the centers of the root plate radius.

It is assumed that the water uptake (``plant_water_uptake``, in m³ per timestep) of a plant is uniformly distributed over all affected cells, defined by their area (`cell_area)` and number (`no_cells`).
Thus, the sink term (`sink_per_cell`, in m per s) of each cell is
````python
sink_per_cell = plant_water_uptake / (cell_area * no_cells) / timesteplength
````

#### calculateBelowgroundResources

- *getBorderValues* Calculate the salinity and mixing rate at the left and right domain boundaries based on ``pyMANGA.BelowGround.Individual.FixedSalinity``.
- *getInflowSalinity* Calculate the inflowing salinity in each cell using linear interpolation (see method *getInflowSalinity*).
- *readGridSalinity* Read salinity of each cell from previous time step.
- *calculateCellSalinity* Calculate the salinity of the current time step using a simple bucket model approach (see below).
- *getPlantSalinity* Calculate mean cell salinity of affected cells for each plant (``salinity_plant``)
- *calculatePlantResources* Calculate salinity below each plant based on ``pyMANGA.BelowGround.Individual.FixedSalinity``.

##### getBorderValues

Calculate salinity and mixing rate at left and right boundaries.

If a sine function is defined in the input file, it can be applied to both salinity and mixing rate, or separately. 
By default, it is applied to salinity only.
For the calculation see ``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``.

##### calculateCellSalinity

Salinity in each cell is calculated assuming a simple water bucket approach, where each cell is an independent bucket with the following characteristics:
- fully saturated
- outflow: water extraction through plant, with salinity = 0
- inflow: water inflow, with salinity = variable

````python
ht = exp(- r_mix_inflow / depth * timesteplength)
sal_cell = sal_cell * ht + (vol_sink_cell + r_mix_inflow) / r_mix_inflow * sal_cell_inflow * (1 - ht)
````

## Application & Restrictions

same as ``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``

# References

<a href="https://doi.org/" target="_blank">Link</a>,


# Author(s)

Marie-Christin Wimmler, Ronny Peters

# See Also

``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``

# Examples


