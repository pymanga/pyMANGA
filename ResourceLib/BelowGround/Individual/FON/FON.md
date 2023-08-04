The Field Of Neighbourhood (FON) below-ground resource concept. 
FON returns a multiplier accounting for the effect of competition.

*Note* If the effect of salinity on resource uptake should be considered use below-ground module `pyMANGA.ResourceLib.BelowGround.Generic.Merge.Merge`.

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
    x_resolution (domain-nested int): x-resolution of grid
    y_resolution (domain-nested int): y-resolution of grid
    aa (float): FON parameter *a* 
    bb (float): FON parameter *b* 
    fmin (float): FON parameter *F<sub>min</sub>* 

Examples:
    
FON without the effect of salinity:
```xml
<belowground>
    <type> FON </type>
    <domain>
        <x_1>0</x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 88 </x_resolution>
        <y_resolution> 88 </y_resolution>
    </domain>
    <aa>10</aa>
    <bb>1</bb>
    <fmin>0.1</fmin>
</belowground>
```
FON with the effect of salinity:
```xml
<belowground>
    <type> Merge </type>
    <modules> FON FixedSalinity </modules>
    <domain>
        <x_1>0</x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_resolution> 88 </x_resolution>
        <y_resolution> 88 </y_resolution>
    </domain>
    <aa>10</aa>
    <bb>1</bb>
    <fmin>0.1</fmin>
    <salinity> 0.025 0.035 </salinity>
    <min_x>0</min_x>
    <max_x>22</max_x>
</belowground>
```

