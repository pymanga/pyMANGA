To test and verify modules in pyMANGA we use benchmarks.
These benchmarks should allow (i) to technically assess the functionality of pyMANGA modules, e.g. after code updates, and (ii) to test and compare pyMANGA results with other module implementations, e.g. with NetLogo models.
Therefore, each contributor is kindly asked to provide a benchmark for the proposed module.
The design and structure of the benchmark differs depending on the library tested.
We distinguish benchmarks for
- plant modules, always tested in combination with resource modules
- population modules
- model output modules

There are two versions of each benchmark, a short one and a long one.
The short one, denoted by '< name>_CI.xml', executes only one timestep and is used for the automated test.

# Benchmark design
## Plant modules

The plant and resource module benchmarks are grouped into sets that belong to a particular plant growth concept (i.e., plant module). 
Each set has a reference plant, which is an individual plant growing with the particular growth concept, but without competition or resource limitation.
The output metrics of each benchmark are the plant geometry parameters available for that plant module, such as stem height, crown, root, and stem radius. 
Additional outputs relevant to the tested module may be specified.

Within a set, benchmarks are classified based on the compartment of the tested module, i.e. below ground interaction, above ground interaction and plant mortality. 
Modules of the other compartments are defined as for the reference plant. 
This means, for example, that to test the below-ground module 'FixedSalinity', above-ground interaction is disabled ('Default') and mortality is mechanistic ('NoGrowth').

The general structure of each benchmark is a 2-plant setup without recruitment.
The position and size of those two plants depends on the plant type (described below).

The following files must be provided for each benchmark

- pyMANGA project file
- Reference files = results as csv file produced with type 'OneTimestepOneFile'
  - the output is only stored for the first and last timestep (<output_times> [first, last] </output_times>)
- All files required to run the setup, e.g. OGS project file (if applicable)

The files are stored in ‘Benchmarks/ModuleBenchmarks/PlantModules/< plant_module>/< compartment>/’ with the name of the module tested.

### Type: tree

The trees are placed in the center of a 22x22m model domain with a fixed distance of 2m.
The initialization of these trees is based on the geometry of the reference plant.
The initial population is designed so that the respective geometry triggers a potentially critical situation of the concept.
For example, in some underground modules this is the case when the root systems of the plants overlap. Therefore, we defined an initial population for each compartment.
Each initial population is stored in 'Benchmarks/ModuleBenchmarks/PlantModules/"plant_module"/"compartment"/'.

If landward and seaward boundary conditions must be defined in a setup, the salinity is set to 25 ppt at the landward boundary and 35 ppt at the seaward boundary.
The random seed for all setups is 643879.

The time step length is 1e6 seconds (~12 days) and the simulation time is 5e8 seconds (~15.8 years, i.e. 500 time steps).
Output is written after the first and last time step. The first output is used for automatic testing.

### Type: marsh plant

The plants are placed in a 2 × 2 m model domain.
The initial population is designed such that the respective plant geometry and spacing trigger a potentially critical situation of the concept to be tested.
For example, in the aboveground benchmark the plants are positioned such that their zones of influence overlap, while in the belowground benchmarks the setup is chosen to induce either root overlap or salinity limitation, depending on the module.
Thus, a specific initial population is defined for each compartment and benchmark case.
Each initial population is stored in 'Benchmarks/ModuleBenchmarks/PlantModules/Saltmarsh/"compartment"/"module"/'.

The random seed for all setups is 643879.

The time step length is 86400 seconds (1 day).
For the standard benchmark runs, the simulation time is 8640000 seconds (100 days), and output is written after the first and last time step.
For the CI benchmarks, the simulation time is 864000 seconds (10 days), and output is written after the last time step only.
The first output is used for automatic testing.

## Disturbance modules

Disturbance benchmarks test the effect of stochastic disturbance events on plant populations.
Each benchmark uses a fixed random seed (643879) and a population of 10 individuals with varying `r_stem` values, so that size-dependent mortality logic can be verified.

The simulation time span covers approximately 3 years, which is sufficient to trigger multiple disturbance events while keeping CI execution time under 2 seconds.

Benchmarks are stored in `Benchmarks/ModuleBenchmarks/DisturbanceLib/<concept>/`.

### Hurricane

Tests large-scale hurricane disturbance (Vogt et al. 2014, scenario 3).
Circular patches are placed randomly within the domain; trees inside patches are killed with DBH-dependent probabilities.

### Lightning

Tests small-scale lightning gap disturbance (Vogt et al. 2014, scenario 2).
Circular gaps with random radii are created each year; all trees inside gaps are removed.

## Population modules

*coming soon*

## Model output modules

*coming soon*

# Automated test

All benchmarks listed in 'Benchmarks/BenchmarkList.xml' are used for automatic testing of pyMANGA.
This list should only include benchmarks that are referenced by '< name>_CI.xml' to save execution time.

The test benchmarks can be executed with ``py .\Benchmarks\test_Benchmarks_CI.py``.
