Library of plant modules that handle plant growth and mortality.

Each growth module updates the plant geometry based on the available resources and it's particular approaches (see ``pyMANGA.ResourceLib``).
Each mortality module defines whether a plant survives this time step or not.

## Output variables

Growth-related variables can be written to output files using the ``<growth_output>`` tag in the project file.
In addition to module-specific variables (e.g., ``growth``, ``ag_factor``, ``bg_factor``), the following variable is available:

- ``mortality_cause``: indicates what killed a plant (e.g., "Hurricane", "Lightning"). Set by disturbance modules (see ``pyMANGA.DisturbanceLib``). Value is "None" if the plant is alive or died from a non-disturbance cause.
