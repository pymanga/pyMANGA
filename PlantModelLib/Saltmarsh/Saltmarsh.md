# Description

This module calculates the growth (production of biovolume) of saltmarsh plants, e.g., grasses, shrubs and herbs.
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

* Above-ground volume: $V_{ag}$ = $\pi \cdot r_{ag}^2 \cdot h_{ag}$
* Below-ground volume: $V_{bg}$ = $\pi \cdot r_{bg}^2 \cdot h_{bg}$
* Total volume: $V_{total} = V_{ag} + V_{bg}$

## Process overview

- ``plantVolume``: calculates $V_{ag}$, $V_{bg}$, and $V_{total}$
- ``plantMaintenance``: computes maintenance costs $maint$
- ``agResources``: computes available above-ground resources $res_{ag}$
- ``bgResources``: computes available below-ground resources $res_{bg}$
- ``growthResources``: computes effective resources $res_{eff}$ and net growth $grow$
- ``plantGrowth``: allocates net growth to $V_{ag}$ and $V_{bg}$ and updates geometries ($r$, $h$)
- ``plantVolume`` (again): recalculates volumes after geometry update
- ``waterUptake``: computes transpiration

## Sub-processes

### Above-ground resources

Available above-ground resources depend on the above-ground limitation factor ($f_{reslim,ag} \in (0,1)$) , plant above-ground radius ($r_{ag}$), solar radiation ($p_{sun}$), and the timestep length ($\Delta t$):

$$
res_{ag} = f_{reslim,ag} \cdot \pi \cdot r_{ag}^{2} \cdot p_{sun} \cdot \Delta t
$$

### Below-ground resources

Available below-ground resources depend on the below-ground limitation factor ($f_{reslim,bg} \in (0,1)$), plant geometry ($r_{bg}, h_{bg}, h_{ag}$), solar radiation ($p_{sun}$), hydraulic conductivity ($p_{water}$) and timestep length ($\Delta t$):

$$
res_{bg} = f_{reslim,bg} \cdot \pi \cdot r_{bg}^{2} \cdot h_{bg} \cdot p_{sun} \cdot p_{water}
\cdot \left( h_{ag} + 0.5 \cdot h_{bg} \right)^{-1} \cdot \Delta t
$$

### Maintenance costs

Maintenance costs ($maint$) are proportional to total biovolume ($V_{total}$) and scaled by the species-specific maintenance factor ($p_{maint}$):

$$
maint = V_{total} \cdot p_{maint} \cdot \Delta t
$$

### Effective resources and net growth

The resources effectively available to the plant $res_{eff}$ are given by the minimum of the above-ground and below-ground resources ($res_{ag}$ and $res_{bg}$):

$$
res_{eff} = \min(res_{ag},\ res_{bg})
$$

Potential growth ($grow_{pot}$) is obtained using the species-specific growth factor ($p_{grow}$):

$$
grow_{pot} = res_{eff} \cdot p_{grow}
$$

Subtracting maintenance costs ($maint$) from potential growth ($grow_{pot}$) yields the net growth or shrinkage ($grow$):

$$
grow = grow_{pot} - maint
$$

If grow is negative, the plant shrinks. In this case, it is additionally multiplied by the species- or PFT-specific dieback factor ($p_{dieback}$):

$$
grow = grow \cdot p_{dieback} \quad \text{if} \ grow < 0
$$

### AG/BG allocation and biovolume update if $grow > 0$

Net growth is allocated dynamically adjusted based on the relative limitation of AG vs BG.

The resource limitation ratio $ratio_{ag,bg}$ is computed from the limitation factors ($f_{reslim,ag}$ and $f_{reslim,bg}$):

$$
ratio_{ag,bg} = \frac{f_{reslim,ag}}{f_{reslim,ag} + f_{reslim,bg}}
$$

Since $f_{\mathrm{reslim},ag} \in (0,1)$ and $f_{\mathrm{reslim},bg} \in (0,1)$, it follows that $ratio_{ag,bg} \in (0,1)$.

A temporary adjustment factor ($Ad$) is defined as:

$$
f_{ad} = 0.5 - ratio_{ag,bg}
$$

Thus:

$$
f_{ad} \in (-0.5,\ 0.5)
$$

The allocation weight ($w_{ratio_{ag,bg}}$) is then obtained by multiplying the species-specific baseline allocation parameter $p_{ratio_{ag,bg}}$ by the adjustment factor $1 - f_{ad}$ :

$$
w_{ratio_{ag,bg}} = p_{ratio_{ag,bg}} \cdot (1 - f_{ad})
$$

Net growth is then split as:

$$
\Delta V_{bg} = grow \cdot w_{ratio_{ag,bg}}
\qquad \text{and} \qquad
\Delta V_{ag} = grow \cdot (1 - w_{ratio_{ag,bg}})
$$

### AG/BG allocation and biovolume update if $grow \le 0$

The model symmetrically reduces AG and BG biovolume:

$$
\Delta V_{ag} = \Delta V_{bg} = \frac{grow}{2}
$$

### Volume update and geometry recalculation

$$
V_{ag} = V_{ag} + \Delta V_{ag}
\qquad \text{and} \qquad
V_{bg} = V_{bg} + \Delta V_{bg}
$$

Plant geometry is recalculated from updated compartment volumes with species specific shape parameters ($p_{ratio\_ag}$ and $p_{ratio\_bg}$) that define the ratio of radius to height for AG and BG cylinders, respectively:

- $r_{ag} = p_{ratio\_{ag}} \cdot h_{ag}$
- $r_{bg} = p_{ratio\_{bg}} \cdot h_{bg}$

With these fixed ratios, height is derived from cylinder volume:

$$
h_{ag} = \left( \frac{V_{ag}}{\pi \cdot p_{ratio\_ag}^{2}} \right)^{1/3}
\qquad \text{and} \qquad
h_{bg} = \left( \frac{V_{bg}}{\pi \cdot p_{ratio\_bg}^{2}} \right)^{1/3}
$$

Radii follow directly:

$$
r_{ag} = p_{ratio\_{ag}} \cdot h_{ag}
\qquad \text{and} \qquad
r_{bg} = p_{ratio\_{bg}} \cdot h_{bg}
$$

### Water uptake / transpiration

Transpiration is computed proportional to total plant volume, species-specific transpiration factor ($p_{transpiration}$) and timestep length ($\Delta t$):

$$
transpiration = V_{total} \cdot p_{transpiration} \cdot \Delta t
$$

## Application & Restriction

# References

tba

# Authors

tba

# See Also

tba

# Examples
