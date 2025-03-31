# Description

Sub-library containing modules defining the initial plant population, i.e., the position and size of plants present at the beginning of the simulation.

# Usage

InitialPop is part of the definition of the population (see ``pyMANGA.PopulationLib``). 

```xml
<initial_population>
    <type> ModuleName </type>
</initial_population>
```

# Attributes

- ``initial_population`` (string): Nesting tag to define the initial population strategy of a group
- ``type`` (string): Name of the selected module

# Value

Dictionary containing the positions, size, and network parameters of plants.

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann

# See Also

``pyMANGA.PopulationLib.InitialPop.FromFile``,
``pyMANGA.PopulationLib.InitialPop.Random``,

