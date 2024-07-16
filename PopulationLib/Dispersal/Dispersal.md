# Description

Sub-library containing seed (plant) dispersal modules.

# Usage

Dispersal is part of the definition of the population (see ``pyMANGA.PopulationLib``). 

```xml
<distribution>
    <type> Random </type>
    <weight_file>weight_map_Avi.csv</weight_file>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
    </domain>
    <n_individuals> 50 </n_individuals>
    <n_recruitment_per_step> 10 </n_recruitment_per_step>
</distribution>
```

# Attributes

- ``distribution`` (string): Nesting tag to define a group
- ``type`` (string): Name of the selected module to initialize the population
- ``n_recruitment_per_step`` (int): Number of plants recruited in each time step
- ``domain`` (nesting-tag): coordinates to define the model domain (as mesh)
    - ``x_1`` (float): x-coordinate of left bottom border of grid
    - ``x_2`` (float): x-coordinate of right bottom border of grid
    - ``y_1`` (float): x-coordinate of left top border of grid
    - ``y_2`` (float): x-coordinate of right top border of grid
    - ``x_res`` (float): (optional) x-resolution of the grid (see `weighted recruiment`)
    - ``y_res`` (float): (optional) y-resolution of the grid (see `weighted recruiment`)
- ``weight_formula`` (string): (optional) Formula to define the weight factor (accepts Python math notation including Numpy as 'np')
- ``weight_file`` (string): (optional)

# Value

Three dictionaries containing the positions and geometry of plants and networks (if applicable).

# Details
## Purpose

The purpose of this module is to add new plants to the model and assign their initial attributes.

## Process overview

- Initialize distribution type for initial population
- Read tags from project file
- Optional: Create map (grid) with weights indicating suitability for recruitment (see _iniWeightsFormula_ and _iniWeightsFile_)
- Get plant attributes from selected module (see _getPlantAttributes_)

## Sub-processes

New plants are added to the system in each time step.
They are distributed randomly within the defined model domain of the group.
Random distribution is either uniform (default) or weighted (see options below).

### Weighted recruitment

Create map (grid) with weights indicating suitability for recruitment.
The map is initialized at the beginning of the simulation for each plant group.
Weights should range between 0 (not suitable) and 1 (suitable).
Based on the weights the position of a plant is drawn from a weighted uniform distribution (see ``pyMANGA.PopulationLib.Dispersal.Random``).

**Note** If both ``weight_file`` and ``weight_formula`` are specified, only ``weight_file`` will be used.

#### iniWeightsFile

The map is loaded from a csv file.
The file must contain the following column names without quotes: x, y, weight.

Grid cell size is calculated as the average distance between x and y coordinates.

#### iniWeightsFormula

The map is a regular grid based on the description of the model domain.
The cell size (``x_r`` and ``y_r``) is
````python
x_r = 1 / (x_res / l_x)
y_r = 1 / (y_res / l_y)
````

The wighting function (``weight_forumla``) can take x and y arguments as well as numpy function.
Here are some examples

````python
np.sin((x**2+y**2)/10)^4
1/2*(x/np.max(x)+y/np.max(y))
````


### getPlantAttributes

Calls ``getPlantAttributes`` method of selected dispersal module.
Is called by ``PlantGroup``.


## Application & Restrictions

-

# References

-

# Author(s)

Marie-Christin Wimmler, Jasper Bathmann

# See Also

``pyMANGA.PopulationLib.Dispersal.Random``,
``pyMANGA.PopulationLib.Species``

# Examples

Initial population of 50 plants is positioned randomly in a 22x22m model domain.
In each time step, 10 new plants are added.
The probability for their location is based on the provided weight formula.
The grid cells have a size of 0.25x0.33m.

````xml
<distribution>
    <type> Random </type>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 22 </x_2>
        <y_2> 22 </y_2>
        <x_res>88</x_res>
        <y_res>66</y_res>
    </domain>
    <n_individuals> 50 </n_individuals>
    <n_recruitment_per_step> 10 </n_recruitment_per_step>
    <weight_formula>(x/np.max(x) + y/np.max(y))/2</weight_formula>
</distribution>
````
