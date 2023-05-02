<MangaProject>
    <random_seed>1</random_seed>
    <ressources>
        <aboveground>
            <type> SimpleAsymmetricZOI </type>
            <domain>
                <x_1> 0 </x_1>
                <y_1> 0 </y_1>
                <x_2> 50 </x_2>
                <y_2> 10 </y_2>
            <x_resolution> 250 </x_resolution>
            <y_resolution> 50 </y_resolution>
            </domain>
        </aboveground>
        <belowground>
            <type> FixedSalinity </type>
            <min_x>0</min_x>
            <max_x>50</max_x>
            <salinity>0.0 0.035</salinity>
        </belowground>
    <plant_dynamics>
        <type> SimpleBettina </type>
        <mortality> Random </mortality>
    </plant_dynamics>
    </ressources>
    <population>
        <group>
            <name> Initial </name>
            <growth_dynamic> SimpleBettina </growth_dynamic>
            <mortality> NoGrowth </mortality>
            <species> Avicennia </species>
            <distribution>
                <type> Random </type>
                <n_individuals> 10 </n_individuals>
                <n_recruitment_per_step> 2 </n_recruitment_per_step>
                <domain>
                    <x_1> 0 </x_1>
                    <y_1> 0 </y_1>
                    <x_2> 50 </x_2>
                    <y_2> 10 </y_2>
                </domain>
            </distribution>
        </group>
    </population>
    <time_loop>
        <type> Simple </type>
        <t_start> 0 </t_start>
        <t_end> 5e6 </t_end>
        <delta_t> 1e5 </delta_t>
    </time_loop>
    <visualization>
        <type> NONE </type>
    </visualization>
    <output>
         <type> OneTimestepOneFile </type>
        <output_each_nth_timestep>5</output_each_nth_timestep>
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
</MangaProject>

