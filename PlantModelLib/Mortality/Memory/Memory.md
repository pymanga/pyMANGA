The Memory mortality concept.

In Memory, a plant remembers its relative average growth of the preceding N years (in m³ per memory period). 
Relative growth is defined as the fraction of growth in plant biomass (in m³ per m³). 
If the relative growth falls below a certain threshold, a plant dies.
The default threshold is 0.5 % (i.e. <threshold> 0.005 </threshold>).
The default memory period is 1 year (i.e. <period> 31557600 </period>).

This concept is based on mechanistic causes, e.g. slowing down of growth due external perturbations. 
A plant can survive a period of resource scarcity but if conditions do not improve, the plant dies.

No stochasticity involved in this module.

Attributes:
    mortality (string): "Memory"
    period (int): memory period of the plant (seconds). Default: 31,557,600 seconds (= 1 year).
    threshold (float): minimum relative, yearly growth of a plant over the memory period. Default: 0.005 (= 0.5 %).

Examples:
```xml
<plant_dynamics>
    <type> Bettina </type>
    <mortality>Memory</mortality>
    <threshold> 0.005 </threshold>
    <period> 31557600 </period>
</plant_dynamics>
```


