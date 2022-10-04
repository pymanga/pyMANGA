---
title: "Das pyMANGA-Projekt"
linkTitle: "Das pyMANGA-Projekt"
weight: 1
description:
---

Wie bekannt wird pyMANGA über ein xml-File gesteuert (siehe hierzu auch <a href="/de/docs/steuerdatei/">diesen Abschnitt</a>).
Hier wird der Inhalt des XML-Files präsentiert.
OGS-Spezifische Anpassungen und Parameter werden erläutert.
Eine Beschreibung aller anderen Konfigurationen kann der <a href="https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html" target="_blank">allgemeinen Dokumentation</a> entnommen werden.

    <?xml version="1.0" encoding="ISO-8859-1"?>
        <MangaProject>
            <random_seed>1</random_seed>
            <tree_dynamics>
            <aboveground_competition>
                <type>SimpleTest</type>
            </aboveground_competition>

Für Simulationen mit dem Untergrundkonzept OGSLargeScale3D müssen folgende Konzeptspezifische Tags definiert werden:

-     der absolute Pfad zum Ordner mit allen relevanten OGS-Dateien (*ogs_project_folder*)
-     die OGS- Projektdatei (*ogs_project_file*)
-     das Source Mesh (*source_mesh*)
-     das Bulk Mesh (*bulk_mesh*)
-     die Zeitschrittlänge, die angibt wie lange das Grundwasserströmungsmodell rechnet, bevor der Rest des BETTINA-Zeitschritts extrapoliert wird(*delta_t_ogs*)
-     Skript mit Python-Randbedingungen (*python_script*)

Das in <a href="/de/docs/beispielmodell_ogs_bettina/ogs_projekt/">Das OGS Projekt</a> beschriebene ogs-Projekt muss als *ogs_project_file* angegeben werden.
Die zuvor definierte python Randbedingung wird unter dem Namen *python_script* eingefügt.
Definition und Nutzung der Zeitlich veränderlichen Randbedingungen sind unter <a href="/de/docs/beispielmodell_ogs_bettina/die_randbedingungen/">die Ranbedingungen</a> ausführlich beschrieben. 
*delta_t_ogs* definiert, für wie lange das Grundwasserströmungsmodell rechnet, bevor der Rest des BETTINA-Zeitschritts extrapoliert wird.
Wie die Meshes für die Grundwassersimulation erstellt werden ist im Detail unter <a href="/de/docs/beispielmodell_ogs_bettina/die_grundwasserdomain/">die Grundwasserdomain</a> beschrieben.
Die Parameter *seaward_salinity* und *landward_salinity* sind Parameter, die später in der python Randbedingung von OGS genutzt werden.
Hier können beliebige Parameter eingeführt werden, solange wir diese in unserer Randbedingung nutzen.

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
            </abiotic_drivers>
            <python_script>python_script.py</python_script>
        </belowground_competition>
        <tree_growth_and_death>
            <type>SimpleBettina</type>
        </tree_growth_and_death>
        </tree_dynamics>
	   
Für dieses Beispiel verwenden wir eine zuvor abgespeicherte initiale Baumverteilung.

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

In diesem Beispiel wird eine initiale Baumverteilung in das Programm hereingeladen.
Diese sollte in einem externen File mit folgendem Inhalt liegen:

    tree,	time,	x,	y,	r_stem,	h_stem,	r_crown,	r_root	
    Initial_000000001,	0,	20,	5.0,	0.04,	3.5,	1.4,	0.7
    Initial_000000002,	0,	22.5,	5.0,	0.04,	3.5,	1.4,	0.7
	
