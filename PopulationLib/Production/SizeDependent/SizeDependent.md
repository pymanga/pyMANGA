# Description

Production module that defines the number of new seeds or seedlings based on the size of existing plants using a user-defined formula.

# Usage

```xml
<type>SizeDependent</type>
    <formula>0.3 + 0.01 * 200 * x</formula>
    <x_geometry>r_stem</x_geometry>
    <log>True</log>
    <per_ha>False</per_ha>
    <min_r_stem>0.02</min_r_stem>
```

# Attributes

- ``type`` (string): "SizeDependent"
- ``formula`` (string): Formula of the form y~x, where y represents the number of new seeds/seedlings and x refers to the plant geometry, see ``x_geometry``.
- ``x_geometry`` (string): The geometry of the plant referenced in the formula, e.g., 'r_stem'. Note that pyMANGA units are SI units, and the formula may need to be adjusted.
- ``log`` (bool): (optional) If True, ``formula`` needs to be log-transformed. Default: False.
- ``per_ha`` (bool): (optional) If True, the number of new plants is normalized per hectare. Default: False.
- ``min_r_stem`` (float): (optional) If set, only plants with ``r_stem`` greater than or equal to this threshold will produce new seeds/seedlings. Default: None (all plants can reproduce).

# Value

List of length = number of plants

# Details

## Purpose

Define the number of new plants added to the model.

## Process overview

### getNumberSeeds

Calculates the number of new plants produced by each of the already existing plants.

The number of new plants is calculated using the defined production function:
``no_per_plant = production_function(x, 0)``.

``x`` is the plant geometry used for the regression.
See ``pyMANGA.PlantModelLib`` for possible plant geometries.
**Note** the potential difference in units.

If this is a logarithmic function, the result is transformed using:
``no_per_plant = int(10 ** no_per_plant - 1)``.

If ``min_r_stem`` is defined, only plants where ``r_stem >= min_r_stem`` contribute to reproduction.

**Note** The number of new seeds can increase exponentially if no other process reduces reproduction, such as competition or mortality.

## Application & Restrictions

- If ``min_r_stem`` is set too high, no new seedlings may be produced, limiting population growth.
- The formula should be adjusted based on the units used in pyMANGA.

# References

-

# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.PopulationLib.Production``,
``pyMANGA.PopulationLib.Species``

# Examples

Each existing plant produces a size-dependent number of seedlings every 12th time step, calculated using the given formula and interpreted logarithmically. Only plants with ``r_stem`` greater than or equal to 0.02 will reproduce.

```xml
<production>
    <type> SizeDependent </type>
    <formula>0.71155 + 0.06346 * 200 * x - 0.00034290 * 200 * x**2</formula>
    <x_geometry>r_stem</x_geometry>
    <log>True</log>
    <nth_timestep>12</nth_timestep>
    <min_r_stem>0.02</min_r_stem>
</production>
```

