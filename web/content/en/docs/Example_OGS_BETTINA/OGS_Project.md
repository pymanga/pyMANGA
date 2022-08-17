---
title: "The OGS Project"
linkTitle: "The OGS Project"
weight: 3
description:
---

OGS is configured via project files.
Such a file is explained below as an example.

The required meshes are defined directly after the header.
We use the main domain, the mesh for water extraction from the trees and our edge meshes.
This part may need to be adjusted.

    <?xml version="1.0" encoding="ISO-8859-1"?>
    <OpenGeoSysProject>
        <meshes>
        <mesh>my_first_model.vtu</mesh>
        <mesh>left_boundary.vtu</mesh>
        <mesh>right_boundary.vtu</mesh>
        <mesh>top_boundary.vtu</mesh>
        <mesh>my_first_source.vtu</mesh>
        </meshes>

In the following section, process parameters & numerical quantities are defined.
This part usually does not require any adjustment.

        <python_script>python_source.py</python_script>
        <processes>
        <process>
            <name>hc</name>
            <type>ComponentTransport</type>
            <non_advective_form>true</non_advective_form>
            <integration_order>2</integration_order>
            <process_variables>
                <concentration>concentration</concentration>
                <pressure>pressure</pressure>
            </process_variables>
            <specific_body_force> 0 0 -9.81</specific_body_force>
            <secondary_variables>
                <secondary_variable type="static" internal_name="darcy_velocity" output_name="darcy_velocity"/>
            </secondary_variables>
        </process>
        </processes>
        <media>
        <medium id="0">
            <phases>
                <phase>
                    <type>AqueousLiquid</type>
                    <components>
                        <component>
                            <name>concentration</name>
                            <properties>
                                <property>
                                    <name>pore_diffusion</name>
                                    <type>Constant</type>
                                    <value>0</value>
                                </property>
                                <property>
                                    <name>molecular_diffusion</name>
                                    <value>1e-9</value>
                                    <type>Constant</type>
                                </property>
                                <property>
                                    <name>retardation_factor</name>
                                    <type>Constant</type>
                                    <value>1</value>
                                </property>
                                <property>
                                    <name>decay_rate</name>
                                    <type>Parameter</type>
                                    <parameter_name>decay</parameter_name>
                                </property>
                            </properties>
                        </component>
                    </components>
                    <properties>
                        <property>
                            <name>density</name>
                            <type>Constant</type>
                            <value>1e3</value>
                        </property>
                        <property>
                            <name>viscosity</name>
                            <type>Constant</type>
                            <value>1.0e-3</value>
                        </property>
                    </properties>
                </phase>
            </phases>
            <properties>
                <property>
                    <name>permeability</name>
                    <type>Parameter</type>
                    <parameter_name>kappa1</parameter_name>
                </property>
                <property>
                    <name>porosity</name>
                    <type>Parameter</type>
                    <parameter_name>constant_porosity_parameter</parameter_name>
                </property>
                <property>
                    <name>transversal_dispersivity</name>
                    <type>Constant</type>
                    <value>.5</value>
                </property>
                <property>
                    <name>longitudinal_dispersivity</name>
                    <type>Constant</type>
                    <value>1</value>
                </property>
            </properties>
        </medium>
        </media>

The time loop is automatically updated by pyMANGA.
The only variable that may need to be adjusted is the storage interval for the groundwater domain.

        <time_loop>
        <processes>
            <process ref="hc">
                <nonlinear_solver>basic_picard</nonlinear_solver>
                <convergence_criterion>
                    <type>PerComponentDeltaX</type>
                    <norm_type>NORM2</norm_type>
                    <reltols>1e-8 1e-8</reltols>
                </convergence_criterion>
                <time_discretization>
                    <type>BackwardEuler</type>
                </time_discretization>
                <time_stepping>
                    <type>FixedTimeStepping</type>
                    <t_end> 315360000 </t_end>
                    <t_initial> 0 </t_initial>
                    <timesteps>
                        <pair>
                            <delta_t>14400</delta_t>
                            <repeat>1</repeat>
                        </pair>
                    </timesteps>
                </time_stepping>
            </process>
        </processes>
        <output>
            <type>VTK</type>
            <prefix>trees_in_box__ogsOutput</prefix>
            <timesteps>
                <pair>
                    <repeat>1</repeat>
                    <each_steps>1500</each_steps> <!-- every 0.5 years -->
                </pair>
            </timesteps>
            <output_iteration_results>false</output_iteration_results>
            <variables>
                <variable>concentration</variable>
                <variable>pressure</variable>
                <variable>darcy_velocity</variable>
            </variables>
        </output>
        </time_loop>
	    
