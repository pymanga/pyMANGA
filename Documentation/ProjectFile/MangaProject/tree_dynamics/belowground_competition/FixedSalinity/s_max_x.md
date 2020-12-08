

Max and min values define the interpolation range for the salinity.

salinity_tree = ((x_tree - min_x) / (max_x - min_x) * (salinity_max - salinity_min) + salinity_min)
