# Description

Sub-library containing seed or seedling recruitment (establishing) modules.

Recruitment (establishment) is optional.
Unless defined otherwise, all seedlings (plants) produced are established.

# Usage

Recruitment is part of the definition of the population (see ``pyMANGA.PopulationLib``). 

```xml
<recruitment>
    <type> ModuleName </type>
</recruitment>
```

# Attributes

- ``recruitment`` (string): Nesting tag to define the recruitment strategy of a group
- ``type`` (string): Name of the selected module

# Value

Dictionary containing the positions of plants.

# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.PopulationLib.Recruitment.Weighted``

