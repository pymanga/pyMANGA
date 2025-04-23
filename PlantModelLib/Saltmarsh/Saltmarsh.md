# Description

This module calculates the growth (production of biovolume) of saltmarsh plants.
The growth is calculated using a simple model based on resource limitation and competition.

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

## Process overview

The following sub-procedures are called by the module:

- ``plantVolume``: Calculates the biovolume of the plant
  - Set plant variable volume
- ``plantMaintenance``: Calculates the maintenance of the plant
  - Set plant variable maint, volume_ag, volume_bg, r_volume_ag_bg
- ``growthResources``: Calculates the resources available to the plant and the total plant growth
  - Set plant variable available_resources and grow
- ``plantGrowthWeights``: Calculates the growth weights of the plant
  - Set plant variable w_r_ag, w_h_ag, w_r_bg, w_h_bg
- ``plantGrowth``: Calculates the growth of the different geometries of the plant
  - Set plant variable inc_r_ag, inc_h_ag, inc_r_bg, inc_h_bg

## Sub-processes

- The resources available to the plant (res_tot) are calculated from the minimum of the two resources (res_bg and res_ag).
$$
res_{tot} = \min(res_bg, res_ag)
$$
- The plant can use only a part of this resources for growth.
First they have to use a part of the resources for maintenance (maint):
$$
maint = \left( V_{bio} \cdot f_{maint} \right) \cdot \Delta t
$$
- In this module, a plant is described by two cylinders, one above-ground (ag) and one below-ground (bg).
These cylinders have two parameters each, i.e., height (h) and radius (r).
With this four parameters (h_ag, r_ag, h_bg, r_bg) the biovolume is calculated with the following equation:
$$
V_{bio} = \pi \cdot r_{ag}^2 \cdot h_{ag} + \pi \cdot r_{bg}^2 \cdot h_{bg}
$$
- Maintenance (maint) now can be used to calculate the part of the resources (res) that leads to an increase or decrease in biomass:
$$
res = res_{tot} - maint
$$
- Together with the species-specific growth factor (f_growth), the total growth (g_tot) in the corresponding time step ($\Delta t$), can be calculated:
$$
g_{tot} = res \cdot f_{growth} \cdot \Delta t
$$
- This growth is then divided between the different geometries (radius and height of the above-ground and below-ground cylinder). In principle, a species-specific ratio of above-ground and below-ground growth is decisive for this (f_ratio_bg,ag). However, the ratio is corrected by the limiting resource. The plant responds to the limitation by growing the affected part proportionately stronger:
$$
f_{res_{bg,}_{res_{ag}}} = \left( \frac{res_{bg}}{res_{bg} + res_{ag}} - 0.5 \right) \cdot 0.4
$$
The standardization results to:
$$
f_{res_{bg,}_{res_{ag}}} \in [-0.2, 0.2]
$$
This means that the species-specific factor that determines the division of biomass growth between below-ground and above-ground biomass (f_ratio_bg,ag) can be changed by a maximum of +/- 20 per cent. This factor is used to correct the distribution of resources to above-ground and below-ground growth depending on the limitation situation:
$$
f_{growth}_{bg,ag} = f_{ratio}_{bg,ag} \cdot f_{res_{bg,}_{res_{ag}}}
$$
The specific standard weights dependent on the PFTs (w_ag and w_bg). The growth weights of the individual geometries can now be calculated:
$$
w_{r_{ag}} = f_{growth_{bg,ag}} \cdot w_{ag}
w_{h_{ag}} = f_{growth_{bg,ag}} \cdot (1 - w_{ag})
w_{r_{bg}} = \left( 1 - f_{growth_{bg,ag}} \right) \cdot w_{bg}
w_{h_{bg}} = \left( 1 - f_{growth_{bg,ag}} \right) \cdot (1 - w_{bg})
$$
- Finally, the plant growth:
$$
r_ag = r_ag + w_{r_{ag}} \cdot g_{tot}
h_ag = h_ag + w_{h_{ag}} \cdot g_{tot}
r_bg = r_bg + w_{r_{bg}} \cdot g_{tot}
h_bg = h_bg + w_{h_{bg}} \cdot g_{tot}
$$

**Application & Restriction**

-

# References

tba

# Authors

tba

# See Also

tba

# Examples
