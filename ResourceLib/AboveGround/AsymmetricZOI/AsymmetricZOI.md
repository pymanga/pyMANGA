The asymmetric zone of influence (ZOI) above-ground resource concept. 

aZOI returns a multiplier accounting for the effect of competition.

The ZOI concept was originally developed by [Weiner et al. (2001)](https://doi.org/10.1086/321988).

The ZOI module calculates the growth reduction factor based on the ZOI a plant has.
It calculates how many grid cells are occupied by a plant minus the cells occupied by its neighbors.
The ZOI of a plant is either equal to a plant geometry (e.g., crown radius in `pyMANGA.PlantModelLib.Bettina`) or scaled using a species specific scaling parameter (e.g., in `pyMANGA.PlantModelLib.Kiwi`).

In the asymmetric ZOI concept, the larger (higher) plant get all resources in the overlapping area.


Attributes:
    type (string): "AsymmetricZOI"
    domain (nesting tag): coordinates to define the tree interaction grid
    x_1 (domain-nested int): x-coordinate of left border of grid    
    y_1 (domain-nested int): y-coordinate of bottom border of grid
    x_2 (domain-nested int): x-coordinate of right border of grid
    y_2 (domain-nested int): y-coordinate of top border of grid
    x_resolution (domain-nested int): x-resolution of grid
    y_resolution (domain-nested int): y-resolution of grid
    allow_interpolation (bool): (optional) If True, the ZOI of a plant can be smaller than a grid cell and it will be assigned to the nearest node. Default: False.

Note:
    If the `allow_interpolation` tag is set to True and the grid is coarse, the calculation of above-ground resource uptake will be inaccurate and this may affect plant growth.

Examples:
    
```xml
<belowground>
    <type> AsymmetricZOI </type>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 88 </x_resolution>
        <y_resolution> 88 </y_resolution>
    </domain>
</belowground>
```



