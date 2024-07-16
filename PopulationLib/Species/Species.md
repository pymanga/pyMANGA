# Description

Sub-library containing species files.

The variables that need to be defined in the species file depend on the modules chosen, e.g. for plant growth.

# Usage

```xml
<species> Rhizophora </species>
```

# Attributes

- ``species`` (string): either the name of an implemented species or the path to the species file

# Value

A class that contains species parameters.

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann, Ronny Peters

# See Also

``pyMANGA.PopulationLib``, 
``pyMANGA.PlantModelLib``, ``pyMANGA.PlantModelLib.Bettina``,
``pyMANGA.PlantModelLib.Mortality``, 
``pyMANGA.PopulationLib.Dispersal``


# Examples

- Use an implemented species file, i.e., Rhizophora (see ``pyMANGA.PopulationLib.Species.Rhizophora``)

```xml
<species> Rhizophora </species>
```

- Use a user-specific species file

```xml
<species> path/to/species/file.py </species>
```