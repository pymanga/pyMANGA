# Description

This module describes tree growth based on the JABOWA growth function presented in <a href="https://doi.org/10.2307/2258570" target="_blank">Botkin et al. 1972</a>.

Species-specific growth parameters are defined in species files.
An example file is stored in the species folder (`pyMANGA.PopulationLib.Species.AvicenniaKiwi`).

# Usage

Plant growth is defined for each group of plants.
This example shows only the tags relevant to this plant concept. 
See the Mortality (`pyMANGA.PlantModelLib.Mortality`) and Population (`pyMANGA.PopulationLib`) modules for the other tags needed to define a group.

```xml
<population>
    <group>
        <vegetation_model_type> Jabowa </vegetation_model_type>
    </group>
</population>
```
# Attributes

- ``vegetation_model_type`` (string): "Jabowa" (no other values accepted)

# Value

Three dictionaries each with length = 1 (i.e., for each individual plant).

The dictionary ``geometry`` contains information about the plant geometry.
The dictionary ``growth_concept_information`` contains information plant growth.
The dictionary ``parameter`` contains the relevant parameters.

# Details
## Purpose

The purpose of this module is to describe tree growth based on the allometric relationship between stem diameter and tree height.

## Tree geometry

In this module, a tree is described only by its height and diameter at breast height (`dbh`).
However, the area covered by the canopy and roots are approximated with the scaling function presented in <a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>.

## Process overview

- Calculate tree height based on stem diameter at breast height (`dbh`)
````
height = (137 + parameter["b2"] * dbh - parameter["b3"] * dbh**2)
````
- Calculate annual growth rate (eq. 5 in Botkin et al. 1972)
````
grow = p_max_growth * dbh * N / D * ag_factor * bg_factor
N = 1 - (dbh * height) / (p_max_dbh * p_max_height)
D = 274 + 3 * p_b2 * dbh - 4 * p_b3 * dbh**2
````
- variables starting with ``p_`` are species-specific parameters (see `pyMANGA.PopulationLib.Species`)
- Calculate new dbh (considering pyMANGAs time step length)
```
dbh = dbh + grow * time / (3600 * 24 * 365.25)
```
- Calculate root and crown radius
```
r_root = r_crown = p_zoi_scaling * dbh**0.5
``` 
- The JABOWA growth function calculates dbh and height in centimeters. For alignment with pyMANGA all variables are transformed to meters.

- Parameters ``p_b2`` and `p_b3` can be estimated using
```
b2 = 2 * (max_height - 137) / max_dbh
b3 = (max_height - 137) / max_dbh**2
```

## Application & Restrictions

**Application**

This module can be used to build the Kiwi model (<a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>).
To do so, combine it with the below-ground modules ``ResourceLib.Belowground.Individual.FON`` and ``ResourceLib.Belowground.Individual.FixedSalinity``.


# References

See <a href="https://doi.org/10.2307/2258570" target="_blank">Botkin et al. 1972</a> for the growth equations and parameterizations for some temperate species.
The growth function has been applied to mangroves, e.g., in <a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>.


# Author(s)

Jasper Bathmann, Marie-Christin Wimmler

# See Also

`pyMANGA.PopulationLib.Species.AvicenniaKiwi`, `pyMANGA.PopulationLib.Species`

# Examples

- Below is a complete description of how to define a plant group in the project file using the Jabowa growth function.

````xml
<population>
    <group>
        <name> avi </name>
        <species> AvicenniaKiwi </species>
        <vegetation_model_type> Jabowa </vegetation_model_type>
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

