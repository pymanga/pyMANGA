Below-ground module defining porewater salinity as  
(i) constant,  
(ii) a gradient, or   
(iii) a time series.

For a time series of salinity, you must create a csv input file (with semicolon as the separator) with 3 columns, 
defining a time step (in seconds) and salinity (in kg/kg) on the left (i.e. at min_x) and right (i.e. at max_x) 
boundary at that time step. For intermediate time steps with no defined salinity, values will be linearly interpolated.
*Note:* the first row of the input file will be skipped and should be used for headers.  

No feedback between plant water uptake and porewater salinity.  
No competition. Recommended for species parametrisation.

Salinity below a tree is calculated using the following formula:  

```python
salinity_tree = ((x_tree - min_x) / (max_x - min_x) * (salinity_max - salinity_min) + salinity_min)
```

Attributes:
    type (string): "FixedSalinity"
    min_x (float): x-coordinate of the left border (y-axis)
    max_x (float): x-coordinate of the right border (y-axis)
    salinity (float float or string): either two values representing the salinity (kg/kg) range 
        from min_x (first value) to max_x (second value) _or_ the path to a csv file containing a time series of salinity (see description above and 
        example below)


Examples:
    
Option (i): constant salinity of 35 ppt across the model domain
```xml
<salinity> 0.035 0.035 </salinity>
```

Option (ii): increasing gradient of salinity from 25 to 35 ppt (left to right border)
```xml
<salinity> 0.025 0.035 </salinity>
```

Option (iii): time series of salinity 
```xml
<salinity> test/SmallTests/inputFiles/salinity_A.csv </salinity>
```

- Example csv file:
```json
t_step;salinity_1;salinity_2
0;0.010;0.020
1000000;0.011;0.021
2000000;0.012;0.022    
```
      
