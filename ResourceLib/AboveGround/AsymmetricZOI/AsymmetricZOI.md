# Description

This module calculates the reduction in above-ground resource availability caused by the competition for light between neighboring plants.
The calculation is based on the overlap of above-ground biomass, using the asymmetric zone-of-influence (ZOI) concept.
The description of above-ground biomass depends on the abstraction of the plant geometry in chosen plant growth model.
For example, in `pyMANGA.PlantModelLib.Bettina`, this is the canopy of a tree with the shape of a hemisphere.

This concepts assumes that a plant without neighbors gets 100% of the available light.
There is no temporal variation in light availability.

# Usage

```xml

<aboveground>
    <type>AsymmetricZOI</type>
    <domain>
        <x_1>0</x_1>
        <y_1>0</y_1>
        <x_2>20</x_2>
        <y_2>20</y_2>
        <x_resolution>80</x_resolution>
        <y_resolution>80</y_resolution>
    </domain>
</aboveground>
```

# Attributes

- ``type`` (string): "AsymmetricZOI" (no other values accepted)
- ``domain`` (nesting-tag): coordinates to define the model domain (as mesh)
    - ``x_1`` (float): x-coordinate of left bottom border of grid
    - ``x_2`` (float): x-coordinate of right bottom border of grid
    - ``y_1`` (float): y-coordinate of left top border of grid
    - ``y_2`` (float): y-coordinate of right top border of grid
    - ``x_resolution`` (float): x-resolution of the grid
    - ``y_resolution`` (float): y-resolution of the grid
- ``allow_interpolation`` (bool): (optional) If True, the ZOI of a plant can be smaller than a grid cell, and it will be
  assigned to the nearest node. Default: False.

# Value

A list of values with length = number of plant.

Each value describes the availability of above-ground resources for a plant (dimensionless).
The factor ranges from 0 to 1, with 1 indicating no limitations and 0 indicating full limitations.

# Details

## Purpose

This module describes light competition between plants and quantifies its strength by means of a factor between 0 and 1.
It follows the asymmetric zone of influence (ZOI) concept introduced
by (<a href="https://doi.org/10.1086/321988" target="_blank">Weiner et al., 2001</a>). Because light does not reach all
canopies equally, this resource is shared unevenly between plants. That is, a tall plant with a large canopy intercepts
more light than a neighboring plant that it shades.
In this model the ZOI is defined by the crown radius of a plant.

The implementation in pyMANGA is based on BETTINA model (<a href="https://doi.org/10.1016/j.ecolmodel.2014.04.001" target="_blank">Peters et al., 2014</a>).

In the following description, the above-ground part of the plant is called crown.

## Process overview

This module calls the following sub-procedures:

- *makeGrid*: create a grid regular 2D grid (set variables: my_grid, mesh_size)
- *addPlant*: add relevant plant variables to the resource module
- *calculateAbovegroundResources*: calculate above-ground resource factor
  - Set resource variable ag_factor

## Sub-processes
### Model grid (makeGrid)

- Create a regular 2D grid (set variables: my_grid, mesh_size)
- This is called only once, during initialization.
- 
### Add plants (addPlant)

- Add xy-positions and crown radii (``r_ag``) and plant height (``h_stem``) of all plants in the model
- Check whether the crown radius of a plant cover a grid node (junction of cells)
```
r_ag > mesh_size * 0.5**0.5
```
  - If interpolation is not allowed (``allow_interpolation`` = FALSE) the model stops
  - If interpolation is allowed and the condition above is not met, ``r_crown`` is set to ``mesh_size`` for the following calculations

### Above-ground factor (calculateAbovegroundResources)

- Calculate the distance of plants to each node (``dist``)
- Get index of nodes that are occupied by the plant (``idx``)	
- Calculate the height of each plant (i) on a node (``idx``) assuming a spherical shape of the canopy	
````
height_idx = stem_height + (4 * crown_radius**2 - dist_idx**2)**0.5
````

- Count the number of nodes occupied by a plant (``crown_areas``) 
- Count the number of nodes where a tree is the highest (``highest_plant``) 
- Calculate the above-ground resource factor (``ag_factor``) 
````
ag_factor = wins \ crown_areas
````


## Application & Restrictions

**Application**

- This module can be used with plant growth modules where plants have a description of the crown such as `pyMANGA.PlantModelLib.Bettina`.

**Restrictions**

- There are no restrictions on the input parameters. 
- However, very high course meshes may result in inaccuracies.

# References

<a href="https://doi.org/10.1086/321988" target="_blank">Weiner et al., 2001</a>  
<a href="https://doi.org/10.1016/j.ecolmodel.2014.04.001" target="_blank">Peters et al., 2014</a>


# Author(s)

Jasper Bathmann, Ronny Peters, Marie-Christin Wimmler

# See Also


`pyMANGA.ResourceLib.AboveGround`, `pyMANGA.PlantModelLib.Bettina`


# Examples

- Define the grid on which to calculate above-ground resource availability.
- The total size is 20x20 m, and a cell is 0.25 x 0.25 m (20 m / 80 cells = 0.25 m/cell).
- Since interpolation is allowed, the canopy can be within a cell without "touching" a node, i.e. with a radius less than 0.177 m. 

```xml

<aboveground>
    <type>AsymmetricZOI</type>
    <domain>
        <x_1>0</x_1>
        <y_1>0</y_1>
        <x_2>20</x_2>
        <y_2>20</y_2>
        <x_resolution>80</x_resolution>
        <y_resolution>80</y_resolution>
    </domain>
    <allow_interpolation>True</allow_interpolation>
</aboveground>
```
