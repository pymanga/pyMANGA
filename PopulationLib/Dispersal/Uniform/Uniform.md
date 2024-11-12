# Description

Dispersal module that defines the location of initial and new plants.

New plants are randomly distributed in the model domain.

The size (geometry) and attributes of a plant are taken from the species file (see ``pyMANGA.PopulationLib.Species``).

# Usage

```xml
<distribution>
    <type> Random </type>
    <n_individuals> 10 </n_individuals>
</distribution>
```

# Attributes

- ``type`` (string): "Random"
- ``n_individuals`` (int): Number of plants recruited in the beginning of the simulation

# Value

see ``pyMANGA.PopulationLib.Dispersal``

# Details
## Purpose

Define the location of new plants added to the model.

## Process overview
#### getWeightedPositions

Location (xy) of new plants drawn from a uniform distribution.

## Application & Restrictions

-

# References

-

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann


# See Also

``pyMANGA.PopulationLib.Dispersal``,
``pyMANGA.PopulationLib.Species``
