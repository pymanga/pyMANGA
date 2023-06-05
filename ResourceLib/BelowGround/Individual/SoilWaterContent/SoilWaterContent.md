The SoilWaterContent below-ground resource module.

Attributes:
    type (string): "SoilWaterContent" (module name)
    delta_t_concept (int): time step length for below-ground concept (seconds). Allows to define different time step length for plant module.
    soil_properties (nesting tag): soil properties describing initial soil saturation
    omega_s (soil_properties-nested float): saturated water content (-)
    omega_r (soil_properties-nested float): residual water content (-)
    alpha (soil_properties-nested float): ???
    n (soil_properties-nested float): ???
    psi_matrix (soil_properties-nested float): matrix potential (Pa)
    domain (nesting tag): coordinates to define model domain
    grid x_1 (domain-nested int): x-coordinate of left border of grid
    y_1 (domain-nested int): y-coordinate of bottom border of grid 
    x_2 (domain-nested int): x-coordinate of right border of grid 
    y_2 (domain-nested int): y-coordinate of top border of grid 
    x_resolution (int): x-resolution of grid 
    y_resolution (int): y-resolution of grid 