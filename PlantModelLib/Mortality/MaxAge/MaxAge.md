# Description

This module determines whether a plant is dying or not based on the probability to reach maximum age (<a href="https://doi.org/10.2307/2258570" target="_blank">Botkin et al. 1972</a>).

<a href="https://doi.org/10.2307/2258570" target="_blank">Botkin et al. (1972)</a> proposed that only 2 % of saplings reach maximum age.
They also summarize maximum age values for common terrestrial trees, while values for the mangrove species *Avicennia germinans* and *Rhizophora mangle* can be found in <a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>.

This mortality concept is purely stochastic.

It is useful to combine ``MaxAge`` with ``NoGrowth`` or ``Memory``.

# Usage

Mortality is defined for each group of plants.
This example shows only the tags relevant to the mortality concept. 
See the Plant Growth (`pyMANGA.PlantModelLib`) and Population (`pyMANGA.PopulationLib`) modules for the other tags needed to define a group.

```xml
<population>
    <group>
        <mortality> MaxAge </mortality>
        <max_age> 100 </max_age>
        <p_max_age> 2/100 </p_max_age>
    </group>
</population>
```

# Attributes

- ``type`` (string): "Random" (no other values accepted)
- ``max_age`` (float): maximum plant age in years (default: 300)
- ``p_max_age`` (float): probability to reach maximum age (default: 0.02)

# Value

A bool.

If False, the plant survives, if False the plant dies.


# Details
## Purpose

The purpose of this module is to add age-dependent mortality to the plant population.

## Process overview

**Initialization**

- Calculate annual probability to die
````
p = 1 - p_max_age**(1/max_age)
````

**Within each timestep**

- Calculate the number of time steps per year (`steps_per_year`)
- Draw a random number from a uniform distribution (`r`)
- Check if plant survives with the following eq.
````
r * steps_per_year < p
````

## Application & Restrictions

-

# References

<a href="https://doi.org/10.2307/2258570" target="_blank">Botkin et al. (1972)</a> 

# Author(s)

Marie-Christin Wimmler

# See Also

`pyMANGA.PlantModelLib.Mortality.NoGrowth`, 
`pyMANGA.PlantModelLib.Mortality.RandomGrowth`,
`pyMANGA.PlantModelLib.Mortality.Memory`
`pyMANGA.PlantModelLib.Mortality.Random`


# Examples

- To see an example where multiple mortality modules are combined see `pyMANGA.PlantModelLib.Mortality.NoGrowth`.
