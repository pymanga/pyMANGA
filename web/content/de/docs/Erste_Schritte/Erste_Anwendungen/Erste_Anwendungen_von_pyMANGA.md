---
title: "Erste Anwendungen von pyMANGA"
linkTitle: "Erste Anwendungen von pyMANGA"
weight: 3
description:
---
Bevor Sie mit den ersten Anwendungen beginnen, sollten Sie falls noch nicht geschehen die Anleitungen zur Installation und Vorbereitung für ihr entsprechendes Betriebssystem durchgehen, diese wird vor allen für Anfänger empfohlen, welche wenig Erfahrung mit Python und der Eingabekonsole haben. Diese Anleitung ist für alle drei Betrebsyteme (MacOS, Unbunt, Windows) geeignet, bei Besonderheiten in der Ausführung auf den jeweiligen Systemen sind Anmerkungen zu finden.   

<figure>
<img src="/pictures/ausgefuehrte_main_py_Datei_in_der_Eingabekonsole.jpg">
<figcaption><font size = "1"><i><b>Abbildung 1:</b> Ausgeführte main.py Datei in der Eingabekonsole.</i></font></figcaption>
</figure><p>

Hier ist zu sehen, dass die *main.py* Datei ausgeführt wurde und auf weitere Eingaben wartet. Damit ist der Start von MANGA geglückt und Sie können ein paar erste Verwendungsbeispiele testen. Dazu können Sie folgenden Code eingeben (siehe Abbildung 2).

	• py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xml			  [1]

*-i* beschreibt dabei den Index bzw. den Pfad der Datei, in der der Input definiert ist, der für dieses Beispiel verwendet werden soll.   

<figure>
<img src="/pictures/Fehlermeldung_beim_Aufuehren_von_py-main.py.jpg">
<figcaption><font size = "1"><i><b>Abbildung 2:</b> Fehlermeldung beim Auführen von <b>py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xml.</b></i></font></figcaption>
</figure><p>

Nach Ausführung des Codes wird eine Fehlermeldung ausgegeben, welche beschreibt, dass ein Ordner Namens *testoutputs* nicht existiert, welcher aber vom Programm benötigt wird, um die erzeugten Daten der Simulation abzuspeichern. Diese Information findet sich in der Datei *AllSimple_WithOutput.xml*, welche den Input für unser Beispiel definiert. Um diese einsehen zu können, müssen Sie die Datei mit Hilfe des Editors öffnen. Dazu erstellen Sie bitte das aufgeführte (siehe Abbildung 2) Verzeichnis. Der angegebene Dateipfad ist relativ zu dem Ordner, in dem sie pyMANGA gestarten haben, angegeben siehe (Abbildung 3). Dazu folgen Sie dem in Abbildung 2 angegeben Dateipfad im Ordner *pyMANGA-master* und machen einen Rechtsklick auf die genannte Datei, gehen auf *Öffnen mit* und suchen den Editor raus (siehe Abbildung 3).

<figure>
<img src="/pictures/Inhalt_von_AllSimple_WithOutput.xml,_geoeffnet_mit_dem_Text_Editor.jpg">
<figcaption><font size = "1"><i><b>Abbildung 3:</b> Inhalt von </b>AllSimple_WithOutput.xml</b>, geöffnet mit dem Text Editor.</i></font></figcaption>
</figure><p>

In der Datei finden sich die rot-markierten Zeilen, welche angeben was vom Programm ausgegeben werden soll, z.B. die Baumhöhe (h_stem) und wo hin, nämlich in den nicht existenten Ordner *testoutputs*, welcher als Ausgabeort für die Simulationsergebnisse definiert wurde. Demzufolge müssen Sie nun diesen Ordner erstellen. Dazu machen Sie einen Rechtsklick in den Unterordner *C:\Users\chris\Desktop\pyMANGA-master\ProjectLib\ExampleSetups*, klicken auf Neuen Ordner erstellen und nennen ihn testoutputs (siehe Abbildung 4).

<figure>
<img src="/pictures/Erstellung_des_neuen_Ordners_testoutputs.jpg">
<figcaption><font size = "1"><i><b>Abbildung 4:</b> Erstellung des neuen Ordners <b>testoutputst</b>.</i></font></figcaption>
</figure><p>

