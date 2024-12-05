# Description

Population module that defines the location of initial and new plants.

New plants are randomly distributed in the model domain.
The number of plants is the same at each time step.
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
#### getWeightedPositions

Location (xy) of new plants drawn from a weighted uniform distribution.

The probability of each grid cell is calculated based on the weights initialized at the beginning of the simulation (see ``pyMANGA.PopulationLib.Dispersal``) with

``python
r = np.random.random(no_cells) ** (1 / weights)
``
The resulting vector (`r`) is sorted and the first n cells are selected, where n is the number of plants recruited in the current time step.
The location (xy) of the plants is randomly chosen with these grid cells.

#### getRandomPositions

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

# Examples

````xml
<distribution>
    <type> Random </type>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
    </domain>
    <n_individuals> 10 </n_individuals>
    <n_recruitment_per_step> 0 </n_recruitment_per_step>
</distribution>
````

