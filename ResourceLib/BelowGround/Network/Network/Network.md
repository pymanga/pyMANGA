# Description

This module calculates the reduction or increase in below-ground resource availability caused by water exchange through root grafts.
The module describes group formation, partner selection and the calculation of water availability taking into account water exchange within groups of grafted trees.

The module only functions with ``pyMANGA.PlantModelLib.BettinaNetwork``.
Water flow through trees is a passive process driven by the water potential gradient along the soil-leaf continuum and between trees (exchange).

This module description is part of the pyNET ODD presented in <a href="https://doi.org/10.1016/j.ecolmodel.2024.110916" target="_blank">Wimmler & Berger (2024)</a>.

The module does not consider any other form of competition or below-ground resource limitation.
To do so, see other modules in ``pyMANGA.ResourceLib.BelowGround.Network``.

# Usage

*The values shown here are examples. See Attributes for more information.*

```xml
<belowground>
    <type> Network </type>
    <f_radius> 0.5 </f_radius>
    <exchange> on </exchange> 
</belowground>
```

# Attributes

- ``type`` (string): "Network" (no other values accepted)
- ``f_radius`` (float): proportion of stem radius to set min. radius of grafted roots. Range: >0 to 1.
- ``exchange`` (string): (optional) indicates whether water can be exchange ("on" or "off"). Default: "on".

# Value

A list of values with length = number of plant.

Each value describes the availability of below-ground resources for a plant (dimensionless). 
The factor ranges from 0 to Inf, with 1 indicating no water exchange, 
< 1 indicating that water flows from the focal tree to the partner and 
values > 1 indicating water flows to the focal tree. 

# Details
## Purpose

The ``Network`` module calculates the water uptake of individual and root-grafted trees. 
It therefore, manages group formation and water exchange. 
The effect of water exchange on the water availability for each tree is defined as the ratio of actual to potential water uptake, 
where an influx of water results in values > 1 (unlike all other resource modules). 
In this module, resources are not limited by environmental factors.
They are only affected by water exchange.

## Process overview

This module calls the following sub-procedures:
- ``groupFormation``: Identifies groups of root grafted trees and assign them a unique identifier
  - Set resource variables: graph_dict, pairs
  - Update tree variables: groupID, partner 
- ``rootGraftFormation``:  Initializes the root graft formation process
  - Set resource variables: contact_matrix, pairs 
- ``calculateBGresourcesPlant``: Calculates water absorbed, available and exchanged for each tree
  - Set tree variables: water_available, water_ absorbed, water_exchanged 
- ``getBGfactor``: Calculates the below-ground resource factor
  - Set resource variable: bg_factor

## Sub-processes

The module is divided into three sections: group formation, partner selection and the calculation of water availability taking into account water exchange within groups.

#### Group formation (groupFormation)

This sub-process manages the assignment of trees into groups, which is needed later to calculate below-ground resources.
Therefore, two variables are needed: the tree ID (``plant``) and a list of partner(s) (``partner``) of these trees. 
Based on these attributes, a graph (i.e., a structure connecting objects in a network) is constructed, 
that contains all trees with functional root grafts (``graph_dict``). 
The dictionary lists each tree as key and the partner ID(s) as values. 
Trees that were grafted but died are identified and removed from the current ``graph_dict``. 
Groups with unique IDs (``groupID``) are derived from the dictionary and assigned to each tree.


#### Partner selection (rootGraftFormation)

Partner selection or the initialization of the root graft formation process depends on four tree characteristics:
(i) position, (ii) graft status, (iii) formation status and (iv) size (see below for details). 
If all conditions are met, a pair of trees will start the formation of a grafted root and the following tree variables are set
- ``rgf``: set to 1
- ``potential_partner``: ID of tree to which grafted root is established
- ``r_gr_min``: minimum radius of the grafted root
- ``l_gr``: length of the grafted root
- 
The formation process is described in ``pyMANGA.PlantModelLib.BettinaNetwork``.

**(i) Position**

Tree can potentially form root grafts, if their root plates overlap, 
which is determined by their position (xy) and root plate radius (``r_root``). 
For all pairs whose root plates overlap, the probability that the roots will also come together is determined. 
To find pairs with overlapping root plates, the difference between the distance between the trees and the sum of the root plate radii is calculated.
If the difference is > 0, the root plates overlap. 

``
r_root_i + r_root_j = r_root_ij > dist_ij
``

The probability of contact increases the more the root plates overlap, and is calculated as:

``
p_contact = 1 - (dist_ij / r_root_ij)
``

For each pair of trees, a random number is drawn from a uniform distribution. 
If this number is < ``p_contact``, the roots are in contact. 
The results are stored an n*n matrix (``contact_matrix``), where n is the number of trees in the model.
This matrix is then converted into a 2*k matrix containing all trees whose roots are in contact (``pairs``), 
where ``k`` is the number of pairs with roots in contact.

**(ii) Graft status**

Only one root graft can exist between each pair. 
This means that trees that are already connected will not form another connection with each other.

**(iii) Formation status**

The formation status of trees describes whether a tree is currently in the process of forming a root graft. 
A tree can only form one root graft at a time. 
That is, a pair of trees whose roots are in contact can only start root grafting if they are not currently in the process of root grafting.

**(iv) Tree size**

A pair of trees whose roots are in contact must be of a certain size, determined by the stem radius, in order to develop new root grafts. 
It is defined that a tree's stem radius must be greater than 0.75 cm (i.e., a stem diameter of 1.5 cm). 
This prevents newly recruited trees from immediately starting to form root grafts.

#### Water availability (calculateBGresourcesPlant)

Water uptake is described by three variables: the amount of water taken from the soil (water_absorbed), 
the amount of water exchanged with partner trees (water_exchange) and the amount of water available for the tree (water_available). 
For non-grafted trees water exchange is 0, and the amount taken from the soil equals that available to the tree. 
For grafted trees, the water balance is calculated group-wise as described in Wimmler et al. (2022).  
Water exchange can be switched off completely.

#### Below-ground factor (getBGfactor)

The below-ground factor is the ratio of actual to potential available water, 
whereby the potential available water is calculated following the ``pyMANGA.PlantModelLib.Bettina`` approach (assuming zero salinity).


## Application & Restrictions

-

# References

<a href="https://doi.org/10.1093/aob/mcac074" target="_blank">Wimmler et al. (2022)</a>,
<a href="https://doi.org/10.1016/j.ecolmodel.2024.110916" target="_blank">Wimmler & Berger, 2024</a>,



# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.PlantModelLib.BettinaNetwork``

# Examples

-

