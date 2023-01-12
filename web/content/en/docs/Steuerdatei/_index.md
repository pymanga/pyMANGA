---
title: "Control File"
linkTitle: "Control File"
weight: 2
description:
---

The control file of each pyMANGA setup is written in _xml_ format.
This file includes all settings for to run pyMANGA.
In the following, each section of the control file is explained using of the model setup "Full Model" as an example.
This model is a coupled consideration of the groundwater balance and plant growth.
Thus, both the influence of tidal dynamics and the relationship between plant water use and salinity in pore water are considered.
This model is presented <a href="/docs/example_ogs_bettina/" target="_blank">here</a> in more detail.
The control file can be found <a href="https://github.com/jbathmann/pyMANGA/blob/master/Benchmarks/ExampleSetups/ExmouthGulf/setup_pymanga.xml" target="_blank">here</a>.


The control file describes the settings for each pyMANGA library (see
<a href="/contribution/structure/" target="_blank">pyMANAGA structure</a> for more detail), namely
- [tree_dynamics](/docs/steuerdatei/#tree_dynamics)
- [initial_population](/docs/steuerdatei/#initial_population)
- [tree_time_loop](/docs/steuerdatei/#tree_time_loop)
- [visualization](/docs/steuerdatei/#visualization)
- [tree_output](/docs/steuerdatei/#tree_output)

The documentation of all control file input can be found <a href="https://jbathmann.github.io/pyMANGA/" target="_blank">here</a>.
## ``tree_dynamics``

Under the item "tree_dynamics" settings for the dynamic development of the tree population are listed.

### ``aboveground_competition``

This sub-item characterizes the modeling of resource availability over the ground.

Since pyMANGA vegetation growth is a function of resources availability, these are the focus of this sub-item.
The above-ground resource relevant to pyMANGA represents the sunlight. 

With the item, `type`, the type of the above-ground competition concept is defined.
In our example, we use "SimpleAsymmetricZOI".

In this concept, the model area is divided into zones in which the tree with the largest crown height in each cell receives all available sunlight.
The class requires the input variables defined under the next item `domain`, namely `y_1`, `y_2`, `x_1` and `x_2`.
They define the boundaries of the model domain.
The coordinate values with the indices "1" define the numerically lower values, the indices "2" the numerically higher ones.
`x_resolution` and `y_resolution` define the spatial discretization of the model domain with the number of grid nodes in the respective spatial direction.

```
<aboveground_competition>
    <type> SimpleAsymmetricZOI </type>
    <domain>
        <x_1> 0 </x_1>
        <y_1> 0 </y_1>
        <x_2> 185 </x_2>
        <y_2> 10 </y_2>
    <x_resolution> 720 </x_resolution>
    <y_resolution> 38 </y_resolution>
    </domain>
</aboveground_competition>
```

Currently, there is only one other `type`: "SimpleTest".
This type means there is no limitation in resource availability.
It's thus not suitable for modeling real vegetation populations.

Links:
- [Source code 'SimpleAsymmetricZOI'](https://github.com/jbathmann/pyMANGA/blob/master/TreeModelLib/AbovegroundCompetition/SimpleAsymmetricZOI/SimpleAsymmetricZOI.py)
- [Documentation 'SimpleAsymmetricZOI'](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__tree_dynamics__aboveground_competition__SimpleAsymmetricZOI__SimpleAsymmetricZOI.html)

### `belowground_competition`

This sub-item characterizes the modeling of resource availability below the ground.

In this setup, the class "OGSLargeScale3D" is used (sub-item `type`), which is designed for modeling the change in salinity in the pore water using a more complex groundwater model. 

In the sub-item `ogs_project_folder`, the file path of the OGS input files is defined, in the next step the name of the OGS control file (`ogs_project_folder`).

In the item `abiotic_drivers`, the salinity of the seawater (or in general of the salt water), the period of the monthly and daily tide and the amplitude of the monthly and daily tide can be defined.
In this control file, only the value for the salinity is defined, the values for the tidal range are read in via python_script (see end of this section).

With `delta_t_ogs` the numerical groundwater modeling with OGS is discretized in time.
This variable can also be used to fix numerical instabilities or to minimize the computation time.

In the item `source_mesh` the name of the grid file for the OGS model is named.
This file defines the spatial discretization of the groundwater model using a vtu file.

In the last sub-item, `python_script`, a Python file can be specified in which boundary conditions and source terms for the OGS model are defined.
This specification is optional; the necessity depends on the complexity of the groundwater model.

In this model, the file provides a loop of the tidal range information read from the EXM_Jan-Jul_2019.txt file and a dynamic adjustment of the mean water level.

```
<belowground_competition>
    <type> OGSLargeScale3D </type>
    <ogs_project_folder> /your/path/to/pyMANGA/Benchmarks/Exmouth_Gulf/full_model </ogs_project_folder>
    <ogs_project_file> testmodel.prj </ogs_project_file>
    <abiotic_drivers>
        <seaward_salinity> 0.05 </seaward_salinity>
    </abiotic_drivers>
    <delta_t_ogs> 1500000 </delta_t_ogs>
    <source_mesh> source_domain.vtu </source_mesh>
    <!--bulk_mesh> testbulk.vtu </bulk_mesh-->
    <!--use_old_ogs_results>True</use_old_ogs_results-->
    <python_script>python_script.py</python_script>
</belowground_competition>
```

Links:
- [Source code 'OGSLargeScale3D'](https://github.com/jbathmann/pyMANGA/blob/master/TreeModelLib/BelowgroundCompetition/OGSLargeScale3D/OGSLargeScale3D.py)  
- [Documentation 'OGSLargeScale3D'](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__tree_dynamics__belowground_competition__OGSLargeScale3D__OGSLargeScale3D.html)

### `tree_growth_and_death`

The third and last main item of the ``tree_dynamics`` section, defines the dynamic concept of tree growth and death.
In our example, we use the "SimpleBettina" concept.
For more information, see this <a href="https://doi.org/10.1016/j.ecolmodel.2018.10.005" target="_blank">publication</a>.
The concept does not need any further parameters.

```
<tree_growth_and_death>
    <type> SimpleBettina </type>
</tree_growth_and_death>
```
If nothing else is defined, tree die of mechanistic reasons, i.e. when maintenance cost are higher than resource uptake.
The mortality concept can be changed by adding the sub-item ``mortality`` and the parameters required for the concept.

```
<tree_growth_and_death>
    <type> SimpleBettina </type>
    <mortality>RandomGrowth</mortality>
    <k_die> 1e-9 </k_die>
</tree_growth_and_death>
```

Links:
- [Source code 'SimpleBettina'](https://github.com/jbathmann/pyMANGA/blob/master/TreeModelLib/GrowthAndDeathDynamics/SimpleBettina/SimpleBettina.py)  
- [Documentation 'SimpleBettina'](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__tree_dynamics__tree_growth_and_death__SimpleBettina__SimpleBettina.html)


## ``initial_population``

This section defines the tree population at the beginning of the modeling period (initial conditions) and the recruitment of trees at each time step.

A group of trees to be added to the model is defined in the ``group`` element.
For example, trees that should be present in the model domain at the beginning of simulation can be defined as one group and those that should be added as new trees at each time step can be defined in another group.
In this setup, there are exactly these two groups.

The item `species` specifies the type of trees.
Currently, only the gray mangrove (Avicennia marina) with the class "Avicennia " is selectable.
If a path is provided for this sub-item, the user can provide an individual species file where all required attributes need to be defined.
To see which attributes are required, please check the default file for <a href="https://github.com/jbathmann/pyMANGA/blob/master/PopulationLib/Species/Avicennia.py" target="_blank">Avicennia</a>.

Under ``distribution`` the distribution of the trees, i.e. the spatial arrangement in the model area, is determined.
Under ``type`` this can either be read from a file with "GroupFromFile" or - as in this setup - randomly arranged with "random".
Under ``domain`` the model domain is defined.
The coordinate values with the indices "1" define the numerically lower values, the indices "2" the numerically higher ones.
With ``n_individuals`` the number of trees can be defined, which should be present in the model at the beginning of the modeling and with `n_recruitment_per_step` the number of trees, which should be added to the model at each time step as young trees.
The properties of the recruited trees correspond to those defined in the species file.

In the "Recruiting" group, ``n_individuals`` is set to zero, and "n_recruitment_per_step" is set to 30.
This shows that this first group is used to integrate new trees over the entire model runtime.
Since ``n_individuals`` must be specified, but `n_recruitment_per_step` is optional, only `n_individuals` is specified as 30 in the second group "Inital".
So, at the beginning of the simulation, there should be 30 trees randomly distributed in the model domain and we each time step, 30 new trees are recruited.

```
<initial_population>
    <group>
        <name> Recruiting </name>
        <species> /your/path/to/pyMANGA/Benchmarks/Exmouth_Gulf/full_model/Avicennia.py </species>
        <distribution>
            <type> Random </type>
            <domain>
                <x_1> 0 </x_1>
                <y_1> 0 </y_1>
                <x_2> 185 </x_2>
                <y_2> 10 </y_2>
            </domain>
            <n_individuals> 0 </n_individuals>
            <n_recruitment_per_step> 30 </n_recruitment_per_step>
        </distribution>
    </group>
</initial_population>
```

Links:
- [Documentation 'initial population'](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__initial_population__group__group.html)

## ``tree_time_loop``

Here the model is discretized in time.

Currently, only "Simple" is available for `type`.
That is, all time steps are of the same size over the entire simulation.
The start time (`t_start`), end time (`t_end`) and the time step length (`delta_t`) must be specified in seconds.

````
<tree_time_loop>
    <type> Simple </type>
    <t_start> 0 </t_start>
    <t_end> 157788000000 </t_end>
    <delta_t> 15778800 </delta_t>
</tree_time_loop>
````

## ``visualization``

In this setup, visualization of the simulation during the model run is switched off.
For this purpose, "NONE" is selected for the ``type`` item.
With "SimplePyplot" the position and the crown radius of trees would be visualized in real time during simulation.

```
<visualization>
    <type> NONE </type>
</visualization>
```

## ``tree_output``

The last section, defines how model results are saved.

For this there are three different possibilities which are specified under `case`: 
- "NONE" saves no results
- "OneTimestepOneFile" creates one file for each time step with the tree population 
- "OneTreeOneFile" creates a separate file for each tree but with all time steps
- "OneFile" creates one file with all trees and time steps

The file path is specified under `output_dir`.
The directory must exist.
If `allow_previous_output` is True, existing files are overwritten.
If it is false (default) and the directory is not empty, the simulation will not start.

With the items ``geometry_output`` geometric dimensions can be added to the output file.
The variables selected in this setup are "r_stem" (stem radius), "h_stem" (stem height), "r_crown" (crown height) and "r_root" (root radius).
With the item ``growth_output`` information from the tree growth concept can be saved.
Other optional output options can be found in the <a href="https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__tree_output__tree_output.html" target="_blank">documentation</a>.

````
<tree_output>
    <type> OneTimestepOneFile </type>
    <output_each_nth_timestep> 1 </output_each_nth_timestep>
    <output_dir> /your/path/to/pyMANGA/Benchmarks/Exmouth_Gulf/full_model/TreeOutput </output_dir>
    <geometry_output> r_stem </geometry_output>
    <geometry_output> h_stem </geometry_output>
    <geometry_output> r_crown </geometry_output>
    <geometry_output> r_root </geometry_output>
    <growth_output> salinity </growth_output>
</tree_output>
````