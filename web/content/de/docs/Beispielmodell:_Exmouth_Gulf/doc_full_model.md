---
title: "Modelsetup Exmouth Golf"
linkTitle: "Modell-Setup"
weight: 2
description:
---

# Beschreibung des Modellsetups

Das Modell-Setup kann unter diesem Link gedownloaded werden. Es wird sowohl der Einfluss der Gezeitendynamik als auch der Zusammenhang zwischen Pflanzenwassernutzung und Salzgehalt im Porenwasser berücksichtigt. In der Veröffentlichung DOI XXX wird dieses Setup als full-model bezeichnet.

Im folgenden werden die wichtigsten Dateien des Setups genauer beschrieben. In der Hauptebene des Setups liegen ein Ordner "Input_OGS" und die zwei Dateien Avicennia.py und setup_pymanga.xml. Wie der Name vermuten lässt, befinden sich im Ordner "Input_OGS" die für die Grundwassermodellierung nötigen Modelleingangsdateien. Avicennia.py enthält Einstellungen zur Mangrovenart "Graue Mangrove". Hier können zum Beispiel die Wachstumsgeschwindigkeit, maximale Wachstumshöhe, maximale Lebenszeit und andere individuenspezifische Parameter definiert werden. Die Steuerdatei "Dateiname.xml" stellt das Herzstück eines jeden Modellsetups dar. Sie wird aufgerufen, um einen Modelllauf zu starten. Das Dokument README.md dient lediglich zu Informationszwecken und spielt bei der Modellierung mit pyMANGA keine Rolle.

# Steuerdatei: setup_pymanga.xml

Die Steuerdatei eines jeden pyMANGA-Setups wird im xml-Format geschrieben. Hier werden alle Einstellungen zur Modellierung vorgenommen. Im Folgenden die Steuerdatei für das Setup Exmouth-Golf genauer beschrieben.

## tree_dynamics

Unter dem Punkt "tree_dynamics" werden Einstellungen zur dynamischen Entwicklung des Baumbestands vorgenommen.

### aboveground_competition

Dieser Unterpunkt charakterisiert die Modellierung des Baumwachstums über dem Boden. Da pyMANGA das Wachstum über das Vorhandensein von Ressourcen modelliert, stehen diese auch in diesem Unterpunkt im Vordergrund. Die für pyMANGA relevanten überirdische Ressource stellt das Sonnenlich dar. Der erste Punkt, "type", definiert die Grundeinstellung als den Typ "SimpleAsymmetricZOI". Diese Einstellungen befinden sich im Quellcode des Programms unter ./TreeModelLib/AbovegroundCompetition/SimpleAsymmetricZOI". Mit dieser Grundeinstellung wird das Modellgebiet in Zonen unterteilt, in denen der Baum mit der jeweils größten Kronenhöhe alles zur Verfügung stehende Sonnenlicht bekommt. Die Klasse benötigt die unter dem nächsten Punkt "domain" definierten Eingangsgrößen. "y_1", "y_2, "x_1" und "x_2" legen die Grenzen des Modellgebiets fest. Die Koordinatenwerte mit den Indizes "1" definieren dabei die numerisch niedrigeren Werte, die Indizes "2" die numerisch höheren. "x_resolution" und "y_resolution" legen mit der Anzahl der Gitterknotenpunkte in die jeweilige Raumrichtung die räumliche Diskretisierung des Modellgebiets fest.

Derzeit gibt es noch eine weitere Klasse für "type", "SimpleTest". Diese soll für Beispiel-Setups und zur Überprüfung der korrekten Berechnung von Setups angewendet werden und eignet sich nicht zur Modellierung von realen Mangroven-Populationen.

### belowground_competition

Neben den überirdischen Ressourcen berücksichtigt pyMANGA auch die unterirdischen für die Bäume zur Verfügung stehenden Ressourcen. Im Punkt "belowground_competion" werden die Einstellungen hierfür im Steuerfile vorgenommen, wofür fünf verschiedene Klassen zur Verfügung stehen. Im Quellcode finden sich diese unter "./TreeModelLib/BelowgroundCompetition". In diesem Setup wird die Klasse "OGSLargeScale3D" verwendet (Unterpunkt "type"), welche für die Modellierung der Änderung des Salzgehalts im Porenwasser mithilfe eines komplexeren Grundwassermodells ausgelegt ist. 

