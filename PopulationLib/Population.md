# Description

Library of population modules.

A population consists of one or more groups, which in turn consist of individuals.
These groups may or may not be of different species.

For each group, separate growth, mortality and establishment modules can be defined.
The establishment process is divided in three parts:
- definition of the initial population (see ``pyMANGA.PopulationLib.InitialPop``)
- seed or seedling production (see ``pyMANGA.PopulationLib.Production``)
- seed or seedling dispersal (see ``pyMANGA.PopulationLib.Dispersal``)

```mermaid
flowchart TB;
    id1[[InitialPop]]-->Random;
    id1[[InitialPop]]-->...;
    id2[[Production]]-->FixedRate;
    id2[[Production]]-->....;
    id3[[Dispersal]]-->Uniform;
    id3[[Dispersal]]-->..;
```


# Usage

```xml
<population>
    <group>
        <name> Group_B </name>
        <species> Rhizophora </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>NoGrowth</mortality>
        <domain>
            <x_1> 0 </x_1>
            <y_1> 0 </y_1>
            <x_2> 22 </x_2>
            <y_2> 22 </y_2>
        </domain>
        <initial_population>
            <type>Random</type>
            <n_individuals> 1 </n_individuals>
        </initial_population>
        <production>
            <type>FixedRate</type>
            <per_individual>False</per_individual>
            <per_ha>False</per_ha>
            <n_individuals> 1 </n_individuals>
        </production>
        <dispersal>
            <type> Uniform </type>
        </dispersal>
    </group>
</population>
```

# Attributes

- ``group`` (string): Nesting tag to define a group
- ``name`` (string): Name of the group (can be chosen freely and does not affect the simulation)
- ``species`` (string): see ``pyMANGA.PopulationLib.Species``
- ``vegetation_model_type`` (string): see ``pyMANGA.PlantModelLib``
- ``mortality`` (string): see ``pyMANGA.PlantModelLib.Mortality``
- ``domain`` (nesting-tag): coordinates to define the model domain (as mesh)
    - ``x_1`` (float): x-coordinate of left bottom border of grid
    - ``x_2`` (float): x-coordinate of right bottom border of grid
    - ``y_1`` (float): x-coordinate of left top border of grid
    - ``y_2`` (float): x-coordinate of right top border of grid
- ``initial_population`` (nesting-tag): Defines initial population of a group, see ``pyMANGA.PopulationLib.InitialPop``
- ``production`` (nesting-tag): Defines seed or seedling production of a group, see ``pyMANGA.PopulationLib.Production``
- ``dispersal`` (nesting-tag): Defines seed or seedling dispersal of a group, see ``pyMANGA.PopulationLib.Dispersal``


# Value

An array containing separate dictionaries for each group.

# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.PopulationLib.Species``, ``pyMANGA.PlantModelLib``, ``pyMANGA.PlantModelLib.Mortality``, 
``pyMANGA.PopulationLib.InitialPop``, ``pyMANGA.PopulationLib.Production``, ``pyMANGA.PopulationLib.Dispersal``


# Examples

Two species (groups), Avicennia and Rhizophora, grow in a model domain of 22x22m.
Tree growth follows the Bettina approach. 
Species parameters and annual mortality are different.
Avicennia starts with 50 trees and 2 new trees are recruited in each time step per existing Acivennia tree, while Rhizophora starts with 20 trees and 8 are recruited in each time step.

```xml
<population>
    <group>
        <name> Group_A </name>
        <species> Avicennia </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>NoGrowth Random</mortality>
        <probability>0.0016</probability>
        <domain>
            <x_1> 0 </x_1>
            <y_1> 0 </y_1>
            <x_2> 22 </x_2>
            <y_2> 10 </y_2>
        </domain>
        <initial_population>
            <type>Random</type>
            <n_individuals> 50 </n_individuals>
        </initial_population>
        <production>
            <type>FixedRate</type>
            <per_individual>True</per_individual>
            <per_ha>False</per_ha>
            <n_individuals> 2 </n_individuals>
        </production>
        <dispersal>
            <type> Uniform </type>
        </dispersal>
    </group>
    <group>
        <name> Group_B </name>
        <species> Rhizophora </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>NoGrowth Random</mortality>
        <probability>0.001</probability>
        <domain>
            <x_1> 0 </x_1>
            <y_1> 0 </y_1>
            <x_2> 22 </x_2>
            <y_2> 10 </y_2>
        </domain>
        <initial_population>
            <type>Random</type>
            <n_individuals> 20 </n_individuals>
        </initial_population>
        <production>
            <type>FixedRate</type>
            <per_individual>True</per_individual>
            <per_ha>False</per_ha>
            <n_individuals> 8 </n_individuals>
        </production>
        <dispersal>
            <type> Uniform </type>
        </dispersal>
    </group>
</population>
```
