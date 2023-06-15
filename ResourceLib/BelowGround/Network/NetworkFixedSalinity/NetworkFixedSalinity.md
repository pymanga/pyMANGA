The NetworkFixedSalinity below-ground resource module.

NetworkFixedSalinity is a child of the modules `pyMANGA.ResourceLib.BelowGround.Network.Network.Network` and 
`pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity.FixedSalinity`.
This means that resource limitation due to pore water salinity is taken into account in the calculation of 
water distribution between root grafted trees.

Attributes:
    type (string): "NetworkFixedSalinity" (module name)
    f_radius (float): proportion of stem radius to set min. radius of grafted roots. Range: 0 to 1.
    min_x (float): x-coordinate of the left border (y-axis)
    max_x (float): x-coordinate of the right border (y-axis)
    salinity (float float or string): either two values representing the salinity (kg/kg) range 
        from min_x (first value) to max_x (second value) <strong>or</strong> the path to a csv file containing a time series of salinity (see description above and 
        example below)


Example:
    ```xml
    <belowground>
        <type> NetworkFixedSalinity </type>
        <f_radius> 0.25 </f_radius>
        <min_x>0</min_x>
        <max_x>22</max_x>
        <salinity>0.025 0.035</salinity>
    </belowground>
    ```
