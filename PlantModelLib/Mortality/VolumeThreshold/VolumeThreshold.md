# Description

This module determines whether a plant is dying or not based on the individual plant's geometry. 
If (i) the current biovolume falls below a threshold biovolume, or (ii) the above-ground radius becomes smaller than the threshold above-ground radius, or (iii) the below-ground radius becomes smaller than the threshold below-ground radius, the plant dies.
All thresholds are species-specific and are defined within the relevant species file (see `pyMANGA.PopulationLib.Species.Saltmarsh`).

In this concept, plant mortality is intrinsic and is dependent on plant growth.
This mortality concept includes no stochasticity.


# Usage

Mortality is defined for each group of plants.
This example shows only the tags relevant to the mortality concept. 
See the Plant Growth (`pyMANGA.PlantModelLib`) and Population (`pyMANGA.PopulationLib`) modules for the other tags needed to define a group.

```xml
<population>
    <group>
        <mortality>VolumeThreshold</mortality>
    </group>
</population>
```

# Attributes

- ``type`` (string): "VolumeThreshold" (no other values accepted)

# Value

A bool.

If True, the plant survives, if False the plant dies.


# Details
## Purpose

If (i) the current biovolume falls below the threshold biovolume, or (ii) the above-ground radius becomes smaller than the threshold above-ground radius, or (iii) the below-ground radius becomes smaller than the threshold below-ground radius, the plant dies.


## Process overview

- Greater than comparison for
  - r_ag
  - r_bg
  - volume
```
r_ag > r_ag_thr
r_bg > r_bg_thr
V_total > V_total_thr
```


## Application & Restrictions

-

# References

-

# Author(s)

Jonas Vollhüter

# See Also

`pyMANGA.PlantModelLib.Mortality.Memory`, 
`pyMANGA.PlantModelLib.Mortality.Random`,


# Examples

````xml
<population>
    <group>
        <name> Initial </name>
        <vegetation_model_type> Saltmarsh </vegetation_model_type>
        <mortality> VolumeThreshold </mortality>
        <distribution>
            <type> FromFile </type>
            <domain>
                <x_1> 0 </x_1>
                <y_1> 0 </y_1>
                <x_2> 2 </x_2>
                <y_2> 2 </y_2>
            </domain>
            <n_recruitment_per_step> 0 </n_recruitment_per_step>
            <filename> Benchmarks/ModuleBenchmarks/PlantModules/Saltmarsh/initial_population.csv </filename>
        </distribution>
    </group>
</population>
````

- To see an example where multiple mortality modules are combined see `pyMANGA.PlantModelLib.Mortality.NoGrowth`.
