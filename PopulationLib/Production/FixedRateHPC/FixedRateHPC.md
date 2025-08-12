# Description

Production module that defines the number of new seeds or seedlings based on a fixed rate.
This rate can be related to the model domain, the number of existing individuals, or independent of both.


# Usage

```xml
<production>
    <type> FixedRate </type>
    <per_model_area> 10 </per_model_area>    
    <per_ha> 0 </per_ha>
    <per_individual> 1 </per_individual>
</production>
```

# Attributes

- ``type`` (string): "FixedRate"
- ``per_model_area`` (int): optional - Number of plants per model area. Default: None.
- ``per_ha`` (int): optional - Number of plants recruited per hectare. Default: None.
- ``per_individual`` (int): optional - Number of plants recruited per existing plant. Default: None.

# Value

dict with three items ("per_individual", "per_ha", "per_model_area")

# Details
## Purpose

Define the number of new plants added to the model.

## Process overview
### getNumberSeeds

Return the number of seeds or seedling produced per time step.
If <per_individual> has a value, this is:

``[per_individual] * no_plants``

**Note** The number of new seeds can increase exponentially, if no other process reduces reproduction, such as competition or mortality.

If <per_ha> has a value, this is:

``
domain_ha * per_ha
`` 

with ``domain_ha = (l_x * l_y) / 10000``,
where ``l_x, l_y`` is the xy-extension of the model domain.

If <per_model_area> has a value, this is:

``
per_model_areaa
`` 

## Application & Restrictions

- ``per_model_area`` and ``per_ha`` cannot be used simultaneously. But ``per_individual`` can be used with both.
- ``per_individual`` may be combined with ``pyMANGA.PopulationLib.Dispersal.Distance2Parent``, since otherwise all seedlings produced by a plant will be placed within the model domain if the parent tree is close to the boundary.

# References

-

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann


# See Also

``pyMANGA.PopulationLib.Dispersal``,
``pyMANGA.PopulationLib.Species``

# Examples

Produce 1 new seedling per existing plant and 100 seedlings per hectare in every 12th time step.

````xml
<production>
    <type> FixedRate </type>
    <per_individual> 1 </per_individual>
    <per_ha> 100 </per_ha>
    <nth_timestep>12</nth_timestep>
</production>
````

