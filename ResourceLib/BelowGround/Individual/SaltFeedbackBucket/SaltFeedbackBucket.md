# Description

This module calculates the change in pore water salinity of each cell as a result of two processes: 
(i) uptake of fresh water by individual plants within their root zone and (ii) mixing of cell water and tidal water. 
Each cell is considered as a simple 1D bucket with no additional vertical or horizontal fluxes and the base salinity is based on ``pyMANGA.BelowGround.Individual.FixedSalinity``.
Local soil salinity determines the availability of water to individual plants: the higher the salinity, the less water is available to a plant. 
Therefore, a plant's water uptake can change its own water availability and that of surrounding plants.

**Water uptake**
When a plant absorbs water from the soil, we assume that the absorbed water does not contain salt, which instead remains in the pore space of the soil. 
This increases the local salt concentration in those cells that are within the root zone of a plant, resulting in reduced resource availability.

**Tidal mixing**
In addition, the salinity concentration in a cell is determined by the inflowing water (representing tidal water). 
The amount of mixing depends on the salinity of the tidal water and a defined mixing rate (i.e. the amount of water exchanged).  
The tidal water concentration and mixing rate are linearly interpolated between the left and right model boundaries.

**Spatial and temporal interpolation**
The spatial and temporal interpolation of tidal salinity and the mixing rate is described in more detail in ``pyMANGA.BelowGround.Individual.FixedSalinity``.
Spatial interpolation is linear between the left and right model boundaries.
Temporal interpolation can follow a sine function or be based on an input file.
The temporal resolution depends on the selected time step length. 
For example, it can represent daily tides or seasonal variations.

# Usage

*The values shown here are examples. See Attributes for more information.*

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
    <save_file> path/to/grid_salinity </save_file>
    <save_salinity_ts> 120 </save_salinity_ts>
    <initial_salinity_file> path/so/salinity.txt </initial_salinity_file>
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
- ``r_mix`` (float or float float): one or two values defining the mixing rate (m per second) at ``x_1`` and ``x_2``. Values are linearly interpolated between ``x_1`` and ``x_2``. If only one value is given, the rate at ``x_1`` and ``x_2`` is equal .
- ``depth`` (float): Cell depth (m, corresponding to theoretical aquifer thickness). Default: 1 m.
- ``sine`` (nesting-tag): (optional) temporal interpolation based on a sine function. See notes for details.
  - ``medium`` (string): (optional) medium to which the sinusoidal option is applied. Possible values: "salt", "water" or "salt water" to apply the interpolation method to the tidal salinity concentration, mixing rate or both, respectively. Default: "salt"
  - ``amplitude`` (float): (optional) amplitude of the sine function. Default: 0
  - ``stretch`` (float): (optional) stretch of the sine function, i.e., length of a full period. Default: 24\*3600\*58 (approx. 1 year)
  - ``offset`` (float): (optional) offset of the sine function (along the time axis). Default: 0
  - ``noise`` (float): (optional) standard deviation to pick salinity value from sine function. Default: 0
- ``save_file`` (str): (optional) file name or path of cell salinity file (without file format). If no path is defined, the file is saved in the root directory.
- ``save_salinity_ts`` (int): (optional) number indicating at which nth timestep the salinity in each cell is written to a text file. Default: 1.
- ``initial_salinity_file`` (str): (optional) path to text file containing initial cell salinity.

See <a href="https://github.com/pymanga/sensitivity/blob/main/ResourceLib/BelowGround/Individual/SaltFeedbackBucket/SaltFeedbackBucket.md" target="_blank">this example</a> for the effect discretization parameters. 


# Value

A list of values with length = number of plants.

Each value describes the availability of below-ground resources for each plant in the list (dimensionless).
The factor ranges from 0 to 1, with 1 indicating no limitations and 0 indicating full limitations.


# Details
## Purpose

The purpose of this module is to simulate the feedback between pore water salinity and plant water uptake.
When a plant takes up (fresh) water, the salt remains in the soil, thus salinizing the soil.
This in turn makes it more difficult for the plant to take up water in the next timestep (i.e. reduces water availability).

## Process overview

Initialize the module
- *makeGrid*: create regular grid (see ``pyMANGA.ResourceLib``)
- *getBorderValues*: Calculate the salinity and mixing rate at the left and right domain boundaries based on ``pyMANGA.BelowGround.Individual.FixedSalinity``.
- *getInflowSalinity*: calculate salinity in each cell
- *getInflowMixingRate*: calculate mixing rate in each cell
- *assignInitialCellSalinity*: get initial cell salinity

