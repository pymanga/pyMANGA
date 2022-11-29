---
title: "pyMANGA Module Benchmarks"
linkTitle: "Module Benchmarks"
weight: 4
description:
---
# pyMANGA Module Benchmarks

To test and verify modules in pyMANGA, we define a structure to create benchmarks. 
Those benchmarks should allow (i) to technical assess the functionality of pyMANGA modules, e.g. after code updates and (ii) to test and compare pyMANGA outputs with other module implementations, e.g. with NetLogo models.
Thus, each contributor is kindly asked to provide a benchmark for each proposed module.
In the following we explain the benchmark structure.

As a reference we define a pyMANGA standard tree, which is an individual BETTINA tree, growing without competition or resource limitation (<a href="/docs/Benchmarks/#Figure_1">Figure 1a</a>).
The output metrics of each benchmark are the tree geometry parameters, i.e. stem height, crown, root and stem radius (<a href="/docs/Benchmarks/#Figure_1">Figure 1b</a>).
Additional outputs relevant for the tested module might be specified.

<figure class="alert">
    <img id="Figure_1" src="/pictures/benchmarks/reference_tree.jpg">
    <figcaption>
        <i><br><strong>Figure 1:</strong> (a) Module combination to create the pyMANGA reference tree (T<sup>0</sup>). (b) Geometry of T<sup>0</sup> over time.</i>
    </figcaption>
</figure><p>

Benchmarks are classified based on the compartment of the module tested, i.e. below-ground interaction, above-ground interaction and tree mortality (for now tree growth is always simulated using the BETTINA approach). 
Modules of the other compartments are defined as for the reference tree  (<a href="/docs/Benchmarks/#Figure_2">Figure 2a</a>). 
This means, for example, to test the below-ground module ‘FixedSalinity’, above-ground interaction is disabled (SimpleTest).

The general structure of each benchmark is a 2-tree setup, without recruitment (<a href="/docs/Benchmarks/#Figure_2">Figure 2b</a>).
The trees are placed centered in a 22x22 m model domain with a fixed distance of 2 m. 
The initialization of those trees is based on the geometry of the reference tree. 
The initial population is designed in a way that the respective geometry triggers a potentially critical situation of the concept. 
In some below-ground modules, this is for example the case, when the root systems of the trees overlap.
Thus, we defined an initial population for each compartment ([Table_1](#Table_1)). 
Each initial population is stored in ‘Benchmarks/ModuleTests/<compartment>/’.

<a name="Table_1"></a> _**Table 1** Initial population based on reference tree._

| Compartment | Tree              | Year  | r_stem | h_stem | r_crown | r_root |
|--------------|-------------------|-------|--------|--------|---------|--------|
| Above-ground | T1 | 14.1  | 0.06   | 4.51   | 1.5     | 0.93   |
| Above-ground | T2 | 3.33  | 0.01   | 1.98   | 0.5     | 0.31   |
| Below-ground | T1 | 26.68 | 0.11   | 5.97   | 2.43    | 1.5    |
| Below-ground | T2 | 6.59  | 0.02   | 3.04   | 0.81    | 0.5    |


If land- and seaward boundary conditions need to be defined in a setup, salinity is set to 25 ppt at the landward boundary and to 35 ppt at the seaward boundary. 
Random seed of all setups is 643879.


Time step length is 1e6 seconds (~12 days) and simulation time is 5e8 secs (~ 15.8 years, i.e. 500 time steps).
Output is written after the first and last time step. 
The first is used for automatic testing.

<figure class="alert">
     <img id="Figure_2" src="/pictures/benchmarks/basic_setup.jpg">
     <figcaption>
        <i><br><strong>Figure 2:</strong> (a) Overview below-ground interaction setups. (b) Schematic representation of benchmark setup (based on Bathmann et al. 2020).</i>
     </figcaption>
</figure>

The following files must be provided for each benchmark
- pyMANGA project file
- Results csv file (`<output_times> [2e6, 5e8] </output_times>`)
- All files required to run the setup, e.g. OGS project file (if applicable)
 
The files are stored in 'Benchmarks/ModuleBenchmarks/' with the name of the module tested.

## Overview existing benchmarks

### Modules tested with SimpleBettina

| Below-ground | Above-ground | Mortality |
| --- | --- |:----------------------------------------------------------- |
| &#x2611; FixedSalinity            | &#x2611; SimpleAsymmetricZOI | &#x2611; Random |
| &#x2610; FON                      |               | &#x2611; RandomGrowth* |
| &#x2610; OGSLargeScale            |               | &#x2611; Memory |
| &#x2610; OGSLargeScaleExternal   |               | &#x2611; NoGrowth |
| &#x2611; SymmetricZOI             |               |  |
| &#x2611; SZoiFixedSalinity        |               |  |

_* Parameter 'k_die' set extremely low in order to force trees to die_

### Modules tested with NetworkBettina

Network modules enable the formation of groups, representing root grafted trees.
Grafted trees can exchange water, based on the water potential gradient between them.

The module describing the group formation as well as the water exchange is 'SimpleNetwork'.
All other below-ground network modules are children of this module and one or two other existing below-ground modules allowing for example the definition of a salinity gradient ('NetworkFixedSalinity').
Network below-ground modules must be combined with the growth module 'NetworkBettina' which is based on 'SimpleBettina' but describes resource allocation to form the root graft.


| Below-ground | 
| --- | 
| &#x2611; SimpleNetwork            | 
| &#x2611; NetworkFixedSalinity     | 
| &#x2610; NetworkOGSLargeScale     | 
| &#x2610; NetworkOGSLargeScaleExternal    |  


### Modules tested with SimpleKiwi

In SimpleKiwi, crown and root radius do not grow during the simulation as tree size is a function of dbh.
Hence, we do not test below- and above-ground concepts, which depend on crown and root radius as the competition behavior would not change over time.

| Below-ground | 
| --- | 
| &#x2610; FixedSalinity            |  
| &#x2610; FON                      |  
| &#x2610; OGSLargeScale            | 
| &#x2610; OGSLargeScaleExternal    |

