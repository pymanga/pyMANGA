# Description

This module calculates the reduction in below-ground resource availability caused by the competition for below-ground resources, e.g., water, between neighboring plants.
The calculation is based on the overlap of below-ground biomass, using the symmetric zone-of-influence (ZOI) concept.
The description of below-ground biomass depends on the abstraction of the plant geometry in chosen plant growth model.
For example, in `pyMANGA.PlantModelLib.Bettina`, this is radius of the root plate.

This concepts assumes that a plant without neighbors gets 100% of the available resource.
There is no temporal variation in resource availability.

# Usage

```xml

<belowground>
    <type>SymmetricZOI</type>
    <domain>
        <x_1>0</x_1>
        <y_1>0</y_1>
        <x_2>20</x_2>
        <y_2>20</y_2>
        <x_resolution>80</x_resolution>
        <y_resolution>80</y_resolution>
    </domain>
</belowground>
```

# Attributes

- ``type`` (string): "SymmetricZOI" (no other values accepted)
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

Each value describes the availability of below-ground resources for a plant (dimensionless).
The factor ranges from 0 to 1, with 1 indicating no limitations and 0 indicating full limitations.

# Details

## Purpose

This module describes competition between plants and quantifies its strength by means of a factor between 0 and 1.
It follows the symmetric zone of influence (ZOI) concept introduced
by (<a href="https://doi.org/10.1086/321988" target="_blank">Weiner et al., 2001</a>). 
The resource is shared evenly between plants. 

In this model the ZOI is defined by the radius of the below-ground part of a plant.

The implementation in pyMANGA is based on BETTINA model (<a href="https://doi.org/10.1016/j.ecolmodel.2014.04.001" target="_blank">Peters et al., 2014</a>).

In the following description, the below-ground part of the plant is called root.

## Process overview

This module calls the following sub-procedures:

- *makeGrid*: create a grid regular 2D grid (set variables: my_grid, mesh_size)
- *addPlant*: add relevant plant variables to the resource module
- *calculateBelowgroundResources*: calculate below-ground resource factor
  - Set resource variable bg_factor

## Sub-processes
### Model grid (makeGrid)

- Create a regular 2D grid (set variables: my_grid, mesh_size)
- This is called only once, during initialization.
- 
### Add plants (addPlant)

- Add xy-positions and root radii (``r_bg``) of all plants in the model
- Check whether the root radius of a plant covers a grid node (junction of cells)
```
r_bg > mesh_size * 0.5**0.5
```
  - If interpolation is not allowed (``allow_interpolation`` = FALSE) the model stops
  - If interpolation is allowed and the condition above is not met, ``r_bg`` is set to ``mesh_size`` for the following calculations

### Below-ground factor (calculateBelowgroundResources)

- Calculate the distance of plants to each node (``dist``)
- Get index of nodes that are occupied by the plant (``idx``)	
- Count the number of nodes occupied by a plant (``plant_counts``) 
- Calculate the above-ground resource factor (``bg_factor``) 
````
bg_factor = plant_wins / plant_counts
````

## Application & Restrictions

**Application**

- This module can be used with plant growth modules where plants have a description of the root such as `pyMANGA.PlantModelLib.Bettina`.

**Restrictions**

- There are no restrictions on the input parameters. 
- However, very high course meshes may result in inaccuracies.

# References

<a href="https://doi.org/10.1086/321988" target="_blank">Weiner et al., 2001</a>  
<a href="https://doi.org/10.1016/j.ecolmodel.2014.04.001" target="_blank">Peters et al., 2014</a>


# Author(s)

Jasper Bathmann, Ronny Peters, Marie-Christin Wimmler

# See Also


`pyMANGA.ResourceLib.BelowGround`, `pyMANGA.PlantModelLib.Bettina`


# Examples

- Symmetric ZOI on a 22x22m² mesh with 1m² cell size.
- Interpolation is allowed.
```xml
<belowground>
    <type> SymmetricZOI </type>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 22 </x_resolution>
        <y_resolution> 22 </y_resolution>
        <allow_interpolation> True </allow_interpolation>
    </domain>
</belowground>
```

- Symmetric ZOI on a 22x22m² mesh with 0.25x0.25m² cell size.
- Interpolation is allowed.
- Additionally, resource limitation through salinity is considered (see `pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity`).
```xml
<belowground>
    <type> Merge </type>
    <modules> SymmetricZOI FixedSalinity </modules>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 88 </x_resolution>
        <y_resolution> 88 </y_resolution>
    </domain>
    <salinity> 0.025 0.035 </salinity>
    <min_x>0</min_x>
    <max_x>22</max_x>
</belowground>
```


