# Description

Population module that defines the position and size of the initial plant population.

Initial plant population is defined in a csv-file (coma-separated).
This file needs to contain the x,y-position of each individual (i.e., plant unit) and their geometry (i.e., size).
The parameters describing a plant's geometry depend on the chosen plant module (`pyMANGA.PlantModelLib`).

```xml
<distribution>
    <type> Random </type>
    <filename> 10 </filename>
</distribution>
```

# Attributes

- ``type`` (string): "Random"
- ``filename`` (string): Path to input file (csv) containing position and geometry of initial populaiton

# Value

see ``pyMANGA.PopulationLib.Dispersal``

# Details
## Purpose

## Process overview

## Sub-processes

## Application & Restrictions


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
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
    </domain>
    <n_recruitment_per_step> 0 </n_recruitment_per_step>
    <filename> Benchmarks/ModuleBenchmarks/PlantModules/Bettina/ag_initial_population.csv </filename>
</distribution>
````

- input initial population (csv) suitable for `pyMANGA.PlantModelLib.Bettina`
````csv    
plant,x,y,r_stem,h_stem,r_crown,r_root
Initial_000000001,10,11,0.0578281884412867,4.51153085664295,1.50012328699222,0.926942149712091
Initial_000000002,12,11,0.0123232096587272,1.9776990151532,0.499186547499313,0.308854210975212
````
