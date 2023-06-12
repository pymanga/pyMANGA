The Field Of Neighbourhood (FON) belowground competition concept. FON returns a multiplier 
accounting for the effect of both competition and salinity on resource uptake.

The FON concept was first introduced in the KiWi model 
([Berger and Hildenbrandt 2000](https://doi.org/10.1016/S0304-3800(00)00298-2)). The effect of FON parameters _a_ and 
_b_ is also discussed by Berger and Hildenbrandt ([2003](https://doi.org/10.1023/A:1023965512755)). 

Attributes:
    type (string): "FON"
    domain (nesting tag): coordinates to define the tree interaction grid
    x_1 (domain-nested int): x-coordinate of left border of grid    
    y_1 (domain-nested int): y-coordinate of bottom border of grid
    x_2 (domain-nested int): x-coordinate of right border of grid
    y_2 (domain-nested int): y-coordinate of top border of grid
    x_resolution (int): x-resolution of grid
    y_resolution (int): y-resolution of grid
    aa (float): FON parameter _a_ 
    bb (float): FON parameter _b_ 
    fmin (float): FON parameter _F<sub>min</sub>_ 
    salinity (float): salinity (ppt)

Examples:
    
Specification of domain:
```xml
<domain>
    <x_1> 0 </x_1>
    <y_1> 0 </y_1>
    <x_2> 100 </x_2>
    <y_2> 100 </y_2>
</domain>
```

