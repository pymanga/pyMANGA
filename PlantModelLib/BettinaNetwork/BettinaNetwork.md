# Description

This module describes tree growth based on the concept presented in <a href="https://doi.org/10.1016/j.ecolmodel.2024.110916" target="_blank">Wimmler & Berger (2024)</a>.
This is an extension of ``pyMANGA.PlantModelLib.Bettina``.

The BETTINA tree geometry is extended by a cylinder representing the common grafted root between each grafted pair,
which is a function of its radius ``r_gr`` and length ``l_gr`` and has the volume

``
V_gr = pi * l_gr * r_gr^2
``

The length of the flow path through the common root is approximated as the mean of the distance between the grafted trees i and j and the sum of their root radii.

Species-specific growth parameters are defined in species files.
An example file is stored in the species folder (`pyMANGA.PopulationLib.Species.Avicennia`).

# Usage

*The values shown here are examples. See Attributes for more information.*

```xml
<vegetation_model_type> BettinaNetwork </vegetation_model_type>
<f_growth> 0.25 </f_growth>
<variant> v2 </variant>
```

# Attributes

- ``vegetation_model_type`` (string): "BettinaNetwork" (no other values accepted)
- ``variant`` (string): root graft formation variant. Possible inputs: 'v0', 'v1' and 'v2'. See ``Details`` for more information.
- ``f_growth`` (float): (optional) fraction of resources allocated to root graft development instead of girth growth. Only relevant for variant 'v2'.

# Value

Four dictionaries each with length = 1 (i.e., for each individual plant).

The dictionary ``geometry`` contains information about the plant geometry.
The dictionary ``growth_concept_information`` contains information plant growth.
The dictionary ``parameter`` contains the relevant parameters.
The dictionary ``network`` contains information describing the individual status regarding the network (root grafting).


# Details
## Purpose

This module describes tree growth and is based on the individual tree model ``pyMANGA.PlantModelLib.Bettina`` <a href="https://doi.org/10.1016/J.ECOLMODEL.2014.04.001" target="_blank">(Peters et al., 2014)</a>. 
In this model, a tree is described by for geometric measures defined the root system, the stem and the crown. 
Resources are allocated to the different parts in order to optimize resource uptake. 
Resources are water and light, whereby water uptake and flow are described by Darcy’s law. 

BettinaNetwork extents the BETTINA tree by adding a new geometry, the grafted root which can connect one tree to a neighbouring tree and allow the transfer of water (i.e., either increase or decrease available below-ground resources).

## Process overview

BettinaNetwork calls the following sub-procedures, whereby procedures divergent from the BETTINA model are marked with an asterisk and are explained in more detail below.

- ``flowLength``: Calculate the flow path length from root to crown
  - Set tree variable flow_length
- ``treeVolume``: Calcualte tree volume (biomass)
  - Set tree variable volume 
- ``treeMaintenance``: Calculate resources used for maintenance	
  - Set tree variable maint 
- ``bgResources``: Calculate the available below-ground resource factors	
  - Set tree variable bg_factor 
- ``agResources``: Calculate the available above-ground resource factors	
  - Set tree variable ag_factor
- ``*growthResources``: Calculate biomass increment and call mortality modules	
  - Set tree variables grow and survive
- ``*treeGrowthWeights``: Calculate weighting factors to distribute biomass increment to different tree parts	
  - Set tree variables weight_stemgrowth, weight_crowngrowth, weight_girthgrowth and weight_rootgrowth 
- ``treeGrowth``: Update tree geometry based on weights	
  - Set tree variables h_stem, r_crown, r_stem and r_root


## Sub-processes

The procedures ``growthResources`` and ``treeGrowthWeights`` contain case selectors, calling the respective ``rootGraftFormation`` procedure. 
The modification of these procedures according to the chosen variant is explained below. 

#### Variant v0

Variant v0 is the null concept and describes immediate root grafting without resource allocation (no costs). 
That is, if roots are in contact (information provided by the below-ground resource module Network), 
they fuse immediately.
In ``rootGraftFormationV0`` the variables ``potential_partner``, ``rgf`` are reset to their default and the potential partner is moved to the list of partners.

#### Variant v1

In variant v1, root graft formation lasts for 2 years. 
During this period a fraction of the growth resources (``f_growth``) of both trees is allocated to the common roots, 
and the involved trees cannot form other root grafts during this period. 
That is, growth of all other geometry parameters is reduced during this time.
There is no mechanistic increment of the grafted root radius. 
It is assumed that after two years the common root is functional and of size ``f_radius*r_stem``.

#### Variant v2

In variant v2, root graft formation is based on the resource allocation concept used in BETTINA and therefore, 
the duration of the process and the amount of resources spent is adaptive and estimated individually for each tree. 
It is assumed that resources usually spent for girth growth are partially allocated to the common root until the ``r_gr`` is considered functional. 
That is, root graft formation lasts until ``r_gr ≥ r_gr_min``.

The increment of ``r_gr`` is a function of the common root volume ``V_gr``. 
Each tree has a share on the common root proportional to the total root radius ``r_root``. 
Thus, the volume that belongs to each tree is i

``
vol_gr = pi * f_growth * l_gr * r_gr**2
``

with 

``
f_growth = r_root_i / (r_root_i + r_root_j)
``

and ``i`` and ``j`` being the trees involved.

The increment is a function of the volume and calculated as:

``
inc_r_gr = (weight_gr * grow / (2 * pi * l_gr * r_gr))
``

With ``w_rg`` is the weighting coefficient for resource allocation and growth is the biomass-equivalent for growth. 
The initial value for r_rg is 0.004 m.

Empirical studies reported a reduction in radial growth during root graft formation (Tarroux and DesRochers, 2011; Quer et al., 2022). 
In the model, a fraction f_growth of resources allocated to the stem is used for root graft formation. 
The weighing coefficient graft growth is thus:

``
weight_gr = weight_girthgrowth * f_growth
``

The girth growth weighting factor is reduced to:

``
weight_girthgrowth = weight_girthgrowth * (1 - f_growth)
``

Both trees involved allocate resources separately and within the own scope and therefore, 
the completion of the root graft is limited by the slower growing tree. 
The tree that finishes his share and is ready for new potential partners (see ``pyMANGA.ResourceLib.BelowGround.Network.Network``).

As the common root is part of the root systems of the involved trees, its growth and maintenance are covered by the resource allocation to the roots as described in ``pyMANGA.PlantModelLib.Bettina``. 
The volume of the common root prorated for each tree involved can also be represented by the cable root volume of the tree,
which is also a function of the stem radius.

In ``rootGraftFormationV2`` the growth of the radius of the grafted root is calculated based on the updated weighting factors for girth and grafted root growth. 
If the grafted root is functional, the variables ``potential_partner``, rgf are reset to their default and the potential partner is moved to the list of partners.


## Application & Restrictions

-

# References

<a href="https://doi.org/10.1016/J.ECOLMODEL.2014.04.001" target="_blank">Peters et al., 2014</a>,
<a href="https://doi.org/10.3732/ajb.1000261" target="_blank">Tarroux and DesRochers, 2011</a>,
<a href="https://doi.org/10.1111/oik.09666" target="_blank">Quer et al., 2022</a>,
<a href="https://doi.org/10.1016/j.ecolmodel.2024.110916" target="_blank">Wimmler & Berger, 2024</a>,



# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.ResourceLib.BelowGround.Network.Network``,
``pyMANGA.PlantModelLib.Bettina``


# Examples

-

