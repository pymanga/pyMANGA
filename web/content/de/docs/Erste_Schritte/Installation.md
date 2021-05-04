---
title: "Installation von pyMANGA"
linkTitle: "Installation von pyMANGA"
weight: 1
description:
---
<head>
<style type="text/css">
<!--
details summary {color: white; background: #00305E; margin-bottom: 1em;}
-->
</style>
</head>

Die Software **pyMANGA** stellt eine Kopplung zwischen einem Baumwachstums- und einem Grundwassermodellierungsprogramm dar.
Für die Modellierung des Pflanzenwachstums findet die Software **Bettina** und für die Modellierung des Grundwassers die Software <a href="https://www.opengeosys.org/" target="_blank">**OpenGeoSys**</a> Anwendung. 

Da das Baumwachstumsmodell und die Kopplung zwischen den beiden Programmen in **Python** geschrieben sind, wird zur Ausführung des Programms **pyMANGA** ein **Python-Compiler** benötigt.
Bei der Installation wird eine lokale Bibliothek mit verschiedenen **Python-Modulen** auf Ihrem Rechner installiert.
Diese Module beinhalten aufwendig zu formulierenden oder häufig gebrauchten Quellcode - somit muss dieser im Programm nicht ausformuliert geschrieben werden, sondern kann einfach aus der Bibliothek abgerufen werden.
Da sich die Installation zwischen den Betriebssystem unterscheidet, wählen Sie nachfolgend Ihr Betriebssystem aus.

Um **pyMANGA** (Mangrove groundwater salinity feedback model) ausführen zu können, muss eine **Python 3-Distribution** installiert sein.
Da sich die Systemvoraussetzungen zwischen den verschiedenen Betriebssystemen stark unterscheiden, wird die Installation für jedes Betriebssystem separat beschrieben.

<details>
<summary>Installation von Python in Ubuntu</summary>
<p>

**Ubuntu 18.04** liefert eine erste Installation von (**Python 2** und) **Python 3** von Haus aus mit.
Um zu überprüfen welche Version sich aktuell auf dem Rechner befindet, kann, nachdem ein neues Terminal-Fenster mit der Tastenkombination **"STRG + Alt + T"** geöffnet wurde, eine Versionsabfrage mit dem Kommando 

	• python3 -V 

erfolgen.
Es wird empfohlen das Paketverzeichnis des Betriebssystems zunächst zu updaten.
Um die Version auf den neuesten Stand zu bringen, kann über die Kommandos 

	• sudo apt update
 
und 

	• sudo apt -y upgrade 

das gesamte System geupdated werden - und damit auch das **Python 3**-Paket.
Die aktualliesierte Version kann erneut über 

	• python3 -V

eingesehen werden.

Falls widererwartens Probleme auftreten, kann über den Befehl

	• sudo apt-get install python3

das Paket (neu)installiert werden.
</p>
</details>


<details>
<summary>Installation von Python in Windows</summary>
<p>

Um **pyMANGA** (Mangrove groundwater salinity feedback model) ausführen zu können, müssen Sie zunächst sich ein **Interpreter** für die Programmiersprache **Python** besorgen.
Ein Beispiel wäre **python<sup>T</sup><sup>M</sup>**.
Dazu öffnen Sie Ihren **Browser** und gehen Sie auf die Seite ***Python.org***.
Im Auswahlmenü unter ***Download*** finden Sie die aktuelle Release Version für ihr Betriebssystem von **Python** (in dieser Anleitung wird das Vorgehen unter Windows beschrieben, siehe <a href="/de/docs/erste_schritte/installation/#Abbildung_1">Abbildung 1</a>).

<figure>
<a name="Abbildung_1"></a>
<img src="/pictures/getting_started/installation_of_pymanga/download_python_windows_1.jpg">
<figcaption><font size = "1"><i><b>Abbildung 1:</b> Auswahl Menü zum Downloaden der Windows Variante von python<sup>T</sup><sup>M</sup>.</i></font></figcaption>
</figure><p>

<figure>
<a name="Abbildung_2"></a>
<img src="/pictures/getting_started/installation_of_pymanga/download_python_windows_2.jpg">
<figcaption><font size = "1"><i><b>Abbildung 2:</b> zu wählender Link für das Downloaden von python-3.7.7.</i></font></figcaption>
</figure><p>

Führen Sie die herunter geladene Datei (***python-3.7.7-amd64.exe***) aus, wie eine normale **Windows** **exe** und installieren Sie sie auf Ihren Rechner <a href="/de/docs/erste_schritte/installation/#Abbildung_3">Abbildung 3</a>

<figure>
<a name="Abbildung_3"></a>
<img src="/pictures/getting_started/installation_of_pymanga/installation_python_windows.jpg.jpg" alt="Abbildung 3">
<figcaption><font size = "1"><i><b>Abbildung 3:</b> Ausführung der Windows exe von Python 3.7.7.</i></font></figcaption>
</figure><p>

Damit ist die Installation von **Python** abgeschlossen.

</p>
</details>


Nachdem Sie Python auf Ihrem Rechner eingerichtet haben, wird im nächsten Schritt pyMANGA installiert.
Dies können Sie entweder durch Klonen des [git-repositories](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") (Für Fortgeschrittene) oder durch Befolgen der nachfolgenden Anleitung erreichen. 
</p>

<details>
<summary>Installation von pyMANGA in Ubuntu <a name="Installation_Ubuntu"></a></summary>
<p>

Um **pyMANGA** ausführen zu können, müssen ggf. noch nicht in der **Python-Bibliothek** vorhandene, aber von **pyMANGA** benötigte Module installiert werden.
Da bei **Ubuntu** auch im Betriebssystem **Python** eine wichtige Rolle spielt, ist die bereits vorinstallierte Bibliothek sehr umfangreich.
Es wird deshalb empfohlen das Programm zunächst zu installieren und ggf. noch fehlende Module nach erster Ausführung des Programms zu installieren - **pyMANGA** weist sie darauf hin, welche Module benötigt werden.

Um die Software zu downloaden laden Sie sich die aktuelle Version als zip-Datei über diese [Homepage](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") herunter.

<figure>
<a name="Abbildung_4"></a>
<img src="/pictures/getting_started/installation_of_pymanga/download_pymanga_ubuntu.png">
<figcaption><font size = "1"><i><b>Abbildung 4:</b> Download von <b>pyMANGA</b> als zip-Datei</i></font></figcaption>
</figure><p>

Diese zip-Datei muss nun an einem beliebigem Speicherort entpackt werden.
Achten Sie darauf, dass sich keine Leerzeichen und keine Umlaute in dem Dateifpad befinden.

Das Programm ist jetzt ausführbar.
Öffnen Sie mit der Tastenkombination **Strg + Alt + T** ein Terminalfenster und navigieren Sie in die Hauptebene des Programms.
Alternativ können Sie auch den grafischen Weg wählen, indem Sie über Dateien zu dem Speicherort navigieren.
Dort können Sie die Konsole über einen Rechtsklick und in dem sich öffnenden Menü über das Feld "In Terminal öffnen" ein Terminalfenster öffnen, indem Sie sich bereits in der Hauptebene des Programms befinden.

Durch die Eingabe

	• python3 main.py

wird das Programm nun gestartet.
Falls **pyMANGA** aufgrund von fehlenden Modulen in der lokalen **Python-Bibliothek** - wie zu Anfang erwähnt - noch nicht ausgeführt werden kann, wird jeweils eines der fehlenden Pakete in einer Fehlermeldung ausgegeben.
Für die Installation von Python-Modulen eignet sich unter anderem **pip** ("Pip installs Python").
Durch das öffnen eines Terminalfenster (Tastenkombination **Strg + Alt + T**) und der Eingabe des Befehls

	• sudo apt-get install python3-pip

lässt sich pip installieren.

Um mit pip nun ein **Python-Modul** in die Bibliothek hinzuzufügen muss folgender Befehl in ein Terminal eingegeben werden:

	• pip3 install Name_des_Moduls

Sollten keine manuellen Veränderungen an der Standard-Python-Bibliothek vorgenommen worden sein, fehlen die Module "numpy", "vtk", "lxml" und "matplotlib" zur Ausführung von **pyMANGA**.
Diese müssen alle der Reihe nach installiert werden, der erste Befehl würde für das Modul "numpy" also folgendermaßen aussehen:

	• pip3 install numpy

Eine Außnahme stellt lediglich das Modul "vtk" dar. Um später Berechnung mit pyMANGA durchführen zu können, bei denen auch die **Grundwasserströmung** berücksichtigt wird, wird für dieses Modul **eine bestimmte Version** benötigt.
Soll nicht die aktuellste Version eines Moduls mit pip installiert werden, sieht der Befehl hierfür so aus:

	• pip3 install vtk==8.1.2

Nachdem die fehlenden Modul installiert wurden, starten Sie pyMANGA erneut.
Sollten jetzt noch weitere **Python-Module** fehlen, wird **pyMANGA** wieder eines davon als fehlende Voraussetzung ausgeben.
Diesen Schritt wiederholen Sie so lange, bis alle Python-Module installiert sind.
Wenn das der Fall ist, sollte Sie folgende Ausgabe erhalten:


	Traceback (most recent call last):
	  File "main.py", line 26, in main
	    prj = XMLtoProject(xml_project_file=project_file)
	UnboundLocalError: local variable 'project_file' referenced before assignment
	
	During handling of the above exception, another exception occurred:
	
	Traceback (most recent call last):
	  File "main.py", line 38, in <module>
	    main(sys.argv[1:])
	  File "main.py", line 28, in main
	    raise UnboundLocalError('Wrong usage of pyMANGA. Type "python' +
	UnboundLocalError: Wrong usage of pyMANGA. Type "python main.py -h" for additional help.



Auch wenn Sie zunächst diese Fehlermeldung erhalten bedeutet es, dass **pyMANGA** richtig installiert und ausgeführt werden kann.
Die Berechnung eines ersten Beispiel-Setups wird im Abschnitt <a href="/de/docs/erste_schritte/erste_anwendungen_von_pyMANGA/">Erste Anwendungen von **pyMANGA**</a> dieses Tutorials erklärt.

</p>
</details>

<details>
<summary>Installation von pyMANGA in Windows</summary>
<p>

Um **pyMANGA** auszuführen zu können, müssen noch ein paar Module für den **Python** **Compiler** installiert werden.
Dazu müssen Sie die **Eingabeaufforderung** öffnen.
Diese finden Sie einfach über die Suche, indem Sie der **„Eingabeaufforderung“** eingeben und per **Mausklick** öffnen.
Da es sich bei **pyMANGA** um ein Zeilenprogramm handelt, spielt sich alles in der **Eingabeaufforderung** ab (siehe <a href="/de/docs/erste_schritte/installation/#Abbildung_5">Abbildung 5</a>). 

<figure>
<a name="Abbildung_5"></a>
<img src="/pictures/getting_started/installation_of_pymanga/open_command_prompt.jpg">
<figcaption><font size = "1"><i><b>Abbildung 5:</b> öffnen der Eingabeaufforderung.</i></font></figcaption>
</figure><p>

Nun müssen die folgenden **Module** ***numpy***, ***vtk***, ***lxml*** und ***matplotlib*** installiert werden.
Wir beginnen mit dem **Modul** ***numpy***.
Geben Sie den aufgezeigten Code in die **Eingabeaufforderung**, um das **Modul** zu installieren (siehe <a href="/de/docs/erste_schritte/installation/#Abbildung_6">Abbildung 6</a>). 

	• py -3.7 -m pip install numpy								    [1]

<figure>
<a name="Abbildung_6"></a>
<img src="/pictures/getting_started/installation_of_pymanga/install_numpy_windows.jpg">
<figcaption><font size = "1"><i><b>Abbildung 6:</b> Beispielhafte Installation des Moduls numpy.</i></font></figcaption>
</figure><p>

Führen Sie dies analog für die drei anderen **Module** aus mit dem folgenden Code

	• py -3.7 -m pip install vtk								     [2]
	• py -3.7 -m pip install lxml							  	     [3]
	• py -3.7 -m pip install matplotlib							     [4]

Hinweis: Sollte die **Eingabeaufforderung** eine Wahrung ausgeben, dass ***pip*** nicht aktuell ist, können Sie mit **upgrade** ***pip*** dies aktualisieren.
Dies ist aber nicht zwingend erforderlich.

Zur Erklärung was Sie eingegeben haben: ***py*** bedeuten, dass Sie **Python** aufrufen.
Dabei ist **-3.7** die Version, die Sie nutzen.
Mit ***-m*** wird ein Modul aufgerufen, in diesem Fall ***pip***, welches dazu dient andere **Module** zu installieren.
Zum Schluss folgt der **Modul** **Name** vom zu installierendem **Modul**.
Nun sind die Vorbereitungen für die Nutzung des **Compilers** abgeschlossen.
Als nächsten Schritt müssen Sie, falls es noch nicht geschehen ist, das Programm **pyMANGA** downloaden.
Dazu gehen Sie auf die folgende [Homepage](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") und downloaden das Programm als zip Datei und speichern es auf Ihren Rechner (siehe <a href="/de/docs/erste_schritte/installation/#Abbildung_7">Abbildung 7</a>).

<figure>
<a name="Abbildung_7"></a>
<img src="/pictures/getting_started/installation_of_pymanga/download_pymanga_windows.jpg">
<figcaption><font size = "1"><i><b>Abbildung 7:</b> Download von pyMANGA.</i></font></figcaption>
</figure><p>

Anschließend entpacken Sie die Datei (***pyMANGA-master.zip***) auf Ihren Desktop.
Sie enthält sämtliche Programmbestandteile von **pyMANGA** unter anderem ***main.py***, welche die Ausführungsdatei darstellt, die zum Ausführen des Programmes aufgerufen werden muss.
Dazu muss Sie nun dem **Ordner** öffnen und mit **Rechtsklick** in einem leeren Bereich des **Ordners** die **Eingabeaufforderung** öffnen (siehe <a href="/de/docs/erste_schritte/installation/#Abbildung_8">Abbildung 8</a>) und den folgenden Code eingeben.

	• py main.py -h										     [5]

Hierbei bedeutet wiederum ***py*** das Python aufgerufen wird, ***main.py*** stellt die Datei dar, die aufgerufen werden soll, und ***-h*** ruft die Hilfe auf.

<figure>
<a name="Abbildung_8"></a>
<img src="/pictures/getting_started/installation_of_pymanga/open_command_prompt_folder.jpg">
<figcaption><font size = "1"><i><b>Abbildung 8:</b> öffnen der Eingabeaufforderung im pyMANGA Ordner.</i></font></figcaption>
</figure><p>

Hinweis: Die **Eingabeaufforderung** wird im **Ordner** aufgerufen, damit der ***Ordnerpfad*** nicht jedes Mal mit eingegeben werden muss.
Unter Windows 10 ist dies nur möglich, wenn Sie sich ***cmd in Kontextmenü hinzufügen.zip*** von der folgenden [Homepage](https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die-eingabeaufforderung-im-kontextmenue-anzeigen/ "https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die- eingabeaufforderung-im-kontextmenue-anzeigen/") herunterladen und wie auf der Seite beschrieben ausführen.
Alternativ ist es möglich in **Eingabeaufforderung**, die Sie in der Windows Suche mit dem **Suchbegriff** **„Eingabeaufforderung“** finden, zu nutzen und den vollständigen Dateipfad anzugeben, der in diesem Beispiel wie folgt lautet ***C:\Users\...\Desktop\pyMANGA-master***.
Um Ihren Dateipfad herauszufinden machen Sie einen **Rechtsklick** auf den **Ordner** ***pyMANGA-master*** und gehen Sie auf **Eigenschaften**.
Hier finden sich die Angaben zum Ort des Ordners an den Sie noch mit eine \ den **Namen** des **Ordners** anhängen müssen.

</p>
</details>