Im Anschluss führen Sie den Code 1 erneut in der Eingabeaufforderung aus. Nun sollte das Programm die erste Simulation starten (siehe Abbildung 5). Es gibt verschiedene input Parameter, welche in MANGA Projektkonfigurationen eingestellt werden können. Die Datei, welche soeben gestartet wurde ist eine Konfigurationsdatei. Eine Beschreibung dieser Parameter findet sich auf der folgenden Internetseite [Link](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html "https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html").Die Ergebnisse der Simulation werden einmal visuell in einem separaten Fenster dargestellt (siehe Abbildung 6) und in Form von *csv* Dateien im neu angelegten Ordner *testoutputs*. Damit haben Sie erfolgreich das erste Beispiel ausgeführt.

<figure>
<img src="/pictures/Widerholte_Ausfuehrung_von_py_main.py_-i_ProjectLibExampleSetupsAllSimple_WithOutput.xml_nach_erstellung_den_neuen_Ordner_testoutputs.jpg">
<figcaption><font size = "1"><i><b>Abbildung 5:</b> Widerholte Auführung von  <b>py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xmlt</b> nach Erstellung des neuen Ordners  <b>testoutputst</b>.</i></font></figcaption>
</figure><p>

<figure>
<a name="Abbildung_6"></a>
<img src="/pictures/Visuelle_Ergebnisse_der_Simulation.jpg">
<figcaption><font size = "1"><i><b>Abbildung 6:</b> Visuelle Ergebnisse der Simulation.</i></font></figcaption>
</figure><p>

Analog dazu können Sie mit den folgenden Codes zwei weitere Beispiel ausprobieren, in dem andere Input-Varianten definiert sind. Dazu müssen Sie aber zunächst den Ordner *testoutputs* leeren bzw. einen anderen Ordner in den Input-Dateien mit Hilfe des Editors definieren, da das Programm die alten Output-Daten nicht überschreiben kann. Anschließend geben Sie wieder den Code in die Eingabeaufforderung ein. Des Weiteren wurden wiederum andere Parameter verändern. Verschaffen Sie sich mit Hilfe der Internetseite [Link](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html "https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html") einen Überblick über die Einstellungsvarianten der Input-Parameter, die in den Beispielen verwendet worden und vergleichen Sie sie.       

	• py main.py -i ProjectLib\ExampleSetups\FIXEDSAL_BETTINA.xml 			         [2] 
	• py main.py -i ProjectLib\ExampleSetups\FON_SAZOI_KIWI.xml			         [3]

Aufgrund von anderen Projekt-Konfigurationen (in *FIXEDSAL_BETTINA.xml und FON_SAZOI_KIWI.xml*) wird unteranderem im Beispiel zu Code 3 keine visuelle Darstellung ausgegeben (vergleiche <a href="/de/docs/erste_schritte/erste_anwendungen/erste_anwendungen_von_pymanga/#Abbildung_6">Abbildung 6</a> ).    

