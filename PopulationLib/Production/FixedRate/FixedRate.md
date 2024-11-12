# Description

Production module that defines the number of new seeds or seedlings based on a fixed rate.
This rate can be related to the model domain, the number of existing individuals, or independent of both.


# Usage

```xml
<production>
    <type> FixedRate </type>
    <n_individuals> 10000 </n_individuals>
    <per_individual> False </per_individual>
    <per_ha> True </per_ha>
</production>
```

# Attributes

- ``type`` (string): "FixedRate"
- ``n_individuals`` (int): Number of plants recruited in the beginning of the simulation
- ``per_individual`` (bool): optional - If True, the number of individuals refers to new individuals per existing individual of the group. Default: False.
- ``per_ha`` (bool): optional - If True, the number of individuals refers to new individuals per hectare. Default: False.

# Value

integer or list of length number of plants

# Details
## Purpose

Define the number of new plants added to the model.

## Process overview
### getNumberSeeds

Return the number of seeds or seedling produced per time step.
If <per_individual> is true, this is:

``[n_individuals] * no_plants``

**Note** The number of new seeds can increase exponentially, if no other process reduces reproduction, such as competition or mortality.

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

