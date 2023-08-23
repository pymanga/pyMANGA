Below-ground module that enables the use of multiple below-ground resource concepts.

Below-ground resource factors are multiplied.

*NOTE:* Not all combinations are meaningful.

Attributes:
    type (string): "Merge"
    modules (string): list of below-ground resource modules to be combined. Separated by white space.
    all relevant attributes of the chosen modules

Examples:
```xml
<belowground>
    <type> Merge</type>
    <modules>FixedSalinity SymmetricZOI</modules>
        <domain>
            <x_1> 0 </x_1>
            <y_1> 0 </y_1>
            <x_2> 22 </x_2>
            <y_2> 22 </y_2>
        </domain>
    <x_resolution> 88 </x_resolution>
    <y_resolution> 88 </y_resolution>
    <salinity> 0.025 0.035 </salinity>
    <min_x> 0 </min_x>
    <max_x> 22 </max_x>
</belowground>
```

