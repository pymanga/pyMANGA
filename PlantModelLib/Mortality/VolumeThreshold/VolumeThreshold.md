# Description

This module determines whether a plant is dying or not based on the individual plant's geometry. 
If (i) the current biovolume falls below the initial biovolume, or (ii) the aboveground radius becomes smaller than the initial aboveground radius, or (iii) the belowground radius becomes smaller than the initial belowground radius, the plant dies.

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

- ``type`` (string): "Random" (no other values accepted)

# Value

A bool.

If True, the plant survives, if False the plant dies.


# Details
## Purpose

Plant mortality depends on relative growth over a defined period.
Growth is based on the growth variable of the selected plant module.

If (i) the current biovolume falls below the initial biovolume, or (ii) the aboveground radius becomes smaller than the initial aboveground radius, or (iii) the belowground radius becomes smaller than the initial belowground radius, the plant dies.


## Process overview

- Greater than comparison for
  - r_ag
  - r_bg
  - V_tot
```
r_ag > r_ag_ini
r_bg > r_bg_ini
V_total > V_total_ini
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
        <species> Avicennia </species>
        <vegetation_model_type> Saltmarsh </vegetation_model_type>
        <mortality> Memory </mortality>
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
