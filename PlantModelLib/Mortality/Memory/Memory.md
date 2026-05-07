# Description

This module determines whether a plant is dying or not based on the individual plant's growth over a period of time. 
This means that the probability of a plant dying increases as the growth rate decreases and the age of the plant increases.
However, a sudden decrease in growth, e.g. due to resource limitation, does not necessarily lead to the death of the plant.

In this concept, plant mortality is intrinsic and is dependent on plant growth.
This mortality concept includes stochasticity.

It is useful to combine ``Memory`` with ``NoGrowth`` or ``Random``.


# Usage

Mortality is defined for each group of plants.
This example shows only the tags relevant to the mortality concept. 
See the Plant Growth (`pyMANGA.PlantModelLib`) and Population (`pyMANGA.PopulationLib`) modules for the other tags needed to define a group.

```xml
<population>
    <group>
        <mortality>Memory</mortality>
        <period>365.25*24*3600</period>
        <threshold>0.005</threshold>
    </group>
</population>
```

# Attributes

- ``type`` (string): "Random" (no other values accepted)
- ``period`` (int): (optional) memory period of the plant (seconds). Default: 3600*24*365.25 seconds (= 1 year)
- ``threshold`` (float): (optional) minimum relative, yearly growth of a plant over the memory period. Default: 0.005 (= 0.5 %).

# Value

A bool.

If True, the plant survives, if False the plant dies.


# Details
## Purpose

Plant mortality depends on relative growth over a defined period.
Growth is based on the per-step growth variable of the selected plant module.
Relative growth is defined as the average per-step growth over the defined
period divided by the corresponding plant size measure (units depend on the
plant model: m³/m³ for Bettina, cm/cm for Jabowa).

If the relative growth, annualised by multiplying with the number of time steps
per year, falls below a certain threshold, a plant dies.

Here, growth refers to the per-step increment in the plant size measure used
by the selected plant module (e.g., volume for Bettina, dbh for Jabowa).
The probability of dying is indirectly proportional to this relative
increase. If the growth of a plant slows down over time, the probability of
dying increases.

**Contract for plant modules**: any plant module combined with this mortality
concept must store a *per-step* increment in ``plant_module.grow``
(not an annualised rate). Both `pyMANGA.PlantModelLib.Bettina` and
`pyMANGA.PlantModelLib.Jabowa` follow this convention.


## Process overview

- Calculate the number of time steps within the defined memory period
- Calculate the average growth over the memory period
- Calculate the relative growth (`relative_grow`)
- Calculate the number of time steps per year (`steps_per_year`)
- Check if relative growth is below a certain threshold (`threshold`)
```
relative_grow * steps_per_year < threshold
```


## Application & Restrictions

-

# References

<a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>


# Author(s)

Marie-Christin Wimmler

# See Also

`pyMANGA.PlantModelLib.Mortality.NoGrowth`, 
`pyMANGA.PlantModelLib.Mortality.Random`,
`pyMANGA.PlantModelLib.Mortality.RandomGrowth`


# Examples

- Below is a complete description of how to define a plant group in the project file.
- Memory is 5 years and the threshold for relative growth is 0.5%.

````xml
<population>
    <group>
        <name> Initial </name>
        <species> Avicennia </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>Memory</mortality>
        <period>5*365.25*24*3600</period>
        <threshold>0.005</threshold>
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
