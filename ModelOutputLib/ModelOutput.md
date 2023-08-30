
Attributes:
    type (string): Name of output module (see notes).
    output_each_nth_timestep (list): (optional) max. 2 numbers indicating in which timestep output is written. The first value refers to the time before and after ``output_time_range`` while the second number applies to `output_time_range`.
    output_times (list): (optional) values indicate time step(s) to write output.
    output_time_range (list): (optional) 2 values, indicating a time window where each step is written to the output file except a second value is defined for ``output_each_nth_timestep``.
    ...

Notes:
    type **OneFile** write model output to 1 csv-file  
    type **OnePlantOneFile**  ...

Examples:
    ````xml
    <output>
        <type> OneFile </type>
        <output_each_nth_timestep> [20, 3] </output_each_nth_timestep>
        <output_times> [23] </output_times>
        <output_time_range> [80, 95] </output_time_range>
        <allow_previous_output>True</allow_previous_output>
        <output_dir>Benchmarks/TestOutputs/</output_dir>
        <geometry_output> r_stem </geometry_output>
        <geometry_output> h_stem </geometry_output>
        <geometry_output> r_crown </geometry_output>
        <geometry_output> r_root </geometry_output>
        <growth_output> growth </growth_output>
        <growth_output> ag_resources </growth_output>
        <growth_output> bg_resources </growth_output>
    </output>
    ````