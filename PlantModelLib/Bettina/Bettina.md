The Bettina plant model concept. 

The Bettina concept was first introduced by [Peters et al. (2014](https://doi.org/10.1016/j.ecolmodel.2014.04.001)) 
and this implementation includes recent revisions 
([Peters, Olagoke and Berger 2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005) --- see Appendices A and B).

Attributes:
    type (string): "Bettina"

Examples:
    ```xml
    <vegetation_model_type> Bettina </vegetation_model_type>
    ```
Possible outputs:
    ```xml
    <output> 
        <geometry_output> r_stem </geometry_output> <!-- stem radius, in m -->
        <geometry_output> h_stem </geometry_output> <!-- stem height, in m -->
        <geometry_output> r_crown </geometry_output> <!-- crown radius, in m -->
        <geometry_output> r_root </geometry_output> <!-- root radius, in m -->
        <growth_output> root_surface_resistance </growth_output> <!-- root surface resistance, in s * Pa per m³ -->
        <growth_output> xylem_resistance </growth_output> <!-- xylem resistance, in s * Pa per m³ -->
        <growth_output> psi_zero </growth_output> <!-- water potential gradient with soil water potential = 0, in Pa -->
        <growth_output> salinity </growth_output> <!-- salinity below plant, in kg per kg -->
        <growth_output> growth </growth_output> <!-- biomass increment, in kg per time step -->
        <growth_output> ag_resources </growth_output> <!-- above-ground resources, in m³ per time step -->
        <growth_output> bg_resources </growth_output> <!-- below-ground resources, in m³ per time step -->
        <growth_output> available_resources </growth_output> <!-- resources available, in m³ per time step -->
        <growth_output> ag_factor </growth_output> <!-- above-ground growth reduction factor, unitless -->
        <growth_output> bg_factor </growth_output> <!-- below-ground growth reduction factor, unitless -->
        <growth_output> age </growth_output> <!-- tree age, in sec -->
    </output>
    ```

