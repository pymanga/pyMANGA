---
title: "The pyMANGA project"
linkTitle: "The pyMANGA project"
weight: 1
description:
---

pyMANGA is controlled via an xml file (see also <a href="/de/docs/steuerFILE/">this section</a>).
The content of the XML file to run this example is presented here.
OGS specific adjustments and parameters are explained.
A description of all other configurations can be found in the <a href="https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html" target="_blank">general documentation</a>.

    <?xml version="1.0" encoding="ISO-8859-1"?>
        <MangaProject>
            <random_seed>1</random_seed>
            <tree_dynamics>
            <aboveground_competition>
                <type>SimpleTest</type>
            </aboveground_competition>

For simulations with the underground concept OGSLargeScale3D, the following concept-specific tags must be defined:

-           the absolute path to the folder with all relevant OGS files (*ogs_project_folder*)
-           the OGS project file (*ogs_project_file*)
-           the source mesh (*source_mesh*)
-           the bulk mesh (*bulk_mesh*)
-           the time step length, which indicates how long the groundwater flow model calculates before the rest of the BETTINA time step is extrapolated(*delta_t_ogs*)
-           Script with Python boundary conditions (*python_script*)

The OGS project described in <a href="/en/docs/example_model_ogs_bettina/ogs_project/">The OGS project</a> must be specified as *ogs_project_file*.
The previously defined python constraint is inserted under the name *python_script*.
Definition and usage of time dependent boundary conditions are described in detail at <a href="/en/docs/example_model_ogs_bettina/the_boundary_conditions/">the boundary conditions</a>. 
*delta_t_ogs* defines for how long the groundwater flow model calculates before extrapolating the rest of the BETTINA time step.
Creation of the required meshes is described in <a href="/en/docs/example_model_ogs_bettina/the_groundwater_domain/">the groundwater domain</a> section.
The parameters *seaward_salinity* and *landward_salinity* are used in the python boundary conditions.
Arbitrary parameters can be introduced here, as long as we use them again in our boundary condition definition.
Spezifications of the tide, beginning with *tide_* are used in the python boundary file.

        <belowground_competition>
            <type>OGSLargeScale3D</type>
            <ogs_project_folder>/ABSOLUTE/PATH/TO/pyMANGA/test/website_test/</ogs_project_folder>
            <ogs_project_file>ogs_projectfile.prj</ogs_project_file>
            <source_mesh>my_first_source.vtu</source_mesh>
            <bulk_mesh>my_first_model.vtu</bulk_mesh>
            <delta_t_ogs>500000</delta_t_ogs>
            <abiotic_drivers>
                <seaward_salinity>0.035</seaward_salinity>
                <landward_salinity>0.035</landward_salinity>
                <tide_daily_amplitude> 0 </tide_daily_amplitude>
                <tide_monthly_amplitude> 0 </tide_monthly_amplitude>
                <tide_daily_period> 60 * 60 * 12. </tide_daily_period>
                <tide_monthly_period> 60. * 60 * 24 * 31 / 2. </tide_monthly_period>
            </abiotic_drivers>
            <python_script>python_script.py</python_script>
        </belowground_competition>
        <tree_growth_and_death>
            <type>SimpleBettina</type>
        </tree_growth_and_death>
        </tree_dynamics>
	   
For this example, we use an initial tree distribution.

        <initial_population>
            <group>
                <name>Initial</name>
                <species>Avicennia</species>
                <distribution>
                    <type>GroupFromFile</type>
                    <filename>/ABSOLUTE/PATH/TO/pyMANGA/test/website_test/initial_trees.csv</filename>
                </distribution>
            </group>
        </initial_population>
            <tree_time_loop>
            <type>Simple</type>
            <t_start>0</t_start>
            <t_end> 3e9 </t_end>
            <delta_t> 3e6</delta_t>
        </tree_time_loop>
        <visualization>
           <type>NONE</type>
        </visualization>
        <tree_output>
            <type>NONE</type>
        </tree_output>
    </MangaProject>

The inital tree distribution is stored in a csv file and has the following content:

    tree,	time,	x,	y,	r_stem,	h_stem,	r_crown,	r_root	
    Initial_000000001,	0,	20,	5.0,	0.04,	3.5,	1.4,	0.7
    Initial_000000002,	0,	22.5,	5.0,	0.04,	3.5,	1.4,	0.7
	
