# Description

# Usage

```xml

```

# Attributes

- ``type`` (string): "..."

# Value

# Details
## Purpose

The purpose of this module is to simulate the feedback between pore water salinity and plant water uptake.
When a plant takes up (fresh) water, the salinity remains in the soil, thus salinizing the soil.
This in turn makes it more difficult for the plant to take up water (i.e. reduces water availability).

## Process overview

Initialize the module
- *expandGrid*: create regular grid
- *getInflowSalinity*: calculate cell salinity
- *writeGridSalinity*: write cell salinity to file

During each time step:
- *prepareNextTimeStep*: technical method
- *addPlant*: add plants to the resource matrix
- *calculateBelowgroundResources*: calculate below-ground factor

## Sub-processes
#### expandGrid

Create a regular grid of size x*y where
```python
x = x_2 - x_1
y = y_2 - y_1
```
and cell size of
````python
xs = x_2 / x_resolution
ys = y_2 / y_resolution
````

The volume of each cell is calculated as
````python
vol_cell = xs * ys * cell_height
````
where the height of each cell (``cell_height``) is 1 m.

#### getInflowSalinity

The salinity at the boundaries of the model is calculated as described in ``pyMANGA.BelowGround.Individual.FixedSalinity``.

The salinity in each cell is linearly interpolated.
If the model domain consists of only 1 cell, the average of the left and right boundaries is taken.

#### writeGridSalinity/readGridSalinity

The salinity of each cell is written to and read from a txt file at the end and beginning of each time step.
The file will be overwritten each time.

#### prepareNextTimeStep

Calculate the water volume in each cell (``vol_water_cell`` in m³):
````python
vol_water_cell = vol_cell * q_cell / 3600 / 24 * timesteplength 
````
where ``vol_cell`` is the total volume of a cell and ``q_cell`` the daily flow through each cell (user input).

#### addPlant

Add plant attributes such as position, size, and growth parameters to the resource module.

*getAffectedCellsIdx* returns the indices of cells affected by a plant.
Affected cells are those that are within the centers of the root plate radius.

It is assumed that the water uptake (``plant_water_uptake``) of a plant is uniformly distributed over all affected cells.
Thus, the sink term of each cell is
````python
sink_per_cell = plant_water_uptake / no_cells
````

#### calculateBelowgroundResources

- *getBorderSalinity* Calculate the salinity at the left and right domain boundaries based on ``pyMANGA.BelowGround.Individual.FixedSalinity``.
- *getInflowSalinity* Calculate the inflowing salinity in each cell using linear interpolation (see method *getInflowSalinity*).
- *readGridSalinity* Read salinity of each cell from previous time step.
- *calculateCellSalinity* Calculate the salinity of the current time step using a simple bucket model approach (see below).
- *getPlantSalinity* Calculate mean cell salinity of affected cells for each plant (``salinity_plant``)
- *calculatePlantResources* Calculate salinity below each plant based on ``pyMANGA.BelowGround.Individual.FixedSalinity``.

##### calculateCellSalinity

Salinity in each cell is calculated assuming a simple water bucket approach, where each cell is an independent bucket with the following characteristics:
- fully saturated
- outflow: water extraction through plant, with salinity = 0
- inflow: water inflow, with salinity = variable

The salinity of each cell is calculated as follows:
- Before uptake: mass of salt in cell ``m_cell = sal_cell * vol_water_cell``
- After uptake: 
  - cell water volume ``vol_cell_remain = vol_water_cell - vol_sink_cell``
  - salt content ``sal_cell_new = m_cell / vol_cell_remain``
- Mixing of cell water and inflowing water
  - volume of exchanged water ``f_mix * vol_water_cell``
  - mass of salt of exchanged water ``m_out = sal_cell_inflow * vol_out``
  - volume of remaining water ``vol_water_cell - vol_out``
  - mass of salt of exchanged water ``m_remain = sal_cell_new * v_remain``
  - total mass of salt ``m_cell = m_remain + m_out``
  - new cell salinity ``m_cell / vol_water_cell``
- Assign the new salinity as ``sal_cell`` and write it to txt file (*writeGridSalinity*)

## Application & Restrictions


# References

<a href="https://doi.org/" target="_blank">Link</a>,


# Author(s)


# See Also

# Examples