Im Unterpunkt "ogs_project_folder" wird der Dateipfad der OGS-Eingangsdateien festgelegt, im nächsten Schritt der Name der OGS-Steuerdatei ("ogs_project_file").

Im Punkt "abiotic drivers" können der Salzgehalt des Meerwassers (bzw. i. A. des Salzwassers), die Periode der monatlichen und täglichen Tide und die Amplitude der monatlichen und täglichen Tide. In diesem Steuerfile ist nur der Wert für den Salzgehalt definiert, die Werte zum Tidenhub werden über python_script eingelesen (siehe am Ende dieses Abschnitts).

Mit "delta_t_ogs" wird die numerische Grundwassermodellierung mit OGS zeitlich diskretisiert. Diese Variable kann auch dazu genutzt werden, um numerische Instabilitäten zu beheben oder die Rechenzeit zu minimieren.

Im Punkt "source_mesh" wird der Name der Gitter-Datei für das OGS-Modell benannt. Diese Datei definiert die räumliche Diskretisierung des Grundwassermodells mittels einer vtu-Datei.

Im letzten Unterpunkt, "python_script", kann eine Python-Datei angegeben werden, in der Randbedingungen und Quellterme für das OGS-Modell definiert werden. Diese Angabe ist optional; die Notwendigkeit hängt von der Komplexität des Grundwassermodells ab. In diesem Modell sorgt die Datei für eine Schleife der aus der Datei EXM_Jan-Jul_2019.txt eingelesenen Informationen und eine Anpassung des mittleren Wasserstands.

### tree_growth_and_death

Im dritten und letzten Hauptpunkt des Abschnitts "tree_dynamics" kann das dynamische Konzept des Baumwachstums und -sterbens ausgewählt werden. Hierfür stehen drei zur Verfügung, "SimpleKiwi", "SimpleTest" und "SimpleBettina". Mit dem in diesem Setup verwendeten Konzepts "SimpleBettina" wird das "Kiwi single tree model"  zur Modellierung der dynamischen Entwicklung des Baumbestands verwendet. Weitere Informationen finden sich hierzu in dieser <a href="https://doi.org/10.1016/j.ecolmodel.2018.10.005"> Veröffentlichung</a> Im Quellcode finden sich die drei Konzepte unter 

	./TreeModelLib/GrowthAndDeathDynamics/".



An dieser Stelle ist der Abschnitt "tree_dynamics" zu Ende. 

## initial_population

In diesem Abschnitt wird die Baumpopulation zu Beginn des Modellierungszeitraums (IC) und das neue hinzukommen von Bäumen in jedem Zeitschritt festgelegt.


Eine Gruppe von Bäumen, die dem Modell hinzugefügt werden soll, wird im Element "group" definiert. So können zum Beispiel die Bäume, die zu Beginn der Modellierung im Modellgebiet vorhanden sein sollen als ein Gruppe und jene, die in jedem Zeitschritt als neue Bäume hinzukommen in einer anderen Gruppe definiert werden. In diesem Setup gibt es genau diese zwei Gruppen.

Der Punkt "species" gibt die Art der Bäume an. Momentan ist hier nur die graue Mangrove (Avicennia marina) mit der Klasse "avicennia" auswählbar.

