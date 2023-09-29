Below-ground module allowing that pyMANGA is used as boundary condition of OGS (***beta***)

Functionality:
    - OGS is configured including project file and meshes.
    - Boundary conditions (BC) are defined in a Python script.
    - In this script, pyMANGA is initialized.
    - The BC ``FluxToTrees`` communicates with pyMANGA, i.e. transfers salinity and triggers plant dynamics.

Note:
    - The time stepping is defined in the OGS project file, but the tags must also be included in the pyMANGA project (although their values are not taken into account).
  - The pyMANGA time step length is defined in python_script.py
  - All paths should be provided as absolute paths. This includes the following files
    - runModel.py
    - python_script.py
    - pyMANGA project

Advantage:
    - Faster than calling OGS as module inside pyMANGA
    - Less file output from OGS

Example:
    [OGSExternal](https://github.com/pymanga/pyMANGA/tree/master/Benchmarks/ExampleSetups/OGSExternal)

