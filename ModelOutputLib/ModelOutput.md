# Description

The child modules of this class define how the model output is written, i.e. its frequency and content.
All model output modules share the same attributes.
They only differ in how the output is distributed to different files.

The minimum output that will be written is the plant ID, it's position and the simulation time.
This is done without any specification in the project file.

# Usage

*The values shown here are examples. See Attributes for more information.*

```xml
<output>
    <type> OneFile </type>
    <output_dir>Benchmarks/TestOutputs/</output_dir>
    <output_dir>Benchmarks/TestOutputs/</output_dir>
    <output_dir>Benchmarks/TestOutputs/</output_dir>
    <output_times> [23, 37] </output_times>
    <output_time_range>[70, 90]</output_time_range>
    <output_each_nth_timestep>[10, 1]</output_each_nth_timestep>
    <geometry_output> r_stem </geometry_output>
    <growth_output> bg_factor </growth_output>
</output>
```

# Attributes

- ``type`` (string): Name of output module (see notes).
- ``output_dir`` (string): directory to which the output will be written. Can be specified as either a relative or absolute path.
- ``delimiter`` (string): (optional) delimiter character to separate columns. Options: tab (\t), colon (:) and semi-colon (;). Default: \t
- ``output_times`` (list): (optional) values indicate time step(s) to write output.
- ``output_each_nth_timestep`` (list): (optional) max. 2 values indicating in which timestep output is written. The first value refers to the time before and after ``output_time_range`` while the second number applies to `output_time_range`. Default: Output is written every time step.
- ``output_time_range`` (list): (optional) 2 values, indicating a time window where each step is written to the output file except a second value is defined for ``output_each_nth_timestep``.
- ``allow_previous_output`` (bool): (optional) If True existing output is overwritten. Default: False. 
- ``geometry_output`` (string): (optional) plant geometry parameters for which output should be written. Possible parameters are defined in `pyMANGA.PlantModelLib`. 
- ``growth_output`` (string): (optional) plant growth parameters for which output should be written. Possible parameters are defined in `pyMANGA.PlantModelLib`. 
- ``network_output`` (string): (optional) network parameters for which output should be written. Possible parameters are defined in `pyMANGA.PlantModelLib`.

Note:
    - The ``type`` defines the structure of the output and therefore how many csv files will be written.
    - ``type`` **OneFile** creates one file for all model output 
    - ``type`` **OnePlantOneFile** creates one file per plant
    - ``type`` **OneTimestepOneFile** creates one file for each time step
    - ``type`` **OneTimestepOneFilePerGroup** creates one file for each time step and group


# Value

writes a csv files

# Details
## Purpose

These modules define when and how pyMANGA results are saved to one or multiple csv-files.

## Process overview

The module defines the output time.
If this is not specified in the project file, output is written at each time step.

In addition, output is forced when a whole plant group dies and in the last time step.

## Application & Restrictions

-

# References

-

# Author(s)

Jasper Bathmann, Marie-Christin Wimmler


# Examples

Write all output to a csv file. 
The output is written to the 'myResults' directory.
If the output file already exists in this directory, it will be overwritten.
There are two different output frequencies.
Before time step 80 and after time step 95 the output is written every 20th time step.
Between timestep 80 and 95 the output is written every 3rd timestep.
In addition, output is written at the 23rd timestep.
This file contains the plant ID, the xy coordinates and the time.

*Note* ``output_time_range`` and ``output_times`` are defined in seconds.

````xml
<output>
    <type> OneFile </type>
    <output_dir>myResults/</output_dir>
    <allow_previous_output>True</allow_previous_output>
    <output_each_nth_timestep> [20, 3] </output_each_nth_timestep>
    <output_time_range> [80, 95] </output_time_range>
    <output_times> [23] </output_times>
</output>
````


