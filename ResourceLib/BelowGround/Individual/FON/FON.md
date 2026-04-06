# Description

This module calculates the reduction in resource availability caused by the competition for resources between neighboring plants.
The calculation is based on the Field of Neighbourhood (FON) concept, where each plant generates an exponentially decaying field on a spatial grid.
Competition is quantified by the overlap of FON fields.

This concept assumes that a plant without neighbors gets 100% of the available resource.
There is no temporal variation in resource availability.

# C++ Backend

This module supports an optional C++ backend for accelerated computation. See `pyMANGA.ResourceLib` for compilation instructions and configuration details.

# Usage

```xml
<belowground>
    <type>FON</type>
    <domain>
        <x_1>0</x_1>
        <y_1>0</y_1>
        <x_2>22</x_2>
        <y_2>22</y_2>
        <x_resolution>88</x_resolution>
        <y_resolution>88</y_resolution>
    </domain>
</belowground>
```

# Attributes

- ``type`` (string): "FON" (no other values accepted)
- ``domain`` (nesting-tag): coordinates to define the model domain (as mesh)
    - ``x_1`` (float): x-coordinate of left bottom border of grid
    - ``x_2`` (float): x-coordinate of right bottom border of grid
    - ``y_1`` (float): y-coordinate of left top border of grid
    - ``y_2`` (float): y-coordinate of right top border of grid
    - ``x_resolution`` (float): x-resolution of the grid
    - ``y_resolution`` (float): y-resolution of the grid
- ``periodic_boundary`` (bool): (optional) If True, periodic boundary conditions are applied using
  the minimum image convention. Default: False.
- ``backend_type`` (string): (optional, case-insensitive) "cpp" for C++ accelerated backend, "python" for pure Python.
  If omitted, auto-selects C++ when available, otherwise falls back to Python.

# Value

A list of values with length = number of plant.

Each value describes the availability of below-ground resources for a plant (dimensionless).
The factor ranges from 0 to 1, with 1 indicating no limitations and 0 indicating full limitations.

# Details

## Purpose

This module describes competition between plants and quantifies its strength by means of a factor between 0 and 1.
It follows the Field of Neighbourhood (FON) concept introduced
by (<a href="https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger and Hildenbrandt, 2000</a>).
Each plant generates an exponentially decaying field on the grid, and competition is computed
from the overlap of these fields (Eq. 7 in Berger and Hildenbrandt, 2000).

The effect of FON parameters ``aa`` and ``bb`` is also discussed by
(<a href="https://doi.org/10.1023/A:1023965512755" target="_blank">Berger and Hildenbrandt, 2003</a>).

## Process overview

This module calls the following sub-procedures:

- *makeGrid*: create a regular 2D grid (set variables: my_grid, mesh_size)
- *addPlant*: add relevant plant variables to the resource module
- *calculateBelowgroundResources*: calculate below-ground resource factor
  - Set resource variable bg_factor

## Sub-processes
### Model grid (makeGrid)

- Create a regular 2D grid (set variables: my_grid, mesh_size)
- This is called only once, during initialization.

### Add plants (addPlant)

- Add xy-positions, stem radii (``r_stem``), and FON parameters (``aa``, ``bb``, ``fmin``, ``phi``) of all plants in the model
- FON parameters ``aa``, ``bb``, ``fmin`` and ``phi`` are defined in the species file.
- ``phi`` defaults to 2.0 if not specified in the species file (Eq. 7, Berger and Hildenbrandt, 2000).

### Below-ground factor (calculateBelowgroundResources)

- Compute the distance of each plant to each grid node. If periodic boundary conditions are enabled, the minimum image convention is applied.
- Compute the FON height of each plant at each grid node:
```
fon_radius = aa * r_stem^bb
cc = -log(fmin) / (fon_radius - r_stem)
height = exp(-cc * (distance - r_stem))
```
  Height is clamped to [0, 1] and set to 0 below ``fmin``.

- Compute the FON area (number of grid nodes with FON > 0) and FON impact (sum of competing plants' fields at each occupied node) for each plant.
- Calculate the below-ground resource factor:
```
stress_factor = fon_impact / fon_area
bg_factor = 1 - phi * stress_factor
```
  The factor is clamped to [0, 1].

### Periodic boundary conditions

When ``periodic_boundary`` is set to True, the model domain is treated as a torus:
plants near one edge can interact with plants near the opposite edge.
Distances are computed using the minimum image convention, i.e., the shortest
distance considering all periodic images of each plant.

This is useful for simulations that represent a small patch of a larger forest,
where edge effects would otherwise bias plants near the domain boundary.

## Application & Restrictions

**Application**

- This module can be used with plant growth modules where plants have a stem radius, such as `pyMANGA.PlantModelLib.Bettina`.
- If the effect of salinity on resource uptake should also be considered, use the below-ground module `pyMANGA.ResourceLib.BelowGround.Generic.Merge.Merge`.

**Restrictions**

- The mesh should be fine enough to resolve each plant's FON field. A warning is issued if any plant's FON radius (``aa`` * ``r_stem`` ^ ``bb``) is smaller than the mesh size.

# References

<a href="https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger and Hildenbrandt, 2000</a>
<a href="https://doi.org/10.1023/A:1023965512755" target="_blank">Berger and Hildenbrandt, 2003</a>
<a href="https://doi.org/10.1016/j.ecolmodel.2014.04.001" target="_blank">Peters et al., 2014</a>

# Author(s)

Jasper Bathmann, Ronny Peters, Marie-Christin Wimmler, Guanzhen Liu

# See Also

`pyMANGA.ResourceLib.BelowGround`, `pyMANGA.PlantModelLib.Bettina`

# Examples

- FON on a 22x22m² mesh with 0.25x0.25m² cell size.
```xml
<belowground>
    <type> FON </type>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 88 </x_resolution>
        <y_resolution> 88 </y_resolution>
    </domain>
</belowground>
```

- FON with periodic boundary conditions on a 22x22m² mesh.
```xml
<belowground>
    <type> FON </type>
    <periodic_boundary> True </periodic_boundary>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 88 </x_resolution>
        <y_resolution> 88 </y_resolution>
    </domain>
</belowground>
```

- FON with C++ backend on a 22x22m² mesh.
- The C++ backend requires compilation (see `CppBackend.md`). If the compiled module is not found, pyMANGA falls back to the pure Python implementation automatically.
```xml
<belowground>
    <type> FON </type>
    <backend_type> cpp </backend_type>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 88 </x_resolution>
        <y_resolution> 88 </y_resolution>
    </domain>
</belowground>
```

- FON with salinity effect (Merge module).
- Additionally, resource limitation through salinity is considered (see `pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity`).
```xml
<belowground>
    <type> Merge </type>
    <modules> FON FixedSalinity </modules>
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
