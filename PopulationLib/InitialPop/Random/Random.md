# Description

Population module that defines the location of initial and new plants.

New plants are randomly distributed in the model domain.
The number of plants is the same at each time step.
The size (geometry) and attributes of a plant are taken from the species file (see ``pyMANGA.PopulationLib.Species``).

# Usage

```xml
<initial_population>
    <type>Random</type>
    <n_individuals> 1 </n_individuals>
</initial_population>
```

# Attributes

- ``type`` (string): "Random"
- ``n_individuals`` (int): Number of plants recruited in the beginning of the simulation

# Value

see ``pyMANGA.PopulationLib.Dispersal``

# Details
## Purpose

Define the location and geometry of new plants added to the model.

## Process overview

- _getPlantAttributes_
- _getPositions_

## Sub-processes
### getPlantAttributes

- Create dictionary containing the plant positions.
- Create geometry array of length = number of plants. The area contains only 'False' to indicate that no initial geometry is provided.
- Create empty network dictionary.

### getPositions

Location (xy) of new plants is determined using ``pyMANGA.PopulationLib.Dispersal.Uniform``.



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

- Start the simulation with a population of 100 randomly distributed seedlings.

````xml
<initial_population>
    <type>Random</type>
    <n_individuals> 100 </n_individuals>
</initial_population>
````

