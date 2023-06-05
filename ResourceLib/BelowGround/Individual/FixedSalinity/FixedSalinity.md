Below-ground module defining pore-water salinity as  
(i) constant,  
(ii) a gradient, or   
(iii) a time series.


For the time series, two values (min and max) need to be specified for each time step you want to define the salinity. 
For time steps with no defined salinity, values will be linearly interpolated.
The input file needs to be a csv file with semicolon as separator and 3 columns, defining the time step (in seconds) and salinity on the left and right boundary (in kg/kg). 
*Note:* the first row will be skipped (as we expect the header to be present).  

No feedback between plant water uptake and pore-water salinity.  
No competition. Recommended for species parametrisation.

Salinity below a tree is calculated using the following formula:  

```python
salinity_tree = ((x_tree - min_x) / (max_x - min_x) * (salinity_max - salinity_min) + salinity_min)
```

Attributes:
    type (string): "FixedSalinity"
    min_x (float): x-coordinate of the left border (y-axis)
    max_x (float): x-coordinate of the right border (y-axis)
    salinity (float - float or string): either two values representing the salinity range 
        from min_x to max_x in kg per kg or the path to a csv file containing a time series for salinity 
        values at min_x and max_x


Examples:
    
Option (i): salinity of 35 ppt  constant within the model domain
```xml
<salinity>0.035 0.035</salinity>
```

Option (ii): salinity increasing from 25 to 35 ppt (left to right border)
```xml
<salinity> 0.025 0.035 </salinity>
```

Option (iii): salinity as time series 
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
      
