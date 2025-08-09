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
Growth is based on the growth variable of the selected plant module.
Relative growth is defined as the average growth over the defined period to plant volume (in m³ per m³). 

If the relative growth falls below a certain threshold, a plant dies.

Here, growth refers to the relative change in biovolume (i.e., plant volume based on the selected plant module) between the current and the previous time step.
The probability of dying is indirectly proportional to the relative volume increase.
If the growth of a plant slows down over time, the probability of dying increases.


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
