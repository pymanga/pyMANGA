# Description

Population module that defines the location of new plants.

New plants are randomly distributed in the model domain.
The number of plants is the same at each time step.
The size (geometry) and attributes of a plant are taken from the species file (see ``pyMANGA.PopulationLib.Species``).

# Usage

```xml
<production>
    <type> Random </type>
    <n_individuals> 10000 </n_individuals>
    <per_individual> False </per_individual>
    <per_ha> True </per_ha>
</production>
```

# Attributes

- ``type`` (string): "Random"
- ``n_individuals`` (int): Number of plants recruited in the beginning of the simulation
- ``per_individual`` (bool): optional - If True, the number of individuals refers to new individuals per existing individual of the group. Default: False.
- ``per_ha`` (bool): optional - If True, the number of individuals refers to new individuals per hectare. Default: False.

# Value

integer or list of length number of plants

# Details
## Purpose

Define the location of new plants added to the model.

## Process overview
### getNumberSeeds

Return the number of seeds or seedling produced per time step.
If <per_individual> is true, this is:

``[n_individuals] * no_plants``

If <per_individual> is true, this is:

``
domain_ha * n_individuals
`` 

with ``domain_ha = (l_x * l_y) / 10000``,
where ``l_x, l_y`` is the xy-extension of the model domain.

## Application & Restrictions

-

# References

-

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann


# See Also

``pyMANGA.PopulationLib.Dispersal``,
``pyMANGA.PopulationLib.Species``

# Examples

````xml
<production>
    <type> Random </type>
    <n_individuals> 10000 </n_individuals>
    <per_individual> False </per_individual>
    <per_ha> True </per_ha>
</production>
````

