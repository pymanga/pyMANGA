Population module that defines the position of initial and new seeds.

New seeds are randomly distributed within the model domain.
The number of seeds is the same at each time step.

Attributes:
    type (string): "Random"
    domain (nesting tag): coordinates to define the model domain (grid)
    x_1 (domain-nested int): x-coordinate of left border of the grid    
    y_1 (domain-nested int): y-coordinate of bottom border of the grid
    x_2 (domain-nested int): x-coordinate of right border of the grid
    y_2 (domain-nested int): y-coordinate of top border of the grid
    n_individuals (integer): number of individuals (i.e., plant units) during model initialization
    n_recruitment_per_step (integer): number of new individuals (i.e., plant units) added in each time step

Examples:

    ````xml
    <distribution>
        <type> Random </type>
        <domain>
            <x_1> 0 </x_1>
            <y_1> 0 </y_1>
            <x_2> 22 </x_2>
            <y_2> 22 </y_2>
        </domain>
        <n_individuals> 10 </n_individuals>
        <n_recruitment_per_step> 0 </n_recruitment_per_step>
    </distribution>
    ````