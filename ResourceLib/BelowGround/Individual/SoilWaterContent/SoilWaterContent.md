# Description

# Usage

```xml

```

# Attributes

- ``type`` (string): "SoilWaterContent" (no other values accepted)
- ``delta_t_concept`` (int): time step length for below-ground concept (seconds). Allows to define different time step length for plant module. 
- ``soil_properties`` (nesting tag): soil properties describing initial soil saturation 
  - ``omega_s`` (float): saturated water content (-)
  - ``omega_r`` (float): residual water content (-)
  - ``alpha`` (float): ??? 
  - ``n`` (float): ??? 
  - ``psi_matrix`` (float): matrix potential (Pa) 
- ``precipitation`` (nesting tag):  
  - ``data_file`` (string): path to precipitation data (text file)
  - ``precipitation_col_number`` (int): number indicating column containing precipitation data
  - ``delta_t_per_row`` (int): recording interval of precipitation data (in seconds)
- ``domain`` (nesting tag): coordinates to define model domain 
  - ``x_1`` (int): x-coordinate of left border of grid 
  - ``y_1`` (int): y-coordinate of bottom border of grid  
  - ``x_2`` (int): x-coordinate of right border of grid 
  - ``y_2`` (int): y-coordinate of top border of grid 
  - ``x_resolution`` (int): x-resolution of grid 
  - ``y_resolution`` (int): y-resolution of grid 
- 
# Value

# Details
## Purpose

## Process overview

## Sub-processes

## Application & Restrictions


# References

<a href="https://doi.org/" target="_blank">Link</a>,


# Author(s)


# See Also

# Examples


