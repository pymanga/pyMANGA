# Description

Production module that defines the number of new seeds or seedlings based on the size of existing plants using a user-defined formula. Optionally, a size threshold can be applied, below which plants will not produce seeds.

# Usage

```xml
<type>SizeDependent</type>
<formula>0.6 + 0.01 * 200 * x</formula>
<x_geometry>r_stem</x_geometry>
<log>True</log>
<log-1>False</log-1>
<x_min>0.02</x_min>
```

# Attributes

- ``type`` (string): "SizeDependent". Defines the type of the production module.
- ``formula`` (string): Formula in the form `y~x`, where `y` is the number of new seeds/seedlings and `x` refers to the plant geometry (e.g., `r_stem`). The formula is applied to calculate the number of seeds or seedlings based on the size of the plant.
``x_geometry`` (string): Specifies the geometry of the plant referenced in the formula (e.g., ``r_stem`` for stem radius). pyMANGA units are typically in SI units, and the formula may need to be adjusted accordingly. The geometry can refer to various plant dimensions, such as stem radius or height, and is defined in the species-specific module (e.g., ``Avicennia.py``) where additional geometries may be available.
- ``log`` (bool): (optional) If set to `True`, the formula result will be log-transformed. Default: `False`.
- ``log-1`` (bool): (optional) If set to `True`, the formula result will be log-transformed with an adjustment of -1. Default: `False`.
- ``x_min`` (float): (optional) If set, only plants with `r_stem` greater than or equal to this threshold will produce new seeds/seedlings. Default: `None` (all plants can reproduce).

# Value

List of length = number of plants

# Details

## Purpose

Defines the number of new plants added to the model based on the size of existing plants.

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

If `x_min` is defined, only plants where the geometry specified by `x_geometry` (e.g., `r_stem` or other plant geometry types) is greater than or equal to `x_min` will contribute to reproduction.

**Note**: The number of new seeds can increase exponentially if no other process (e.g., competition or mortality) reduces reproduction.

## Application & Restrictions

- If `x_min` is set too high, no new seedlings may be produced, limiting population growth.
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
    <x_min>0.02</x_min>
</production>
```

