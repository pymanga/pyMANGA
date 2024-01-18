The Kiwi plant model concept. 

The Kiwi concept was first introduced by [Berger and
Hildenbrandt (2000)](https://doi.org/10.1016/S0304-3800(00)00298-2), where plant growth is based on the FORMAN model by [Chen and Twilley, 1998](https://doi.org/10.1046/j.1365-2745.1998.00233.x) and competition and resource limitation on the FON approach.

The pyMANGA Kiwi module describes the plant growth.
We recommend to use it with `pyMANGA.ResourceLib.BelowGround.Individual.FON`.
To add resource limitation by salinity, use `pyMANGA.ResourceLib.BelowGround.Generic.Merge`.

The zone of influence is used as a proxy to calculate root and crown plate radii to be used in resource modules.
Scaling dbh to zone of influence (ZOI) based on eq. 1 in Berger & Hildenbrandt (2000).
    $\a_zoi_scaling * (dbh/2/100)**0.5$
... with a_zoi_scaling being a species specific scaling parameter.


Attributes:
    type (string): "Kiwi"

Examples:
    ```xml
    <vegetation_model_type> Kiwi </vegetation_model_type>
    ```
Possible outputs:
    ```xml
    <output> 
        <geometry_output> r_stem </geometry_output>
        <geometry_output> height </geometry_output>
        <geometry_output> r_crown </geometry_output>
        <geometry_output> r_root </geometry_output>
        <growth_output> growth </growth_output>
        <growth_output> ag_factor </growth_output>
        <growth_output> bg_factor </growth_output>
        <growth_output> age </growth_output>
    </output>
    ```