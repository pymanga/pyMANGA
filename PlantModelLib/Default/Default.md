The Default plant model concept. 

With this concept plants do no grow or die at all.

Note:
    This module can also be used to monitor below- and above-ground resources within the model domain by configuring an additional plant group where all plants are of size 0.
    The resources available in a given position can then be calculated backwards.
    In combination with `pyMANGA.ResourceLib.BelowGround.Individual.FixedSalinity`, variant `bettina`, salinity below a plant is calculated as 
    $\frac{\psi_{leaf} * (bg_{factor} - 1)}{8.5e7}$.

Attributes:
    type (string): "Default"

Examples:
    ```xml
    <plant_dynamics>
        <type> Bettina </type>
    </plant_dynamics>
    ```
Possible outputs:
    ```xml
    <output> 
        <growth_output> ag_factor </growth_output>
        <growth_output> bg_factor </growth_output>
    </output>
    ```

