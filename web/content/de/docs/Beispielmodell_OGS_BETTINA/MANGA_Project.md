---
title: "Das pyMANGA-Projekt"
linkTitle: "Das pyMANGA-Projekt"
weight: 1
description:
---

Wie bekannt wird pyMANGA über ein xml-File gesteuert.
Hier wird der Inhalt des XML-Files präsentiert.
OGS-Spezifische Anpassungen und Parameter werden erläutert.
Eine Beschreibung aller anderen Konfigurationen kann der allgemeinen Dokumentation entnommen werden.

    <?xml version="1.0" encoding="ISO-8859-1"?>
        <MangaProject>
            <random_seed>1</random_seed>
            <tree_dynamics>
            <aboveground_competition>
                <type>SimpleTest</type>
            </aboveground_competition>

Der Ort, an dem alle für OGS relevanten Dateien liegen ist als *ogs_project_folder* benannt.
Das in "Das OGS Projekt" beschriebene ogs-Projekt muss als *ogs_project_file* angegeben werden.
Die zuvor definierte python Randbedingung wird unter dem Namen *python_script* eingefügt.
*delta_t_ogs* definiert, für wie lange das Grundwasserströmungsmodell rechnet, bevor der Rest des BETTINA-Zeitschritts extrapoliert wird.

        <belowground_competition>
            <type>OGSLargeScale3D</type>
            <ogs_project_folder>/home/bathmann/Documents/AGBerger/code/pyMANGA/test/website_test/</ogs_project_folder>
            <ogs_project_file>ogs_projectfile.prj</ogs_project_file>
            <source_mesh>my_first_source.vtu</source_mesh>
            <bulk_mesh>my_first_model.vtu</bulk_mesh>
            <delta_t_ogs>500000</delta_t_ogs>
            <abiotic_drivers>
                <seaward_salinity>0.035</seaward_salinity>
            </abiotic_drivers>
            <python_script>python_script.py</python_script>
        </belowground_competition>
        <tree_growth_and_death>
            <type>SimpleBettina</type>
        </tree_growth_and_death>
        </tree_dynamics>
	   
Für das erste Beispiel wird eine Initiale Baumverteilung in das Programm hereingeladen.

        <initial_population>
            <group>
                <name>Initial</name>
                <species>Avicennia</species>
                <distribution>
                    <type>GroupFromFile</type>
                    <filename>/home/bathmann/Documents/AGBerger/code/pyMANGA/test/website_test/initial_trees.csv</filename>
                </distribution>
            </group>
        </initial_population>
            <tree_time_loop>
            <type>Simple</type>
            <t_start>0</t_start>
            <t_end> 3e9 </t_end> <!-- ~ 95 a-->
            <delta_t> 3e6</delta_t> <!-- ~ 35 d-->
        </tree_time_loop>
        <visualization>
           <type>NONE</type>
        </visualization>
        <tree_output>
            <type>NONE</type>
        </tree_output>
    </MangaProject>

Die Initiale Baumverteilung aus *initial_trees.csv* sollte in einer seperaten *.csv* Datei gespeichert werden:

    tree,	time,	x,	y,	r_stem,	h_stem,	r_crown,	r_root	
    Initial_000000001,	0,	20,	5.0,	0.04,	3.5,	1.4,	0.7
    Initial_000000002,	0,	22.5,	5.0,	0.04,	3.5,	1.4,	0.7
	
