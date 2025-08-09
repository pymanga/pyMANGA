# Description

This module calculates the growth (production of biovolume) of saltmarsh plants.
The growth is calculated using a simple model based on resource limitation and competition.

# Usage

```xml
<population>
    <group>
        <vegetation_model_type> Saltmarsh </vegetation_model_type>
        <species> Saltmarsh </species>
    </group>
</population>
```

Go to [Examples](#examples) for more information.

# Attributes

- ``vegetation_model_type`` (string): "Saltmarsh" (no other values accepted)
- ``species`` (string): Path to file defining species or plant functional type (PFT). Possible Inputs: "Saltmarsh" (will use default saltmarsh species defined in `PopulationLib.Species.Saltmarsh.createPlant`) or path to custom species file.

# Value

Three dictionaries each with length = 1 (i.e., for each individual plant).

The dictionary ``geometry`` contains information about plant geometry.
The dictionary ``growth_concept_information`` contains information about plant growth concept.
The dictionary ``parameter`` contains the relevant parameters.


# Details
## Purpose

The purpose of this module is to describe the growth of saltmarsh plants based on resource limitation and competition.

## Plant geometry

Saltmarsh plants are represented as two cylinders:

* one above-ground (AG)
* one below-ground (BG)

Each cylinder is described by:

* radius ($r_{ag}$, $r_{bg}$)
* height ($h_{ag}$, $h_{bg}$)

From this, volumes are computed:

* $V_{ag}$ = $\pi \cdot r_{ag}^2 \cdot h_{ag}$
* $V_{bg}$ = $\pi \cdot r_{bg}^2 \cdot h_{bg}$
* Total volume: $V_{bio} = V_{ag} + V_{bg}$

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
res_{tot} = \min(res_{bg}, res_{ag})
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
- Together with the species-specific growth factor (f_growth), the total growth (grow) in the corresponding time step ($\Delta t$), can be calculated:
$$
growth = res \cdot f_{growth} \cdot \Delta t
$$
- If net growth G is positive, it is allocated to the above- and belowground compartment depending on which one is more limiting and thus needs more investment. To account for this, the ratio of available aboveground and belowground resources is computed and normalized to a range between −0.5 and 0.5. This yields the temporary adjustment factor Ad​, defined as:
$$
Ad = 0.5 - \left( \frac{res_{bg}}{res_{bg} + res_{ag}}\right)
$$
The standardization results to:
$$
f_{res_{bg/ag}} \in \[ -0.5,\ 0.5\]
$$
The allocation weight for the aboveground compartment $w_ag$ is dynamically updated based on a baseline value $w_{ag_{base}}$ (standard allocation factor under equilibrium conditions between aboveground and belowground resources) and the adjustment factor $Ad$:

$$
w_{bg} = w_{bg_{base}} \cdot (1 - Ad)
$$

This formulation ensures that when aboveground resources are more limited than belowground resources (i.e., $Ad > 0$), the plant allocates more resources to the aboveground compartment and vice versa.

Actual growth increment for each compartment is then:

$$
\Delta V_{bg} = growth \cdot w_{bg}\ and\ \Delta V_{ag} = growth \cdot w_{ag}
$$

In case of negative net growth G (maintenance greater than available resources), the model symmetrically reduces biovolume of both compartments:

$$
\Delta V_{bg} = \Delta V_{ag} = \frac{growth}{2}
$$

Volumes are subsequently updated as:

$$
V_{bg,t-1} = V_{bg,t} + \Delta V_{bg}
$$

The plant geometries are recalculated by solving for height h and radius r under the assumption of fixed shape ratios of the cylinders. The new height and radius of each component are derived as:

$$
h_{ag} = \left( \frac{V_{ag}}{\left( \pi \cdot w_{ag}^{2} \right)} \right)^{2/3}\ and\ \left( \frac{V_{bg}}{\left( \pi \cdot w_{bg}^{2} \right)} \right)^{2/3}
$$

$$
r_{ag} = w_{ag} \cdot h_{ag}\ and\ r_{bg} = w_{bg} \cdot h_{bg}
$$




## Application & Restriction

# References

tba

# Authors

tba

# See Also

tba

# Examples
