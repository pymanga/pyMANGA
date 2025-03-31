# Description

Sub-library containing seed or seedling production modules.

# Usage

Production is part of the definition of the population (see ``pyMANGA.PopulationLib``). 

```xml
<production>
    <type> ModuleName </type>
    <nth_timestep>12</nth_timestep>
</production>
```

# Attributes

- ``production`` (string): Nesting tag to define the production strategy of a group
- ``type`` (string): Name of the selected module
- ``nth_timestep`` (int): (optional) The time step in which production takes place, e.g. ``nth_timestep=2`` means that production takes place every second time step. Default: 1. 

# Value

integer or list of length number of plants

# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.PopulationLib.Production.FixedRate``

