# Description

This module determines whether a plant is dying or not.
Plants die if growth is equal or below zero, i.e., the plant doesn't grow in a timestep.

In this concept, plant mortality is intrinsic and is dependent on plant growth.
This mortality concept represents mechanistic causes, e.g., a resource deficit, and did not include any stochasticity.


# Usage

Mortality is defined for each group of plants.
This example shows only the tags relevant to the mortality concept. 
See the Plant Growth (`pyMANGA.PlantModelLib`) and Population (`pyMANGA.PopulationLib`) modules for the other tags needed to define a group.

```xml
<population>
    <group>
        <mortality>NoGrowth</mortality>
    </group>
</population>
```

# Attributes

- ``type`` (string): "NoGrowth" (no other values accepted)

# Value

A bool.

If False, the plant survives, if False the plant dies.


# Details
## Purpose

-

## Process overview

-

## Application & Restrictions

- If there is no external disturbance of the system during a simulation, e.g. irregular fluctuation of resources, the plant will not die with this concept, because the growth will approach 0, but not fall below it.

# References

-


# Author(s)

Jasper Bathmann, Marie-Christin Wimmler

# See Also

`pyMANGA.PlantModelLib.Mortality.Random`, 
`pyMANGA.PlantModelLib.Mortality.RandomGrowth`,
`pyMANGA.PlantModelLib.Mortality.Memory`


# Examples

- Below is a complete description of how to define a plant group in the project file, assuming that plants die when growth stops.

````xml
<population>
    <group>
        <name> Initial </name>
        <species> Avicennia </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>NoGrowth</mortality>
        <distribution>
            <type> FromFile </type>
            <domain>
                <x_1> 0 </x_1>
                <y_1> 0 </y_1>
                <x_2> 22 </x_2>
                <y_2> 22 </y_2>
            </domain>
            <n_recruitment_per_step> 0 </n_recruitment_per_step>
            <filename> Benchmarks/ModuleBenchmarks/PlantModules/Bettina/bg_initial_population.csv </filename>
        </distribution>
    </group>
</population>
````

- In the following example mortality modules ``NoGrowth`` and ``Random`` are combined.
- In this case, the attributes of both concepts need to be defined.

````xml
<population>
    <group>
        <mortality>NoGrowth Random</mortality>
        <probability>0.0016</probability>
    </group>
</population>
````