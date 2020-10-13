---
title: "Interaktives Steuerfile"
linkTitle: "Interaktives Steuerfile"
weight: 4
description:
---

<head>
<style type="text/css">
<!--
code.lines {
       white-space: pre;}
-->
</style>
</head>

<pre>
<code class="language-xml"; white-space="pre"; line-break="strict">

<details>
<summary >&lt;MangaProject></summary>
<p>
Hier finden Sie in kürze eine Beschreibung. Die Frage ist, was passiert wenn diese über eine Zeile hinausgeht?
</p>
</details>
<details>
<summary>    &lt;tree_dynamics></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>        &lt;aboveground_competition></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>            &lt;type> SimpleAsymmetricZOI &lt;/type></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>            &lt;domain></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>                &lt;x_1> 0 &lt;/x_1></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>                &lt;y_1> 0 &lt;/y_1></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>                &lt;x_2> 185 &lt;/x_2></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>                &lt;y_2> 10 &lt;/y_2></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details> 
<summary>	          &lt;x_resolution> 720 &lt;/x_resolution></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>	          &lt;y_resolution> 38 &lt;/y_resolution></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>            &lt;/domain></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>
<details>
<summary>        &lt;/aboveground_competition></summary>
Hier finden Sie in kürze eine Beschreibung.
</details>












        &lt;belowground_competition>
            &lt;type> OGSLargeScale3D &lt;/type>
            &lt;ogs_project_folder> /home/jonas/Dokumente/WHK/Marzipan/Quellcode/pyMANGA/a &lt;/ogs_project_folder>
            &lt;ogs_project_file> testmodel.prj &lt;/ogs_project_file>
            &lt;abiotic_drivers>
                &lt;seaward_salinity> 0.05 &lt;/seaward_salinity>
            &lt;/abiotic_drivers>
            &lt;delta_t_ogs> 1500000 &lt;/delta_t_ogs>
            &lt;source_mesh> source_domain.vtu &lt;/source_mesh>
            &lt;!--bulk_mesh> testbulk.vtu &lt;/bulk_mesh-->
            &lt;!--use_old_ogs_results>True&lt;/use_old_ogs_results-->
            &lt;python_script>python_script.py&lt;/python_script>
        &lt;/belowground_competition>
        &lt;tree_growth_and_death>
            &lt;type> SimpleBettina &lt;/type>
        &lt;/tree_growth_and_death>
    &lt;/tree_dynamics>
    &lt;initial_population>
        &lt;group>
            &lt;name> Recruiting &lt;/name>
            &lt;species> Avicennia &lt;/species>
            &lt;distribution>
                &lt;type> Random &lt;/type>
                &lt;domain>
                    &lt;x_1> 0 &lt;/x_1>
                    &lt;y_1> 0 &lt;/y_1>
                    &lt;x_2> 185 &lt;/x_2>
                    &lt;y_2> 10 &lt;/y_2>
                &lt;/domain>
                &lt;n_individuals> 0 &lt;/n_individuals>
                &lt;n_recruitment_per_step> 30 &lt;/n_recruitment_per_step>
            &lt;/distribution>
        &lt;/group>
        &lt;group>
            &lt;name> Initial &lt;/name>
            &lt;species> Avicennia &lt;/species>
            &lt;distribution>
                &lt;type> Random &lt;/type>
                &lt;domain>
                    &lt;x_1> 0 &lt;/x_1>
                    &lt;y_1> 0 &lt;/y_1>
                    &lt;x_2> 185 &lt;/x_2>
                    &lt;y_2> 10 &lt;/y_2>
                &lt;/domain>
                &lt;n_individuals> 30 &lt;/n_individuals>

            &lt;/distribution>
        &lt;/group>
    &lt;/initial_population>
    &lt;tree_time_loop>
        &lt;type> Simple &lt;/type>
        &lt;t_start> 0 &lt;/t_start>
        &lt;t_end> 157788000000 &lt;/t_end>
        &lt;delta_t> 15778800 &lt;/delta_t>
    &lt;/tree_time_loop>
    &lt;visualization>
        &lt;type> NONE &lt;/type>
    &lt;/visualization>
    &lt;tree_output>
        &lt;type> OneTimestepOneFile &lt;/type>
        &lt;output_each_nth_timestep> 1 &lt;/output_each_nth_timestep>
        &lt;output_dir> /home/jonas/Dokumente/WHK/Marzipan/Quellcode/pyMANGA/a/TreeOutput/ &lt;/output_dir>
        &lt;geometry_output> r_stem &lt;/geometry_output>
        &lt;geometry_output> h_stem &lt;/geometry_output>
        &lt;geometry_output> r_crown &lt;/geometry_output>
        &lt;geometry_output> r_root &lt;/geometry_output>
        &lt;growth_output> salinity &lt;/growth_output>
    &lt;/tree_output>
&lt;/MangaProject>
</code>
</pre>
