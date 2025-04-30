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
Each initial population is stored in 'Benchmarks/ModuleBenchmarks/PlantModules/< plant_module>/< compartment>/'.

If landward and seaward boundary conditions must be defined in a setup, the salinity is set to 25 ppt at the landward boundary and 35 ppt at the seaward boundary.
The random seed for all setups is 643879.

The time step length is 1e6 seconds (~12 days) and the simulation time is 5e8 seconds (~15.8 years, i.e. 500 time steps).
Output is written after the first and last time step. The first output is used for automatic testing.

### Type: marsh plant

*coming soon*

## Population modules

*coming soon*

## Model output modules

*coming soon*

# Automated test

All benchmarks listed in 'Benchmarks/BenchmarkList.xml' are used for automatic testing of pyMANGA.
This list should only include benchmarks that are referenced by '< name>_CI.xml' to save execution time.

The test benchmarks can be executed with ``py .\Benchmarks\test_Benchmarks_CI.py``.
