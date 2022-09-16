

Array of times for output to be written, defined in seconds. Example:
<output_times> [86400, 12960000, 38880000] </output_times> or
<output_times> [1e6, 1.38e8] </output_times>

If defined, all other outputs are omitted.
Caution: Numbers should be a multiple of time step length, otherwise no output is written, i.e. output is only written, if the predefined times are hit during simulation.
Parameter is optional.