Unter "distribution" wird die Verteilung der Bäume, also die räumliche Anordnung im Modellgebiet, bestimmt. Unter "type" kann diese entweder mit "GroupFromFile" aus einer Datei ausgelesen werden oder - wie in diesem Setup - mit "random" zufällig angeordnet werden. Unter "domain" wird das Modellgebiet festgelegt. Die Koordinatenwerte mit den Indizes "1" definieren dabei die numerisch niedrigeren Werte, die Indizes "2" die numerisch höheren. Mit "n_individuals" kann die Anzahl an Bäumen, die zu Beginn der Modellierung im Modell vorhanden sein soll und mit "n_recruitment_per_step" die Anzahl an Bäumen, die zu jedem Zeitschritt als junge Bäume dem Modell hinzugefügt werden soll. In der Gruppe "Recruiting" ist "n_individuals" auf Null gesetzt, "n_recruitment_per_step" auf 30. Hieran lässt sich also erkenn, dass diese erste Gruppe dazu dient, neue Bäume über die gesamte Modelllaufzeit zu integrieren. Da "n_individuals" zwingend angegeben werden muss, "n_recruitment_per_step" aber optional ist, wird in der zweiten Gruppe "Inital" nur noch "n_individuals" mit 30 angegeben. Zu Beginn der Modellierung sollen also 30 Bäume zufällig im Modellgebiet verteilt vorhanden sein.

Im Quellcode finden sich die für die Modellierung des Hinzukommens von neuen Bäumen ins Modell benötigten Dateien unter ./PopulationLib. 

## tree_time_loop

Hier wird das Modell zeitlich diskretisiert.

Zur Verfügung steht für "type" momentan nur "simple". Hierbei sind alle Zeitschritte über die gesamte Modellierung gleich groß. Angegeben werden müssen die Startzeit ("t_start"), Endzeit ("t_end") und die Zeitschrittlänge ("delta_t").

## visualization

In diesem Setup ist eine Visualisierung der Modellierung während eines Modelllaufs ausgeschaltet. Für den Punkt "type" wird hierzu "NONE" gewählt. Mit "SimplePypolot" würde die Position und der Kronenradius von Bäumen in Echtzeit mit Hilfe der matplotlib visualisiert werden.

## tree_output

Im letzten Abschnitt wird die Speicherung der Modellergebnisse festgelegt.

Hierfür gibt es drei verschiedene Möglichkeiten die unter "case" angegeben werden: "NONE" speichert keine Ergebnisse, mit "OneTimestepOneFile" wird pro Zeitschritt eine Datei mit der Baumpopulation gespeichert und mit "OneTreeOneFile" wird für jeden im Modell vorhandenen Baum eine eigene Datei abgespeichert. Der Dateipfad wird unter "output_dir" angegeben. Dieser muss vorhanden und leer sein, andernfalls startet die Modellierung nicht. Mit den Punkten "geometry_output" können geometrische Maße der Output-Datei hinzugefügt werden. Die in diesem Setup gewählten Variablen sind "r_stem" (Stammradius), "h_stem" (Stammhöhe), "r_crown" (Kronenhöhe) und "r_root" (Wurzelradius). Mit dem letzten Punkt "growth_output" können Informationen aus dem Baumwachstumskonzept ausgegeben werden. Alle Informationen die der Output-Datei hinzugefügt werden können lassen sich unter ./TreeModelLib/GrowthAndDeathDynamics/SimpleBettina/SimpleBettina.py Zeile 35 ff. einsehen.

# Input_OGS

Im Ordner "Input_OGS" befinden sich, wie schon zu Beginn erwähnt, Eingangsdateien für die Grundwassermodellierung mit OpenGeoSys.

## EXM_Jan-Jul_2019.txt

Diese Datei enthält detailierte Informationen zum Tidenhub.

## complete_boundary.vtu

Zusammenfassung aller Randbedingungen.

## constant_contributions.npy

## left_boundary.vtu

Informationen zur Randbedingung am linken Rand des Grundwassermodells.

## python_script.py

## quad.vtu

Volumen des Modellraums.

## right_boundery.vtu

Informationen zur Randbedingung am rechten Rand des Grundwassermodells.

## source_domain.vtu

Räumliche Diskretisierung des Modellgebiets.

## testbulk.vtu

## testmodel.prj

Was das xml-File für pyMANGA, ist das prj-File für OGS: die Steuerdatei. Hier können verschiedene Input-Dateien angegeben werden und Parameter definiert werden. Eigenschaften zum Untergrund und des Fluids wie die Porosität oder die Dichte werden zum Beispiel von OGS aus dieser Datei ausgelesen. 

## top_boundery.vtu

Informationen zur Randbedingung am oberen Rand des Grundwassermodells.
