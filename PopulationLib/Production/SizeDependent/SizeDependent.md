# Description

Production module that defines the number of new seeds or seedlings based on the size of existing plants using a user defined formula.

# Usage

```xml
<type>SizeDependent</type>
    <formula>0.3 + 0.01 * 200 * x</formula>
    <x_geometry>r_stem</x_geometry>
    <log>True</log>
<per_ha>False</per_ha>
```

# Attributes

- ``type`` (string): "SizeDependent"
- ``formula`` (string): formula of the form y~x, with y the number of new seeds/seedlings and x referring to the plant geometry, see ``x_geometry``.
- ``x_geometry`` (string): The geometry of the plant x is referred to in the formula, e.g. 'r_stem'. Note that pyMANGA units are SI units and the formula may need to be adjusted.
- ``log`` (bool): (optional) If True, ``formula`` needs to be log-transformed. Default: False.

# Value

list of length = number of plants

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

If this is a logarithmic function the result is transformed using:
``no_per_plant = int(10 ** no_per_plant - 1)``

**Note** The number of new seeds can increase exponentially, if no other process reduces reproduction, such as competition or mortality.

## Application & Restrictions

-

# References

-

# Author(s)

Marie-Christin Wimmler


# See Also

``pyMANGA.PopulationLib.Production``,
``pyMANGA.PopulationLib.Species``

# Examples

Produce 1 new seedling per existing plant in every 12th time step.

````xml
<production>
    <type> FixedRate </type>
    <n_individuals> 1 </n_individuals>
    <per_individual> True </per_individual>
    <per_ha> False </per_ha>
    <nth_timestep>12</nth_timestep>
</production>
````

