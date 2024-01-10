Population module that defines the position and size of the initial plant population.

Initial plant population is defined in a csv-file (coma-separated).
This file needs to contain the x,y-position of each individual (i.e., plant unit) and their geometry (i.e., size).
The parameters describing a plant's geometry depend on the chosen plant module (`pyMANGA.PlantModelLib`).

Attributes:
    type (string): "Random"
    domain (nesting tag): coordinates to define the model domain (grid)
    x_1 (domain-nested int): x-coordinate of left border of the grid    
    y_1 (domain-nested int): y-coordinate of bottom border of the grid
    x_2 (domain-nested int): x-coordinate of right border of the grid
    y_2 (domain-nested int): y-coordinate of top border of the grid
    n_recruitment_per_step (integer): number of new individuals (i.e., plant units) added in each time step
    filename (string): path to input file (csv)

Examples:
    - project file (xml)
    ````xml
    <distribution>
        <type> FromFile </type>
        <domain>
            <x_1> 0 </x_1>
            <y_1> 0 </y_1>
            <x_2> 22 </x_2>
            <y_2> 22 </y_2>
        </domain>
        <n_recruitment_per_step> 0 </n_recruitment_per_step>
        <filename> Benchmarks/ModuleBenchmarks/PlantModules/Bettina/ag_initial_population.csv </filename>
    </distribution>
    ````
    - input initial population (csv) suitable for `pyMANGA.PlantModelLib.Bettina`
    ````csv    
    plant,x,y,r_stem,h_stem,r_crown,r_root
    Initial_000000001,10,11,0.0578281884412867,4.51153085664295,1.50012328699222,0.926942149712091
    Initial_000000002,12,11,0.0123232096587272,1.9776990151532,0.499186547499313,0.308854210975212
    ````
