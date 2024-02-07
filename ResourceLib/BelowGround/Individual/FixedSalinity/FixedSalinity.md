## Description

This module calculates the reduction in below-ground resource availability caused by pore water salinity beneath a plant.
The calculation is based on the salinity at the model's left and right boundaries.
There is no feedback between plant water uptake and pore water salinity, and no competition.

## Usage

```xml
<belowground>
    <type> FixedSalinity </type>
    <min_x>0</min_x>
    <max_x>22</max_x>
    <salinity>0.035 0.035</salinity>
</belowground>
```

## Attributes

- ``type`` (string): "FixedSalinity"
- ``min_x`` (float): x-coordinate of the left border (x = 0)
- ``max_x`` (float): x-coordinate of the right border (x = max.)
- ``salinity`` (float float or string): either two values representing the salinity (kg/kg) at ``min_x`` and ``max_x`` <strong>or</strong> the path to a csv file containing a time series of salinity (see description above and 
        example below)
- ``variant`` (string): (optional) variant to calculate salinity reduction factor. Default is "bettina". See Notes for more information.
- ``sine`` (nesting-tag): (optional) calculate salinity for each time step based on a sine function. See notes for details.
  - ``amplitude`` (float): (optional) amplitude of the sine function. Default: 0
  - ``stretch`` (float): (optional) stretch of the sine function, i.e., length a full period. Default: 24\*3600\*58 (approx. 1 year)
  - ``offset`` (float): (optional) offset of the sine function (along the time axis). Default: 0
  - ``deviation`` (float): (optional) standard deviation to pick salinity value from sine function. Default: 0

*Note*: all values are given in SI units, but can be provided using equations (see examples).
For salinity, this means typical seawater salinity of 35 ppt is given as 0.035 kg/kg or 35*10**-3 kg/kg.

## Value

This factor describes the availability of below-ground resources for each plant (dimensionless). 
The factor ranges from 0 to 1, with 1 indicating no limitations and 0 indicating full limitations.

## Details
### Purpose

This module describes the below-ground resource limitation induced by the presence of salt. 
Salinity reduces the osmotic water potential and therefore makes it more difficult for halophytic plants to take up water from the soil column. 
This resource limitation corresponds physiologically to drought stress in terrestrial systems. 
The limitation is expressed as a factor varying between 0 and 1.

### Process overview

Each time step, *calculateBelowgroundResources* calls the following sub-procedures:
-	*getPlantSalinity*: calculate salinity below each tree based on the chosen variant
-	*getBGfactor*: calculate below-ground factor

### Sub-processes
#### getPlantSalinity

Salinity within the model domain is defined by two values: salinity (``s_xmin``, ``s_xmax``) on the left (``x_min``) and right (``x_max``) border, respectively. 
Based on those values and the x-position of trees (``x_i``), the salinity below a tree (``s_i``) is interpolated with

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
For  example , if one period equals one year (in seconds), b is equal to (365*3600*24)/2π. Additionally, noise can be added by drawing s_(i,t) from a normal distribution with s_(i,t) (from eq. 15) as mean and a user-defined standard deviation.
If ``s_xm_t`` becomes negative, it is set to 0. 

See <a href="https://github.com/pymanga/sensitivity/blob/main/ResourceLib/BelowGround/Individual/FixedSalinity/sine.md" target="_blank">this example</a> for the effect of each parameter.       

#### getBGfactor

The below-ground factor (belowground_resources) is the ratio of the tree water potential with (psi_wSal) and without (psi_woSal) the effect of salinity. 
If this module is used in with a BETTINA tree, this is calculated as follows:

```
belowground_resources = psi_wSal / psi_woSal 
psi_woSal = psi_leaf + (2 * r_crown + h_stem) * 9810
psi_wSal = ψ_0 + 85e6 * s_i
```

85e6 Pa per kg is the factor to transfer salinity in Pa.

## References


## Author(s)

Jasper Bathmann, Jonas Vollhüter, Marie-Christin Wimmler

## See Also

`pyMANGA.ResourceLib.BelowGround`, `pyMANGA.PlantModelLib.Bettina`

## Examples

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
    <deviation>1/10**3</deviation>
</sine>
```
*or*
```xml
<salinity>35*10**-3 35*10**-3</salinity>
<sine>
    <amplitude>0.01</amplitude>
    <offset>1.57</offset>
    <stretch>5019110</stretch>
    <deviation>0.001</deviation>
</sine>
```
