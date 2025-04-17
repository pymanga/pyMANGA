# Description

This module calculates the growth (production of biovolume) of saltmarsh plants.
The growth is calculated using a simple model based on resource limitation and competition.
Resource limitation is modelled with the submodel FixedSalinity.
The same applies to the competition: Here the Zone of Influence (ZOI) models can be used.

This module can be used in simulations where you want to include the growth of saltmarsh plants.

# Usage

```xml
<population>
    <group>
        <vegetation_model_type> Saltmarsh </vegetation_model_type>
        <species> Saltmarsh </species>
    </group>
</population>
```

Go to [Examples](#examples) for more information

# Attributes

- ``vegetation_model_type`` (string): "Saltmarsh" (no other values accepted)
- ``species`` (string): Saltmarsh species oder PFT. Possible Inputs: "Saltmarsh" or path to individual species file.

# Value

Three dictionaries each with length = 1 (i.e., for each individual plant).

The dictionary ``geometry`` contains information about the plant geometry.
The dictionary ``growth_concept_information`` contains information plant growth.
The dictionary ``parameter`` contains the relevant parameters.


# Details
## Purpose

The purpose of this module is to describe the growth of saltmarsh plants based on resource limitation and competition.

## Plant geometry

In this module, a plant is described by two cylinders, one above ground and one blowground.
These two cylinders have two parameters, the height and the radius.
With this four parameters (h_ag, r_ag, h_bg, r_bg) the volume of the plant can be calculated.

## Process overview

- For the calculation of the below and above ground resources you have to use one ore more of the resource submodels (e.g. FixedSalinity and AsymetricZOI).
the resources available to the plant (res_tot) are calculated from the minimum of the two resources (res_bg and res_ag).
````
res_{tot} = \min(res_bg, res_ag)
````
- The plant can use only a part of this resources for growth.
First they have to use a part of the resources for maintenance (maint):
````
maint = \left( V_{bio} \cdot f_{maint} \right) \cdot \Delta t
````
- The Biovolume is calculated with the following equation:
````
V_{bio} = \pi \cdot r_{ag}^2 \cdot h_{ag} + \pi \cdot r_{bg}^2 \cdot h_{bg}
````
- Maintenance (maint) now can be used to calculate the part of the resources (res) that leads to an increase or decrease in biomass:
```
res = res_{tot} - maint
```
- Together with the species-specific growth factor (f_growth), the total growth (g_tot) in the corresponding time step ($\Delta t$), can be calculated:
```
g_{tot} = res \cdot f_{growth} \cdot \Delta t
```
- This growth is then divided between the different geometries (radius and height of the above-ground and below-ground cylinder). In principle, a species-specific ratio of aboveground and belowground growth is decisive for this (f_ratio_bg,ag). However, the ratio is corrected by the limiting resource. The plant responds to the limitation by growing the affected part proportionately stronger:
``` 
f_{res_{bg,}_{res_{ag}}} = \left( \frac{res_{bg}}{res_{bg} + res_{ag}} - 0.5 \right) \cdot 0.4
```
The standardization results to:
```
f_{res_{bg,}_{res_{ag}}} \in [-0.2, 0.2]
```
This means that the species-specific factor that determines the division of biomass growth between belowground and aboveground biomass (f_ratio_bg,ag) can be changed by a maximum of +/- 20 per cent. This factor is used to correct the distribution of resources to above-ground and below-ground growth depending on the limitation situation:
```
f_{growth}_{bg,ag} = f_{ratio}_{bg,ag} \cdot f_{res_{bg,}_{res_{ag}}}
```
The specific standard weights dependent on the PFTs (w_ag and w_bg). The growth weights of the individual geometries can now be calculated:
```
w_{r_{ag}} = f_{growth_{bg,ag}} \cdot w_{ag}
w_{h_{ag}} = f_{growth_{bg,ag}} \cdot (1 - w_{ag})
w_{r_{bg}} = \left( 1 - f_{growth_{bg,ag}} \right) \cdot w_{bg}
w_{h_{bg}} = \left( 1 - f_{growth_{bg,ag}} \right) \cdot (1 - w_{bg})
```
- Finally, the plant growth:
```
r_ag = r_ag + w_{r_{ag}} \cdot g_{tot}
h_ag = h_ag + w_{h_{ag}} \cdot g_{tot}
r_bg = r_bg + w_{r_{bg}} \cdot g_{tot}
h_bg = h_bg + w_{h_{bg}} \cdot g_{tot}
```

**Application**

For the calculation of the resource availability can be used ``ResourceLib.Belowground.Individual.FixedSalinity`` and ``ResourceLib.Belowground.Individual.SymmetricZOI`` for the belowground resources and ``ResourceLib.Aboveground.Individual.AsymmetricZOI`` for the aboveground resources.


# References

tba



*Note*: all values are given in SI units, but can be provided using equations (see examples).
For salinity, this means typical seawater salinity of 35 ppt is given as 0.035 kg/kg or 35\*10\**-3 kg/kg.
