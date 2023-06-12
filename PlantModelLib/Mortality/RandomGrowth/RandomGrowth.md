The RandomGrowth mortality concept.

In RandomGrowth, a plant dies with a biomass-dependent probability. 
If a random number falls below this defined probability, the plant dies. 
This probability is a function of the relative biomass increment per time step and a calibration factor k_die. 
As the relative biomass increment decreases over time, the probability of dying increases.

In this approach, a plant dies for semi-mechanistic reasons.

Attributes:
    mortality (string): "RandomGrowth"
    k_die (float): calibration factor. Default: 1e-12.

Examples:
    ```xml
    <plant_dynamics>
        <type> Bettina </type>
        <mortality>RandomGrowth</mortality>
        <k_die> 1e-9 </k_die>
    </plant_dynamics>
    ```

Notes:
    See the pymanga sensitivity repository for an analysis of the effect of k_die.  
    <a href="https://github.com/pymanga/sensitivity/blob/main/PlantModels/Mortality/RandomGrowth/RandomGrowth.md" target="_blank">Go to analysis</a>