Die nächste Anwendung von pyMANGA nutzt OpenGeoSys (OGS). Dabei handelt es sich um ein wissenschaftliches Open-Source-Projekt zur Entwicklung numerischer Methoden für die Simulation von thermo-hydro-mechanisch-chemischen (THMC) Prozessen in porösen und fragmentierten Medien. Um OGS zu nutzen müssen Sie dieses zunächst herunterladen und installieren. Dazu gehen Sie auf die folgende Internetseite [Link](https://www.opengeosys.org/releases/ "https://www.opengeosys.org/releases/")  und scrollen bis Sie die Version 6.3.0 finden und downloaden diese (siehe Abbildung 7 und 8).

<figure>
<a name="Abbildung_7"></a>
<img src="/de/static/Versionsauswahl_von_OGS.jpg">
<figcaption><font size = "1"><i><b>Abbildung 7:</b> Versionsauswahl von OGS.</i></font></figcaption>
</figure><p>

<figure>
<a name="Abbildung_8"></a>
<img src="/de/static/Download_von_OGS 6.3.0.jpg">
<figcaption><font size = "1"><i><b>Abbildung 8:</b> Download von OGS 6.3.0.</i></font></figcaption>
</figure><p>

Wählen Sie entsprechend ihres Betriebssystems die zu downloadende Datei aus.  Anschließend entpacken Sie die Zip Datei, kopieren den Bin Ordner und fügen diese in den pyMANGA-master Ordner in den folgenden Pfad ein (siehe Abbildung 9).

	\pyMANGA-master\TreeModelLib\BelowgroundCompetition\OGS					 [4]

<figure>
<a name="Abbildung_9"></a>
<img src="/de/static/Einfuegen_von_OGS_in_den_pyMANGA-master_Ordner.jpg">
<figcaption><font size = "1"><i><b>Abbildung 9:</b> Einfügen von OGS in den pyMANGA-master Ordner.</i></font></figcaption>
</figure><p>

<<<<<<< HEAD:web/content/de/docs/Erste_Schritte/Erste_Anwendungen/Erste_Anwendungen_von_pyMANGA.md
Aufgrund von anderen Projekt-Konfigurationen (in *FIXEDSAL_BETTINA.xml und FON_SAZOI_KIWI.xml*) wird unteranderem im Beispiel zu Code 3 keine visuelle Darstellung ausgegeben (vergleiche <a href="/de/docs/erste_schritte/erste_anwendungen/erste_anwendungen_von_pymanga/#Abbildung_6">Abbildung 6</a> ).    
=======
Damit ist OGS installiert. Um zu testen ob es ordnungsgemäß funktioniert, öffnen Sie den Bin Ordner, drücken shift und die rechte Maustaste und wählen PowerShell-Fenster hier öffnen (siehe Abbildung 10).

<figure>
<a name="Abbildung_10"></a>
<img src="/de/static/Test_ob_OGS_Ordnungsgemaeß_funktioniert.jpg">
<figcaption><font size = "1"><i><b>Abbildung 10:</b> Test ob OGS Ordnungsgemaeß funktioniert.</i></font></figcaption>
</figure><p>

Kopieren Sie den Pfad, der im PowerShell-Fenster angezeigt wird, und hängen Sie \OGS an und führen dies mit der Eingabetaste aus. In der folgenden Abbildung sehen Sie die Ausgabe des PowerShell-Fensters, wenn OGS reibungslos funktioniert. 

<figure>
<a name="Abbildung_11"></a>
<img src="/de/static/Ausgabe_bei_Ordnungsgemaeßer_Funktion_von_OGS.jpg">
<figcaption><font size = "1"><i><b> Abbildung 11:</b> Ausgabe bei Ordnungsgemäßer Funktion von OGS.</i></font></figcaption>
</figure><p>

Nun können Sie das nächste Anwendungsbeispiel starten, indem Sie wie gehabt die Eingabeaufforderung im pyMANGA-master Ordner öffnen und pyMANGA starten. Anschließend geben Sie den nachfolgenden Befehl ein (siehe Abbildung 12).

	py main.py -i ProjectLib\ExampleSetups\OGS3D_SAZOI_BETTINA.xml 				 [5]

<figure>
<a name="Abbildung_12"></a>
<img src="/de/static/zeigt_die_Ausfuehrung_des_Anwendungsbeispiels_mit_OGS.jpg">
<figcaption><font size = "1"><i><b>Abbildung 12:</b> zeigt die Ausführung des Anwendungsbeispiels mit OGS.</i></font></figcaption>
</figure><p>

Hinweis: Die Rechenzeit kann mehrere Stunden betragen. Dies können Sie reduzierten, indem Sie in der Datei GS3D_SAZOI_BETTINA unter folgenden Pfad \pyMANGA-master\ProjectLib\ExampleSetups öffnen und die folgende Zeile hinzufügen.

	<delta_t_ogs> 604800 </delta_t_ogs>							 [6]

Dabei kann 604800 variiert werden und entspricht hier eine Woche, somit wird nicht für jede Sekunde die Berechnungen durchgeführt, sondern nur pro Woche was die Rechenzeit deutlich reduziert(siehe Abbildung 13). 

<figure>
<a name="Abbildung_13"></a>
<img src="/de/static/Anpassung_zur_Rechenzeit_Verkuerzung.jpg">
<figcaption><font size = "1"><i><b>Abbildung 13:</b> Anpassung zur Rechenzeit Verkürzung.</i></font></figcaption>
</figure><p>
>>>>>>> 4d80603... OGS Beispiel hinzugefügt und ins Englische übersetz:web/content/de/docs/Erste_Schritte/Erste Anwendungen/Erste_Anwendungen_von_pyMANGA.md
