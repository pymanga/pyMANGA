The Network below-ground resource module.

In the network module plants can form groups that exchange below-ground resources.
The module is divided in three sections
- root graft formation
- group formation
- below-ground resource exchange

Water exchange can increase or decrease water availability.
This means that the below-ground resource factor can be > 1.

Resource exchange is based on [Wimmler et al. 2022](https://doi.org/10.1093/aob/mcac074).

Attributes:
    type (string): "Network" (module name)
    f_radius (float): proportion of stem radius to set min. radius of grafted roots. Range: >0 to 1.


Example:
    ```xml
    <belowground>
        <type> Network </type>
        <f_radius> 0.25 </f_radius>
    </belowground>
    ```
