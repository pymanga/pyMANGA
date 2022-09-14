---
title: "pyMANGA Module Benchmarks"
linkTitle: "Module Benchmarks"
weight: 4
description:
---

To test and verify modules in MANGA, we define a structure to create benchmarks. 
Those benchmarks should allow (i) to technical assess the functionality of MANGA modules, e.g. after code updates and (ii) to test and compare MANGA outputs with other module implementations, e.g. with NetLogo models.
Thus, each contributor is kindly asked to provide a benchmark for each proposed module.
In the following we explain the benchmark structure.

As a reference we define a MANGA standard tree, which is an individual BETTINA tree, growing without competition or resource limitation (<a href="/docs/Benchmarks/#Figure_1">Figure 1a</a>).
The output metrics of each benchmark are the tree geometry parameters, i.e. stem height, crown, root and stem radius (<a href="/docs/Benchmarks/#Figure_1">Figure 1b</a>).


<figure>
    <a name="Figure_1"></a>
    <img src="/pictures/benchmarks/reference_tree.jpg">
    <figcaption>
        <font size = "1"><i><b>Figure 1:</b> (a) Module combination to create the MANGA reference tree (T0). (b) Geometry of T^0 over time.</i></font>
    </figcaption>
</figure><p>

The general structure of each benchmark is a 2-tree setup, without recruitment (<a href="/docs/Benchmarks/#Figure_2">Figure 2a</a>).
The trees are placed centered in a 22x22 m model domain with a fixed distance of 2 m. 
The initialization of those trees is based on the reference tree. 
The tree on the left is initialized with the geometry of the 5-year-old reference tree while the other tree is initialized as a seedling (0-year reference tree, see ‘Benchmarks/ModuleTests/Standard/initial_population.csv’). 
Time step length is 1e6 seconds (~12 days) and simulation time is 300 years. Each benchmark has a short version with only 2 time steps used in the automatic test of MANGA (starting at 5e9 seconds simulation time). 
If land- and seaward boundary conditions need to be defined in a setup, salinity is set to 25 ppt at the landward boundary and to 35 ppt at the seaward boundary. 
Random seed of all setups is 643879.

Benchmarks are classified based on the compartment of the module tested, i.e. below-ground interaction, above-ground interaction and tree mortality (for now tree growth is always simulated using the BETTINA approach). 
Modules of the other compartments are defined as for the reference tree  (<a href="/docs/Benchmarks/#Figure_2">Figure 2b</a>). 
This means, for example, to test the below-ground module ‘FixedSalinity’, above-ground interaction is disabled (SimpleTest).

<figure>
    <a name="Figure_2"></a>
    <img src="/pictures/benchmarks/basic_setup.jpg">
    <figcaption>
        <font size = "1"><i><b>Figure 2:</b> (a) Schematic representation of benchmark setup (based on Bathmann et al. 2020). (b) Overview below-ground interaction setups.</i></font>
</figcaption>
</figure><p>

The following files must be provided for each benchmark
-	Full benchmark  
     + MANGA project file  
     + Results csv file (output every 10th time step)
     + Optional: other files required to run the setup, e.g. OGS project file 
-	Short benchmark  
     + MANGA project file
     + Initial population (based on geometry in 5e9 s full benchmark)
     + Results csv file 
 
Naming convention
-	Folder to store benchmark: name of tested module
-	File names
     + full setup: \"below_above_growth_mortality"
     + short setup: \"name-full-setup_short"

## Overview existing benchmarks

### Non-network modules (tested with SimpleBettina)

| Below-ground | Above-ground | Mortality |
| --- | --- |:----------------------------------------------------------- |  
| &#x2610; FixedSalinity            | &#x2610; AZOI | &#x2610; Random |
| &#x2610; FON                      |               | &#x2610; RandomGrowth|
| &#x2610; OGSLargeScale            |               | &#x2610; Memory |
| &#x2610; OGSLargeScale External   |               |  |
| &#x2610; SymmetricZOI             |               |  |
| &#x2610; SZoiFixedSalinity        |               |  |

### Network modules (tested with NetworkBettina)

| Below-ground | 
| --- | 
| &#x2610; SimpleNetwork            | 
| &#x2610; NetworkFixedSalinity     | 
| &#x2610; NetworkOGSLargeScale     | 
| &#x2610; NetworkOGSLargeScale External    |  
