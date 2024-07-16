# Description

Library of population modules.

A population consists of one or more groups, which in turn consist of individuals.
These groups may or may not be of different species.

For each group, separate growth, mortality and dispersal modules can be defined.

# Usage

```xml
<population>
    <group>
        <name> Group_B </name>
        <species> Rhizophora </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>NoGrowth</mortality>
        <distribution>
            <type> Random </type>
            <domain>
                <x_1> 0 </x_1>
                <y_1> 0 </y_1>
                <x_2> 22 </x_2>
                <y_2> 22 </y_2>
            </domain>
            <n_individuals> 50 </n_individuals>
            <n_recruitment_per_step> 10 </n_recruitment_per_step>
        </distribution>
    </group>
</population>
```

# Attributes

- ``group`` (string): Nesting tag to define a group
- ``name`` (string): Name of the group (can be chosen freely and does not affect the simulation)
- ``species`` (string): see ``pyMANGA.PopulationLib.Species``
- ``vegetation_model_type`` (string): see ``pyMANGA.PlantModelLib``
- ``mortality`` (string): see ``pyMANGA.PlantModelLib.Mortality``
- ``distribution`` (string): see ``pyMANGA.PopulationLib.Dispersal``

# Value

An array containing separate dictionaries for each group.

# Author(s)

Marie-Christin Wimmler

# See Also

``pyMANGA.PopulationLib.Species``, ``pyMANGA.PlantModelLib``, ``pyMANGA.PlantModelLib.Mortality``, 
``pyMANGA.PopulationLib.Dispersal``


# Examples

Two species (groups), Avicennia and Rhizophora, grow in a model domain of 22x22m.
Tree growth follows the Bettina approach. 
Species parameters and annual mortality are different.
Avicennia starts with 50 trees and 10 new trees are recruited in each time step, while Rhizophora starts with 20 trees and 8 are recruited in each time step.

```xml
<population>
    <group>
        <name> Group_A </name>
        <species> Avicennia </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>NoGrowth Random</mortality>
        <probability>0.0016</probability>
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
    </group>
    <group>
        <name> Group_B </name>
        <species> Rhizophora </species>
        <vegetation_model_type> Bettina </vegetation_model_type>
        <mortality>NoGrowth Random</mortality>
        <probability>0.001</probability>
        <distribution>
            <type> Random </type>
            <weight_file>weight_map_Rhi.csv</weight_file>
            <domain>
                <x_1> 0 </x_1>
                <y_1> 0 </y_1>
                <x_2> 22 </x_2>
                <y_2> 22 </y_2>
            </domain>
            <n_individuals> 20 </n_individuals>
            <n_recruitment_per_step> 8 </n_recruitment_per_step>
        </distribution>
    </group>
</population>
```