During each time step:
- *prepareNextTimeStep*: technical method
- *addPlant*: add plants to the resource matrix
- *calculateBelowgroundResources*: calculate below-ground factor

## Sub-processes
#### getInflowSalinity

The salinity at the boundaries of the model is calculated as described in ``pyMANGA.BelowGround.Individual.FixedSalinity`` (temporal interpolation).

The salinity in each cell is linearly interpolated (spatial interpolation).
If the model domain consists of only 1 cell, the average of the left and right boundaries is taken.

Both salinity

#### getInflowMixingRate

The mixing rate in each cell (`r_mix_inflow`) is linearly interpolated based on the mixing rate at the left and right boundaries (`r_mix`).

#### assignInitialCellSalinity

If an initial cell salinity is provided as a text file, the file is read and the salinity (in kg per kg) is assigned.
The file needs to contain the salinity matrix of shape (row: y_resolution, col: x_resolution).
If this is not the case, salinity is calculated with *getInflowSalinity*.

#### addPlant

Add plant attributes such as position, size, and growth parameters to the resource module.

The cells affected by each plant are determined based on the root plate radius (*getAffectedCellsIdx*).
It is assumed that the water uptake (``plant_water_uptake``, in m³ per timestep) of a plant is uniformly distributed over all affected cells, defined by their area (`cell_area)` and number (`no_cells`).
Thus, the sink term (`sink_per_cell`, in m per s), i.e., the amount of water removed from each cell, is
````python
sink_per_cell = plant_water_uptake / (cell_area * no_cells) / timesteplength
````

#### calculateBelowgroundResources

This function calculates the below-ground resource factor for each plant using the following functions.

- *getBorderValues*: Calculate the salinity and mixing rate at the left and right domain boundaries based on ``pyMANGA.BelowGround.Individual.FixedSalinity``.
- *getInflowSalinity*: Calculate the inflowing salinity in each cell using linear interpolation (see method *getInflowSalinity*).
- *calculateCellSalinity*: Calculate the salinity of the current time step using a simple bucket model approach (see below).
- *getPlantSalinity*: Calculate the average cell salinity of affected cells, i.e., cells that are within the root plate radius, for each plant (``salinity_plant``)
- *calculatePlantResources*: Calculate salinity below each plant based on ``pyMANGA.BelowGround.Individual.FixedSalinity``.
- *writeGridSalinity*: Write grid cell salinity to a text file.

##### getBorderValues

Calculate salinity and mixing rate at left and right boundaries (i.e., temporal interpolation).

If a sine function is defined in the input file, it can be applied to both salinity and mixing rate, or separately. 
By default, it is applied to salinity only.
For the calculation see ``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``.

##### calculateCellSalinity

Salinity in each cell is calculated assuming a simple water bucket approach, where each cell is an independent bucket with the following characteristics:
- fully saturated
- outflow: water extraction through plant, with salinity = 0
- inflow: water inflow with defined mixing rate and salinity = variable

````python
ht = exp(- r_mix_inflow / depth * timesteplength)
sal_cell = sal_cell * ht + (vol_sink_cell + r_mix_inflow) / r_mix_inflow * sal_cell_inflow * (1 - ht)
````

#### writeGridSalinity

The salinity of each cell is written to a txt file at the end of a time step, if defined in the project file.
The file contains the salinity matrix of shape (row: y_resolution, col: x_resolution) 

## Application & Restrictions

same as ``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``

# References

-

# Author(s)

Marie-Christin Wimmler, Ronny Peters

# See Also

``pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity``

# Examples

A 20x5 m transect with regular grid cells (0.25x0.25 m², depth 1 m) has a base salinity of 35 ppt at it's left and right boundaries.
The mixing rate is 0.01 m per day and 0.015 m per day at the left and right boundaries, respectively.
In addition, the mixing rate follows an annual sinusoidal cycle with an amplitude of 0.001 m per day.
The salinity of each cell is saved to a text file every 10th time step.

```xml
<belowground>
    <type> SaltFeedbackBucket </type>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 20 </x_2>
        <y_2> 5 </y_2>
        <x_resolution> 100 </x_resolution>
        <y_resolution> 20 </y_resolution>
    </domain>
    <salinity> 0.035 0.035 </salinity>
    <r_mix> 0.01/3600/24 0.015/3600/24 </r_mix>
    <depth> 1 </depth>
    <sine>
        <medium> water </medium>
        <amplitude> 0.01/3600/24/10 </amplitude>
    </sine>
    <save_file> path/to/grid_salinity </save_file>
    <save_salinity_ts> 10 </save_salinity_ts>
</belowground>
```
