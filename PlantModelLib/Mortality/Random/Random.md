The Random mortality concept.

In Random, a plant dies with a defined annual mortality probability. 
If a random number times the number of time steps per year is less than this defined probability, the plant dies. 
Values for *Avicennia germinans* and *Rhizophora mangle* can be found, e.g., in Berger & Hildenbrandt (2000).

In this concept, a plant does not die for mechanistic reasons. 
It is useful to combine Random with NoGrowth or Memory.

Attributes:
    mortality (string): "Random"
    probability (float): annual mortality probability. Default: 0.0016.

Examples:
    ```xml
    <plant_dynamics>
        <type> Bettina </type>
        <mortality>Random</mortality>
        <probability>0.0016 </probability>
    </plant_dynamics>
    ```

