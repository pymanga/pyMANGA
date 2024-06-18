# Description

This module calculates the reduction in below-ground resource availability caused by pore water salinity beneath a plant.
The area beneath a plant depends on the abstraction of the plant geometry in chosen plant growth model.
The calculation is based on the salinity at the model's left and right boundaries.
There is no feedback between plant water uptake and pore water salinity, and no competition.

This module can be used in simulations where salt is a limiting growth factor, e.g. mangrove forests or abandoned mines.
Salinity can also be used as a proxy for drought stress. Salinity decreases soil water potential, similar to a decrease in water content.

# Usage

```xml
<belowground>
    <type> FixedSalinity </type>
    <min_x>0</min_x>
    <max_x>22</max_x>
    <salinity>0.035 0.035</salinity>
</belowground>
```

Go to [Examples](#examples) for more information


# Attributes

- ``type`` (string): "FixedSalinity" (no other values accepted)
- ``min_x`` (float): x-coordinate of the left border (x = 0)
- ``max_x`` (float): x-coordinate of the right border (x = max.)
- ``salinity`` (float float or string): either two values representing the salinity (kg/kg) at ``min_x`` and ``max_x`` <strong>or</strong> the path to a csv file containing a time series of salinity (see description above and 
        example below)
- ``sine`` (nesting-tag): (optional) calculate salinity for each time step based on a sine function. See notes for details.
  - ``amplitude`` (float): (optional) amplitude of the sine function. Default: 0
  - ``stretch`` (float): (optional) stretch of the sine function, i.e., length of a full period. Default: 24\*3600\*58 (approx. 1 year)
  - ``offset`` (float): (optional) offset of the sine function (along the time axis). Default: 0
  - ``noise`` (float): (optional) standard deviation to pick salinity value from sine function. Default: 0

*Note*: all values are given in SI units, but can be provided using equations (see examples).
For salinity, this means typical seawater salinity of 35 ppt is given as 0.035 kg/kg or 35\*10\**-3 kg/kg.

# Value

A list of values with length = number of plant.

Each value describes the availability of below-ground resources for a plant (dimensionless). 
The factor ranges from 0 to 1, with 1 indicating no limitations and 0 indicating full limitations.

# Details
## Purpose

This module describes the below-ground resource limitation induced by the presence of salt. 
Salinity reduces the osmotic water potential and therefore makes it more difficult for halophytic plants to take up water from the soil column. 
This resource limitation corresponds physiologically to drought stress in terrestrial systems. 
The limitation is expressed as a factor varying between 0 and 1.

## Process overview

Each time step, *calculateBelowgroundResources* calls the following sub-procedures:
-	*getPlantSalinity*: calculate salinity below each plant based on the chosen variant
-	*getBGfactor*: calculate below-ground factor

## Sub-processes
### getPlantSalinity

Salinity within the model domain is defined by two values: salinity (``s_xmin``, ``s_xmax``) on the left (``x_min``) and right (``x_max``) border, respectively. 
Based on those values and the x-position of plants (``x_i``), the salinity below a plant (``s_i``) is interpolated with

```
s_i = s_xmin + (x_i - x_min) * (s_xmax - s_xmin) / (x_max - x_min)
```

There are three variants to calculate the variation of salinity in time: fixed, variable, or from file.  
 - Fixed: no temporal variation in salinity
 - From file: temporal variations of ``s_xmin`` and ``s_xmax`` at given time steps are read from a csv-file
 - Sine: temporal variation follows a sine function. ``s_xmin_t`` and ``s_xmax_t`` are calculated for each time step with

```
s_xm_t = a * sin(t / b + c) + s_xi
```
where ``a`` and ``b`` define the vertical and horizontal stretch of the function, respectively, ``c`` the offset along the time axis, ``t`` the time and ``s_xi`` the salinity at the borders (i.e., ``s_xmin`` and ``s_xmax``). 
More specifically, ``b`` specifies the length of a full period. 
For  example , if one period equals one year (in seconds), b is equal to (365\*3600\*24)/2π. 
Additionally, noise can be added by drawing ``s_i_t`` from a normal distribution with ``s_i_t`` as mean and a user-defined standard deviation.
If ``s_xm_t`` becomes negative, it is set to 0. 

See <a href="https://github.com/pymanga/sensitivity/blob/main/ResourceLib/BelowGround/Individual/FixedSalinity/sine.md" target="_blank">this example</a> for the effect of each parameter.       

### getBGfactor

The below-ground factor (``belowground_resources``) is calculated based on the salinity response function of the plant module.
This is specified as ``r_salinity`` in the species file.
There are two possible responses, introduced in the following.

**bettina**

If the response is based on the BETTINA approach (i.e., ``parameter["r_salinity"] = "bettina"``), the below-ground factor (``belowground_resources``) is the ratio of the plant water potential with (``psi_wSal``) and without (``psi_woSal``) the effect of salinity. 
This is calculated as follows:

```
belowground_resources = psi_wSal / psi_woSal 
psi_woSal = psi_leaf + (2 * r_crown + h_stem) * 9810
psi_wSal = ψ_0 + 85e6 * s_i
```

85e6 Pa per kg is the factor to transfer salinity in Pa.


**forman**

If the response is based on the Forman approach (i.e., ``parameter["r_salinity"] = "forman"``), the below-ground factor (``belowground_resources``) is follows a sigmoid function. 
This is calculated as follows:

```
e = salt_effect_d * salt_effect_ui - salinity_plant*10**3
belowground_resources = 1 / (1 + np.exp(e))
```

``salt_effect_d`` and ``salt_effect_ui`` are species-specific calibration factors.

## Application & Restrictions

**Application**

- It is not useful to use this module with any `Network` module, e.g. `pyMANGA.PlantModelLib.BettinaNetwork`.
- This module can be used with other resource module via `pyMANGA.ResourceLib.BelowGround.Generic.Merge` to combine resource limitation and competition

**Restrictions**

- There are no restrictions on input parameters. However, very high salinity values will result in immediate plant death.

# References

<a href="https://doi.org/10.1016/j.ecolmodel.2014.04.001" target="_blank">Peters et al. (2014)</a>,
<a href="https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>,
<a href="https://doi.org/10.1046/j.1365-2745.1998.00233.x" target="_blank">Chen & Twilley (1998)</a>


# Author(s)

Jasper Bathmann, Jonas Vollhüter, Marie-Christin Wimmler

# See Also

`pyMANGA.ResourceLib.BelowGround`, `pyMANGA.PlantModelLib.Bettina`, `pyMANGA.PopulationLib.Species.Avicennia`

# Examples
## Project file snippets

- Define salinity of 35 ppt, homogenous in space and constant over time, on a model domain of 22 m

```xml
<belowground>
    <type> FixedSalinity </type>
    <min_x>0</min_x>
    <max_x>22</max_x>
    <salinity>35*10**-3 35*10**-3</salinity>
</belowground>
```

- Define salinity increasing from the left to the right border from 25 to 35 ppt (and constant over time)

```xml
<salinity> 0.025 0.035 </salinity>
```

- Define salinity as a time series provided as [csv-file](https://github.com/pymanga/pyMANGA/blob/master/Benchmarks/ExampleSetups/FixedSalinityFromFile/inputFiles/salinity_A.csv)

```xml
<salinity> Benchmarks/ExampleSetups/FixedSalinityFromFile/inputFiles/salinity_A.csv </salinity>
```

- Define salinity with temporal variation following a sine function, with 
  - reference values at the borders of 35 ppt, 
  - an amplitude of 10 ppt, 
  - noise of 1 ppt, 
  - offset of 0.5*pi and 
  - 1 year for a full period

```xml
<salinity>35*10**-3 35*10**-3</salinity>
<sine>
    <amplitude>10/10**3</amplitude>
    <offset>np.pi/2</offset>
    <stretch>3600*24*365/2/np.pi</stretch>
    <noise>1/10**3</noise>
</sine>
```
*or*
```xml
<salinity>35*10**-3 35*10**-3</salinity>
<sine>
    <amplitude>0.01</amplitude>
    <offset>1.57</offset>
    <stretch>5019110</stretch>
    <noise>0.001</noise>
</sine>
```

## Run this module

Check out our <a target="_blank" href="https://github.com/pymanga/pyMANGA/tree/master/Benchmarks"> benchmark library</a>. There are several benchmarks that include ``FixedSalinity``.

Run the module in combination with the Bettina plant growth module with the following code (from the pyMANGA root directory)

```
py .\MANGA.py -i .\Benchmarks\ModuleBenchmarks\PlantModules\Bettina\Belowground\FixedSalinity\FixedSalinity.
xml
```

or in combination with the Kiwi plant growth module


```
py .\MANGA.py -i .\Benchmarks\ModuleBenchmarks\PlantModules\Kiwi\Belowground\FixedSalinity\FixedSalinity.
xml
```