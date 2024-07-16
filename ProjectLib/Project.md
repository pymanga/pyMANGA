# Description

Library for pyMANGA project management.

A pyMANGA simulation is defined in a project file.
Some modules contain stochasticity (see e.g., ``pyMANGA.PopulationLib.Dispersal``).
A start value to initialize the random generator can be defined to reproduce simulations.

# Usage

```xml
<MangaProject>
    <random_seed>643879</random_seed>
</MangaProject>
```

# Attributes

- ``random_seed`` (int): (optional) start value of random number generator