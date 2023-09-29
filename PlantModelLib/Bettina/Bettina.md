The Bettina plant model concept. 

The Bettina concept was first introduced by [Peters et al. (2014](https://doi.org/10.1016/j.ecolmodel.2014.04.001)) 
and this implementation includes recent revisions 
([Peters, Olagoke and Berger 2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005) --- see Appendices A and B).

Attributes:
    type (string): "Bettina"

Examples:
    ```xml
    <plant_dynamics>
        <type> Bettina </type>
    </plant_dynamics>
    ```
Possible outputs:
    ```xml
    <output> 
        <geometry_output> r_stem </geometry_output>
        <geometry_output> h_stem </geometry_output>
        <geometry_output> r_crown </geometry_output>
        <geometry_output> r_root </geometry_output>
        <growth_output> root_surface_resistance </growth_output>
        <growth_output> xylem_resistance </growth_output>
        <growth_output> available_resources </growth_output>
        <growth_output> psi_zero </growth_output>
        <growth_output> salinity </growth_output>
        <growth_output> growth </growth_output>
        <growth_output> ag_resources </growth_output>
        <growth_output> bg_resources </growth_output>
        <growth_output> ag_factor </growth_output>
        <growth_output> bg_factor </growth_output>
    </output>
    ```

