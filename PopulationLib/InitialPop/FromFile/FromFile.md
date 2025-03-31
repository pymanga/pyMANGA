# Description

Population module that defines the position and size of the initial plant population.

The initial plant population is defined in a CSV file (comma-separated). This file needs to contain the x,y-position of each individual (i.e., plant unit) and their geometry (i.e., size). The parameters describing a plant's geometry depend on the chosen plant module (pyMANGA.PlantModelLib).

```xml
<initial_population>
    <type> FromFile </type>
    <filename> Benchmarks/.../ag_initial_population.csv </filename>
</initial_population>
```

# Attributes

- ``type`` (string): "FromFile"
- ``filename`` (string): Path to input file (csv) containing position and geometry of initial population

# Value

see ``pyMANGA.PopulationLib.Dispersal``

# Details
## Purpose

The purpose of the ``FromFile`` module is to define the initial plant population by reading from a CSV file. 
The file contains position (x, y) and geometry (such as stem radius, height, and root radius) for each individual plant. 

## Process overview

**Initialization**

The module reads the input file specified in the filename attribute and processes the data.
It then retrieves the positions and geometries of plants.

**Geometry Validation**

The geometry parameters in the file are checked against expected parameters, ensuring that the data corresponds to the required model format.

**Data Extraction**

The positions (x, y) and geometries (e.g., stem and root dimensions) are extracted and returned as dictionaries.

## Sub-processes

- *getInputParameters*: Extracts input parameters (such as the type and filename) from the XML configuration.
- *getPlantsFromFile*: Reads the initial population data from the specified CSV file.
- *getInitialGroup*: Returns the positions and geometries of the initial plant population.
- *getGeometryList*: Provides the list of geometries accepted by the plant module.

## Application & Restrictions

- The input CSV file must contain the required fields for each plant (position and geometry). The geometrical parameters depend on the specific plant model used.
- The geometry parameters are checked against predefined lists for validity.
- If the geometry fields do not match, an error will be raised, and the process will halt.

# References

-

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann


# See Also

``pyMANGA.PopulationLib.Dispersal``,
``pyMANGA.PopulationLib.Species``


# Examples_

- project file (xml)
````xml
<distribution>
    <type> FromFile </type>
    <filename> Benchmarks/ModuleBenchmarks/PlantModules/Bettina/ag_initial_population.csv </filename>
</distribution>
````

- input initial population (csv) suitable for `pyMANGA.PlantModelLib.Bettina`
````csv    
plant,x,y,r_stem,h_stem,r_crown,r_root
Initial_000000001,10,11,0.0578281884412867,4.51153085664295,1.50012328699222,0.926942149712091
Initial_000000002,12,11,0.0123232096587272,1.9776990151532,0.499186547499313,0.308854210975212
````
