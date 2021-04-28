---
title: "Control File"
linkTitle: "Control File"
weight: 2
description:
---
The control file of each pyMANGA setup is written in xml format, here are all settings for modeling made.
In the following, the control file of the model setup "Full Model" is described as an example.
This model is a coupled consideration of the groundwater balance and plant growth.
Thus, both the influence of tidal dynamics and the relationship between plant water use and salinity in pore water are considered.
For more information on this model, read <a href="/en/docs/sample_model_exmouth_gulf/">this section</a> in the documentation, which describes the setup in more detail.

## tree_dynamics

Under the item "tree_dynamics" settings for the dynamic development of the tree population are listed.

### aboveground_competition

This subitem characterizes the modeling of tree growth over the ground.
Since pyMANGA models growth via the presence of resources, these are also the focus of this subitem.
The above-ground resource relevant to pyMANGA represents the sunlight. The first item, "type", defines the default setting as the type "SimpleAsymmetricZOI".
These settings are located in the source code of the program at ./TreeModelLib/AbovegroundCompetition/SimpleAsymmetricZOI".
With this basic setting, the model area is divided into zones in which the tree with the largest crown height in each case receives all available sunlight.
The class requires the input variables defined under the next item "domain".
"y_1", "y_2, "x_1" and "x_2" define the boundaries of the model domain.
The coordinate values with the indices "1" define the numerically lower values, the indices "2" the numerically higher ones.
"x_resolution" and "y_resolution" define the spatial discretization of the model domain with the number of grid nodes in the respective spatial direction.

Currently there is another class for "type", "SimpleTest".
This is to be used for example setups and to check the correct calculation of setups and is not suitable for modeling real mangrove populations.

### belowground_competition

In addition to the aboveground resources, pyMANGA also takes into account the belowground resources available for the trees.
In the item "belowground_competion" the settings for this are made in the control file, for which five different classes are available.
In the source code these can be found under "./TreeModelLib/BelowgroundCompetition".
In this setup, the class "OGSLargeScale3D" is used (subitem "type"), which is designed for modeling the change in salinity in the pore water using a more complex groundwater model. 

In the subitem "ogs_project_folder" the file path of the OGS input files is defined, in the next step the name of the OGS control file ("ogs_project_file").

In the item "abiotic drivers" the salinity of the sea water (or in general of the salt water), the period of the monthly and daily tide and the amplitude of the monthly and daily tide can be defined.
In this control file only the value for the salinity is defined, the values for the tidal range are read in via python_script (see at the end of this section).

With "delta_t_ogs" the numerical groundwater modeling with OGS is discretized in time.
This variable can also be used to fix numerical instabilities or to minimize the computation time.

In the item "source_mesh" the name of the grid file for the OGS model is named.
This file defines the spatial discretization of the groundwater model using a vtu file.

In the last subitem, "python_script", a Python file can be specified in which boundary conditions and source terms for the OGS model are defined.
This specification is optional; the necessity depends on the complexity of the groundwater model.
In this model, the file provides a loop of the tidal range information read from the EXM_Jan-Jul_2019.txt file and a dynamic adjustment of the mean water level.

### tree_growth_and_death

In the third and last main item of the "tree_dynamics" section, the dynamic concept of tree growth and death can be selected.
There are three available for this, "SimpleKiwi", "SimpleTest" and "SimpleBettina". With the "SimpleBettina" concept used in this setup, the "Kiwi single tree model" is used to model the dynamic evolution of the tree population.
For more information, see this <a href="https://doi.org/10.1016/j.ecolmodel.2018.10.005"> publication</a> In source code, the three concepts can be found at "./TreeModelLib/GrowthAndDeathDynamics/".

At this point, the "tree_dynamics" section is over.

## initial_population

This section defines the tree population at the beginning of the modeling period (IC) and the new addition of trees at each time step.


A group of trees to be added to the model is defined in the "group" element.
For example, the trees that should be present in the model domain at the beginning of modeling can be defined as one group and those that should be added as new trees at each time step can be defined in another group.
In this setup, there are exactly these two groups.

The item "species" specifies the type of trees.
Currently only the gray mangrove (Avicennia marina) with the class "avicennia" is selectable.

Under "distribution" the distribution of the trees, i.e. the spatial arrangement in the model area, is determined.
Under "type" this can either be read from a file with "GroupFromFile" or - as in this setup - randomly arranged with "random".
Under "domain" the model domain is defined.
The coordinate values with the indices "1" define the numerically lower values, the indices "2" the numerically higher ones.
With "n_individuals" the number of trees can be defined, which should be present in the model at the beginning of the modeling and with "n_recruitment_per_step" the number of trees, which should be added to the model at each time step as young trees.
In the "Recruiting" group, "n_individuals" is set to zero, and "n_recruitment_per_step" is set to 30.
This shows that this first group is used to integrate new trees over the entire model runtime.
Since "n_individuals" must be specified, but "n_recruitment_per_step" is optional, only "n_individuals" is specified as 30 in the second group "Inital".
So, at the beginning of the modeling there should be 30 trees randomly distributed in the model domain.

In the source code, the files required for modeling the addition of new trees to the model can be found under "./PopulationLib".

## tree_time_loop

Here the model is discretized in time.

Currently, only "simple" is available for "type".
Here, all time steps are of the same size over the entire modeling.
The start time ("t_start"), end time ("t_end") and the time step length ("delta_t") must be specified.

## visualization

In this setup, visualization of the modeling during a model run is switched off.
For this purpose, "NONE" is selected for the "type" item.
With "SimplePyplot" the position and the crown radius of trees would be visualized in real time during modeling using matplotlib.

## tree_output

In the last section the saving of the model results is defined.

For this there are three different possibilities which are specified under "case": "NONE" saves no results, with "OneTimestepOneFile" a file with the tree population is saved per time step and with "OneTreeOneFile" a separate file is saved for each tree present in the model.
The file path is specified under "output_dir".
This must be present and empty, otherwise the modeling will not start.
With the items "geometry_output" geometric dimensions can be added to the output file.
The variables selected in this setup are "r_stem" (stem radius), "h_stem" (stem height), "r_crown" (crown height) and "r_root" (root radius).
With the last item "growth_output" information from the tree growth concept can be output.
All information that can be added to the output file can be viewed under ./TreeModelLib/GrowthAndDeathDynamics/SimpleBettina/SimpleBettina.py line 35 ff.
