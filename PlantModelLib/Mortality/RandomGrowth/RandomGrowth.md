# Description

This module determines whether a plant is dying or not based on the individual plant growth. 
This means, the probability that a plant dies increases with growth reduction and thus, plant age.

The module requires a species-specific calibration parameter (`k_die`).
An analysis of the effect of this parameter on individual plant mortality can be found in <a href="https://github.com/pymanga/sensitivity/blob/main/PlantModels/Mortality/RandomGrowth/RandomGrowth.md" target="_blank">pyMANGA's sensitivity repository</a>.

In this concept, plant mortality is intrinsic and is dependent on plant growth.
This mortality concept includes stochasticity.

It is useful to combine ``RandomGrowth`` with ``NoGrowth`` or ``Memory``.


# Usage

Mortality is defined for each group of plants.
This example shows only the tags relevant to the mortality concept. 
See the Plant Growth (`pyMANGA.PlantModelLib`) and Population (`pyMANGA.PopulationLib`) modules for the other tags needed to define a group.

```xml
<population>
    <group>
        <mortality>RandomGrowth</mortality>
        <k_die>0.0016</k_die>
    </group>
</population>
```

# Attributes

- ``type`` (string): "RandomGrowth" (no other values accepted)
- ``k_die`` (float): (optional) annual mortality (default: 0.0016)

# Value

A bool.

If False, the plant survives, if False the plant dies.


# Details
## Purpose

Plant mortality depends on growth.
Here, growth refers to the relative change in biovolume (i.e., plant volume based on the selected plant module) between the current and the previous time step.
The probability of dying is indirectly proportional to the relative volume increase.
If the growth of a plant slows down over time, the probability of dying increases.


## Process overview

- Calculate the relative change in biomass (as volume) between the current and the previous time step (`relative_volume_increment`)
```
relative_volume_increment = delta_volume / (time * volume)
```
- Calculate the probability to die (`r`) based on species-specific mortality value `k_die`
```
p_die = k_die / relative_volume_increment
```
- Draw a random number from a uniform distribution (`r`)
- Check if plant survives with the following eq.
````
r < p_die
````

## Application & Restrictions

-

# References

-

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann

# See Also

`pyMANGA.PlantModelLib.Mortality.NoGrowth`, 
`pyMANGA.PlantModelLib.Mortality.Random`,
`pyMANGA.PlantModelLib.Mortality.Memory`


# Examples

- Below is a complete description of how to define a plant group in the project file.

````xml
<population>
    <group>
        <name> Initial </name>
        <species> Avicennia </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>RandomGrowth</mortality>
        <k_die>1e-12</k_die>
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
