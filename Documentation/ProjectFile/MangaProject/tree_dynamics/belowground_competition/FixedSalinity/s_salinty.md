

There are two ways to indicate the salinity of the bottom water:  
(i) two values, each for the location defined via max_x and min_x (option 1), or  
(ii) a time series with values for these (option 2).

**Option (i)** 

Salinity in kg/kg. e.g. 35 ppt corresponds to 0.035. 
Two values (min and max) need to be specified.

Example:  
*<salinity> 0.005 0.095 </salinity>*

<br>
**Option (ii)**

Path to file containing salinity in kg/kg.
Two values (min and max) need to be specified for each time step you want to define the salinity. 
For time steps with no defined salinity, values will be linearly interpolated.
The input file needs to be a csv file with semicolon as separator and 3 columns, 
defining the time step (in seconds) and salinity on the left and right boundary (in kg/kg).

Note: the first row will be skipped (as we expect the header to be present).
<br>
Example xml-file:

*<salinity> test/SmallTests/inputFiles/salinity_A.csv </salinity>*

Example csv file:

*t_step;salinity_1;salinity_2<br>
0;0.010;0.020<br>
1000000;0.011;0.021<br>
2000000;0.012;0.022<br>*
