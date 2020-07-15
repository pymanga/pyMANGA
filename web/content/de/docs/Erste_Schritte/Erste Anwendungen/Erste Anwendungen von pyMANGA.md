---
title: "Erste Anwendungen von pyMANGA"
linkTitle: "Erste Anwendungen von pyMANGA"
weight: 3
description: >

## Erste Anwendungen von pyMANGA 
Bevor Sie mit den ersten Anwendungen beginnen, sollten Sie falls noch nicht geschehen die Anleitungen Installation und Vorbereitung für ihr entsprechendes Betriebssystem durchgehen, diese wird vor allen für Anfänger empfohlen, welche wenig Erfahrung mit Python und der Eingabekonsole haben. Diese Anleitung ist für alle drei Betrebsyteme (MacOS, Unbunt, Windows) geeignet, bei Besonderheiten in der Ausführung auf den jeweiligen Systemen sind Anmerkungen zu finden.   

![Bildtext]("ausgeführte main_py Datei in der Eingabekonsole")

Abbildung 1: ausgeführte main.py Datei in der Eingabekonsole.

Hier ist zu sehen, dass die *main.py* Datei ausgeführt wurde und auf weitere Eingaben wartet. Damit ist der Start von MANGA geglückt und Sie können ein paar erste Verwendungsbeispiele testen. Dazu können Sie folgenden Code eingeben (siehe Abbildung 2).
•	py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xml		[1]

*-i* beschreibt dabei den Index bzw. den Pfad der Datei, in der der Input definiert ist, der für dieses Beispiel verwendet werden soll.   


![Bildtext]("Fehlermeldung beim Aufführen von py main.py")

Abbildung 2: Fehlermeldung beim Aufführen von *py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xml*.

Nach Ausführung des Codes wird eine Fehlermeldung ausgegeben, welche beschreibt, dass ein Ordner Namens *testoutputs* nicht existiert, welcher aber vom Programm benötigt wird, um die erzeugten Daten der Simulation abzuspeichern. Diese Information findet sich in der Datei *AllSimple_WithOutput.xml*, welche den Input für unser Beispiel definiert. Um diese einsehen zu können, müssen Sie die Datei mit Hilfe des Editors öffnen. Dazu folgen Sie dem in Abbildung 2 angegeben Dateipfad im Ordner *pyMANGA-master* und machen einen Rechtsklick auf die genannte Datei, gehen auf *Öffnen mit* und suchen den Editor raus (siehe Abbildung 3).


![Bildtext]("Inhalt von AllSimple_WithOutput.xml, geöffnet mit dem Text Editor")

Abbildung 3: Inhalt von AllSimple_WithOutput.xml, geöffnet mit dem Text Editor.

In der Datei finden sich die rot-markierten Zeilen, welche angeben was vom Programm ausgegeben werden soll, z.B. die Baumhöhe (h_stem) und wo hin, nämlich in den nicht existenten Ordner *testoutputs*, welcher als Ausgabeort für die Simulationsergebnisse definiert wurde. Demzufolge müssen Sie nun diesen Ordner erstellen. Dazu machen Sie einen Rechtsklick in den Unterordner *C:\Users\chris\Desktop\pyMANGA-master\ProjectLib\ExampleSetups*, klicken auf Neuen Ordner erstellen und nennen ihn testoutputs (siehe Abbildung 4).

![Bildtext]("Erstellung des neuen Ordner testoutputs")

Abbildung 4: Erstellung des neuen Ordner *testoutputs*.

Im Anschluss führen Sie den Code 1 erneut in der Eingabeaufforderung aus. Nun sollte das Programm die erste Simulation starten (siehe Abbildung 5). Es gibt verschiedene input Parameter, welche im MANGA eingestellt werden können. Eine Beschreibung dieser Parameter findet sich auf der folgenden Internetseite [Link](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html "https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html").Die Ergebnisse der Simulation werden einmal visuell in einem separaten Fenster dargestellt (siehe Abbildung 6) und in Form von *csv* Dateien im neu angelegten Ordner *testoutputs*. Damit haben Sie erfolgreich das erste Beispiel durchgeführt. 

![Bildtext]("Widerholte Aufführung von py main.py -i ProjectLibExampleSetupsAllSimple_WithOutput.xml nach erstellung den neuen Ordner testoutputs")

Abbildung 5: Widerholte Aufführung von *py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xml* nach erstellung den neuen Ordner *testoutputs*.

![Bildtext]("Visuelle Ergebnisse der Simulation)

Abbildung 6: Visuelle Ergebnisse der Simulation.

Analog dazu können Sie mit den folgenden Codes zwei weitere Beispiel ausprobieren, in dem andere Input-Varianten definiert sind. Dazu müssen Sie aber zunächst den Ordner *testoutputs* leeren bzw. einen anderen Ordner in den Input-Dateien mit Hilfe des Editors definieren, da das Programm die alten Output-Daten nicht überschreiben kann. Anschließend geben Sie wieder den Code in die Eingabeaufforderung ein.Des Weiteren wurden wiederum andere Parameter verändern. Verschaffen Sie sich mit Hilfe der Internetseite [Link](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html "https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html") einen Überblick über die Einstellungsvarianten der Input-Parameter, die in den Beispielen verwendet worden und vergleichen Sie sie.       
•	py main.py -i ProjectLib\ExampleSetups\FIXEDSAL_BETTINA.xml 		[2] 
•	py main.py -i ProjectLib\ExampleSetups\FON_SAZOI_KIWI.xml		[3]

Aufgrund von anderen Input-Varianten (in *FIXEDSAL_BETTINA.xml und FON_SAZOI_KIWI.xml*) wird unteranderem im Beispiel zu Code 3 keine visuelle Darstellung ausgegeben (vergleiche Abbildung 6).      