The parameters used can be specified in the project file.

        <parameters>
        <parameter>
            <name>rho_fluid</name>
            <type>Constant</type>
            <value>1000</value>
        </parameter>
        <parameter>
            <name>decay</name>
            <type>Constant</type>
            <value>0</value>
        </parameter>
        <parameter>
            <name>c_ini</name>
            <type>MeshNode</type>
            <field_name>c_ini</field_name>
        </parameter>
        <parameter>
            <name>p_ini</name>
            <type>MeshNode</type>
            <field_name>p_ini</field_name>
        </parameter>
        <parameter>
            <name>constant_porosity_parameter</name>
            <type>Constant</type>
            <value>0.5</value>
        </parameter>
        <parameter>
            <name>kappa1</name>
            <type>Constant</type>
            <values>2.5e-11 0 0 0 2.5e-11 0 0 0 2.5e-11</values>
        </parameter>
        <parameter>
            <name>c_left</name>
            <type>Constant</type>
            <value>.035</value>
        </parameter>
        <parameter>
            <name>c_right</name>
            <type>Constant</type>
            <value>.035</value>
        </parameter>
        <parameter>
            <name>p_left</name>
            <type>MeshNode</type>
            <field_name>p_ini</field_name>
            <mesh>left_boundary</mesh>
        </parameter>
        <parameter>
            <name>p_right</name>
            <type>MeshNode</type>
            <field_name>p_ini</field_name>
            <mesh>right_boundary</mesh>
        </parameter>
        </parameters>

The boundary conditions are now defined in the *process_variables* section.
This may need to be adjusted.
First, the boundary conditions for the concentration are assigned.
We use the previously defined python boundary conditions.
Each boundary condition is defined on a mesh and consists of a previously defined BC object.
See the section <a href="/en/docs/example_ogs_bettina/the_boundary_conditions">The boundary conditions</a>.

        <process_variables>
        <process_variable>
            <name>concentration</name>
            <components>1</components>
            <order>1</order>
            <initial_condition>c_ini</initial_condition>
            <boundary_conditions>
                <boundary_condition>
                    <mesh>left_boundary</mesh>
                    <type>Python</type>
                    <bc_object>bc_tide_C</bc_object>
                </boundary_condition>
                <boundary_condition>
                    <type>Python</type>
                    <mesh>top_boundary</mesh>
                    <bc_object>bc_tide_C</bc_object>
                </boundary_condition>
                <boundary_condition>
                    <type>Python</type>
                    <mesh>right_boundary</mesh>
                    <bc_object>bc_land_C</bc_object>
                </boundary_condition>
            </boundary_conditions>
        </process_variable>

After defining the concentration boundary conditions, the boundary conditions for the pressure are still missing:

        <process_variable>
            <name>pressure</name>
            <components>1</components>
            <order>1</order>
            <initial_condition>p_ini</initial_condition>
            <boundary_conditions>
                <boundary_condition>
                    <type>Python</type>
                    <mesh>left_boundary</mesh>
                    <bc_object>bc_tide_p</bc_object>
                </boundary_condition>
                <boundary_condition>
                    <mesh>top_boundary</mesh>
                    <type>Python</type>
                    <bc_object>bc_tide_p</bc_object>
                </boundary_condition>
                <boundary_condition>
                    <mesh>right_boundary</mesh>
                    <type>Python</type>
                    <bc_object>bc_land_p</bc_object>
                </boundary_condition>
                
For the tree water uptake, a helpter for the source terms is required and must be defined here.
                
                <boundary_condition>
                    <mesh>right_boundary</mesh>
                    <type>Python</type>
                    <bc_object>bc_source_helper</bc_object>
                </boundary_condition>
            </boundary_conditions>
            
The water uptake of the trees is described as a source term and is automatically added to our python script by pyMANGA.
The source term only needs to be defined once in the OGS project file:

            <source_terms>
                <source_term>
                    <type>Python</type>
                    <mesh>my_first_source</mesh>
                    <source_term_object>flux_to_trees</source_term_object>
                    <flush_stdout> true </flush_stdout>
                </source_term>
            </source_terms>
        </process_variable>
        </process_variables>

At the end of the project file, the parameters for the numerical solvers must still be specified.
In general, these no longer require adjustment.

        <nonlinear_solvers>
        <nonlinear_solver>
            <name>basic_picard</name>
            <type>Picard</type>
            <max_iter>20</max_iter>
            <linear_solver>general_linear_solver</linear_solver>
        </nonlinear_solver>
        </nonlinear_solvers>
        <linear_solvers>
        <linear_solver>
            <name>general_linear_solver</name>
            <lis>-i bicgstab -p ilut -tol 1e-12 -maxiter 20000</lis>
            <eigen>
                <solver_type>BiCGSTAB</solver_type>
                <precon_type>DIAGONAL</precon_type>
                <max_iteration_step>10000</max_iteration_step>
                <error_tolerance>1e-12</error_tolerance>
            </eigen>
            <petsc>
                <prefix>hc</prefix>
                <parameters>-hc_ksp_type bcgs -hc_pc_type bjacobi -hc_ksp_rtol 1e-12 -hc_ksp_max_it 20000</parameters>
            </petsc>
        </linear_solver>
        </linear_solvers>
    </OpenGeoSysProject>


