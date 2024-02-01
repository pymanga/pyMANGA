Below-ground module defining pore-water salinity as  
(i) constant,  
(ii) a gradient, or   
(iii) a time series.

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
    salinity (float float or string): either two values representing the salinity (kg/kg) range 
        from min_x (first value) to max_x (second value) <strong>or</strong> the path to a csv file containing a time series of salinity (see description above and 
        example below)
    variant (string): (optional) variant to calculate salinity reduction factor. Default is "bettina". See Notes for more information.
    sine (nesting-tag): (optional) calculate salinity for each time step based on a sine function. See notes for details.
    amplitude (sine-nested float): (optional) amplitude of the sine function. Default: 0
    stretch (sine-nested float): (optional) stretch of the sine function, i.e., length a full period. Default: 24*3600*58 (approx. 1 year)
    offset (sine-nested float): (optional) offset of the sine function (along the time axis). Default: 0
    deviation (sine-nested float): (optional) standard deviation to pick salinity value from sine function. Default: 0

*Note*: all values are given in SI units, but can be provided using equations (see examples)

**Notes:**

*Variant*
- Calculate salinity reduction factor  
    - "bettina" (default): ratio of zero-salinity and actual water potential. Zero-salinity water potential based on water potential difference between leaf (minimum leaf water potential) and porewater (osmotic potential).
    - "forman": sigmoidal salinity stress factor based on FORMAN model by Chen and Twilley (1998). See pyMANGA sensitivity repository for [details](https://github.com/pymanga/sensitivity/blob/main/ResourceLib/BelowGround/Individual/FixedSalinity/forman.md).

*Sine*
- Calculate salinity (sal_xi_t) on the left and right model domain using a sine function
```python
sal_xi_t = amplitude * sin(time / stretch + offset) + sal_i
```
- See pyMANGA sensitivity repository for [details](https://github.com/pymanga/sensitivity/blob/main/ResourceLib/BelowGround/Individual/FixedSalinity/sine.md)

*Time series*

- For a time series of salinity, you must create a csv input file (with semicolon as the separator) with 3 columns, defining a time step (in seconds) and salinity (in kg/kg) on the left (i.e. at min_x) and right (i.e. at max_x) boundary at that time step. 
- For intermediate time steps with no defined salinity, values will be linearly interpolated.
- *Note:* the first row of the input file will be skipped and should be used for headers.  

Examples:
    
Option (i): constant salinity of 35 ppt across the model domain
```xml
<belowground>
    <type> FixedSalinity </type>
    <min_x>0</min_x>
    <max_x>22</max_x>
    <salinity>0.035 0.035</salinity>
</belowground>
```
*or*
```xml
<belowground>
    <type> FixedSalinity </type>
    <min_x>0</min_x>
    <max_x>22</max_x>
    <salinity>35*10**-3 35*10**-3</salinity>
</belowground>
```

Option (ii): increasing gradient of salinity from 25 to 35 ppt (left to right border)
```xml
<salinity> 0.025 0.035 </salinity>
```

Option (iii): time series of salinity 
```xml
<salinity> test/SmallTests/inputFiles/salinity_A.csv </salinity>
```

Example csv file:
```json
t_step;salinity_1;salinity_2
0;0.010;0.020
1000000;0.011;0.021
2000000;0.012;0.022    
```

Example sine function:
```xml
<sine>
    <amplitude>10/10**3</amplitude>
    <offset>np.pi/2</offset>
    <stretch>3600*24*365/2/np.pi</stretch>
    <deviation>1/10**3</deviation>
</sine>
```
*or*
```xml
<sine>
    <amplitude>0.01</amplitude>
    <offset>1.57</offset>
    <stretch>5019110</stretch>
    <deviation>0.001</deviation>
</sine>
```
