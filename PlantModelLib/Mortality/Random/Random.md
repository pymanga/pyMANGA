# Description

This module determines whether a plant is dying or not based on the annual mortality probability. 
Values for the mangrove species *Avicennia germinans* and *Rhizophora mangle* can be found e.g. in <a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>.

In this concept, a plant does not die for mechanistic reasons. 
It is useful to combine ``Random`` with ``NoGrowth`` or ``Memory``.


# Usage

Mortality is defined for each group of plants.
This example shows only the tags relevant to the mortality concept. 
See the Plant Growth (`pyMANGA.PlantModelLib`) and Population (`pyMANGA.PopulationLib`) modules for the other tags needed to define a group.

```xml
<population>
    <group>
        <mortality>Random</mortality>
        <probability>0.0016</probability>
    </group>
</population>
```

# Attributes

- ``type`` (string): "Random" (no other values accepted)
- ``probability`` (float): (optional) annual mortality (default: 0.0016)

# Value

A bool.

If False, the plant survives, if False the plant dies.


# Details
## Purpose

The purpose of this module is to add random mortality to the plant population.

## Process overview

- Calculate the number of time steps per year (`steps_per_year`)
- Draw a random number from a uniform distribution (`r`)
- Check if plant survives with the following eq.
````
r * steps_per_year < probability
````

## Application & Restrictions

-

# References

<a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt, 2000</a>


# Author(s)

Marie-Christin Wimmler

# See Also

`pyMANGA.PlantModelLib.Mortality.NoGrowth`, 
`pyMANGA.PlantModelLib.Mortality.RandomGrowth`,
`pyMANGA.PlantModelLib.Mortality.Memory`


# Examples

- Below is a complete description of how to define a plant group in the project file.

````xml
<population>
    <group>
        <name> Initial </name>
        <species> Avicennia </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>Random</mortality>
        <probability>0.0016</probability>
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

- To see an example where multiple mortality modules are combined see `pyMANGA.PlantModelLib.Mortality.NoGrowth`.
