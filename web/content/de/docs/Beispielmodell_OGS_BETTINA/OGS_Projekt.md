---
title: "Das OGS-Projekt"
linkTitle: "Das OGS-Projekt"
weight: 3
description:
---

OGS wird über Projektdateien konfiguriert.
Im folgenden wird Beispielhaft eine solche Datei erläutert.
Nach dem Header werden direkt die benötigten meshes definiert.
Wir verwenden die Hauptdomain, das Mesh für die Wasserentnahme der Bäume und unsere Randmeshes.
Dieser Teil muss ggf. angepasst werden.

    <?xml version="1.0" encoding="ISO-8859-1"?>
    <OpenGeoSysProject>
        <meshes>
        <mesh>my_first_model.vtu</mesh>
        <mesh>left_boundary.vtu</mesh>
        <mesh>right_boundary.vtu</mesh>
        <mesh>top_boundary.vtu</mesh>
        <mesh>my_first_source.vtu</mesh>
        </meshes>

Im folgenden Abschnitt werden Prozessparameter & numerische Größen definiert.
Dieser Teil bedarf meist keiner Anpassung.

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

Die Zeitschleife wird von pyMANGA automatisch aktualisiert.
Die einzige Größe, die uns eventuell interessiert ist, in welchem Intervall die Grundwasserdomain gespeichert wird.

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
	    
Die verwendeten Parameter können in der Projektdatei spezifiziert werden. 

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

Im Abschnitt *process_variables* werden nun die Randbedingungen definiert.
Dies muss ggf angepasst werden.
Zuerst werden die Randbedingungen für die Konzentration zugewiesen.
Wir verwenden die zuvor definierten python-Randbedingungen.
Jede Randbedingung ist auf einem mesh definiert und besteht aus einem zuvor definierten BC-Object.
Siehe hierzu den Abschnitt "Die Randbedingungen".

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

Nach Definition der Konzentrations-Randbedingungen fehlen noch die Randbedingungen für den Druck:

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
            </boundary_conditions>
            
Die Wasseraufnahme der Bäume wird als Quellterm beschrieben und wird von pyMANGA automatisch zu unserem python-script hinzugefügt.
Der Quellterm muss lediglich in der OGS-Projektdatei einmal definiert werden:

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

Am Ende der Projektdatei müssen noch die Parameter für die numerischen Löser festgelegt werden.
Im Allgemeinen bedürfen diese keiner Anpassung mehr.

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


