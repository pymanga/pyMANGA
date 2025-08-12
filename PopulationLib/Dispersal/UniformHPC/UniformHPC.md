# Description

Dispersal module that defines the location of new plants.

New plants are randomly distributed in the model domain.
The boundaries of the area are specified by the model domain.

The size (geometry) and attributes of a plant are taken from the species file (see ``pyMANGA.PopulationLib.Species``).

# Usage

```xml
<dispersal>
    <type> Uniform </type>
</dispersal>
```

# Attributes

- ``type`` (string): "Uniform"

# Value

see ``pyMANGA.PopulationLib.Dispersal``

# Details
## Purpose

Define the location of new plants added to the model by randomly distributing them within the defined model domain.

## Process overview

#### getWeightedPositions

Location (xy) of new plants drawn from a uniform distribution within the specified boundaries.

#### Alternative Distributions

Currently, only a uniform distribution is implemented. Future extensions could include:
- **Normal Distribution**: Plants cluster around a central location.
- **Exponential Distribution**: Most plants are placed near a reference point, with some dispersed further away.

## Application & Restrictions

- Plants are only placed within the specified model domain.
- The module assumes that seed production per individual is handled separately (see ``pyMANGA.PopulationLib.Production``).
- Future implementations may allow more control over plant placement.

# References

-

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann

# See Also

``pyMANGA.PopulationLib.Dispersal``,
``pyMANGA.PopulationLib.Species``,
``pyMANGA.PopulationLib.Production``

