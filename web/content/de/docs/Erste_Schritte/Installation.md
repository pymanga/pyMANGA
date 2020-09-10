---
title: "Installation von pyMANGA"
linkTitle: "Installation von pyMANGA"
weight: 1
description:
---

Die Software pyMANGA stellt eine Kopplung zwischen einem Baumwachstums- und einem Grundwassermodellierungsprogramm dar. Da das Baumwachstumsmodell und die Kopplung zwischen den beiden Programmen in Python geschrieben sind, wird zur Ausführung des Programms pyMANGA ein Python-Compiler benötigt. Bei der Installation wird eine lokale Bibliothek mit verschiedenen Python-Modulen auf Ihrem Rechner installiert. Diese Module beinhalten aufwendig zu formulierenden oder häufig gebrauchten Quellcode - somit muss dieser im Programm nicht ausformuliert geschrieben werden, sondern kann einfach aus der Bibliothek abgerufen werden. Da sich die Installation zwischen den Betriebssystem unterscheidet, wählen Sie nachfolgend Ihr Betriebssystem aus.

<details>
<summary>Installation von Python in Ubuntu</summary>
<p>

</p>
</details>


<details>
<summary>Installation von Python in Ubuntu Windows</summary>
<p>

Um MANGA (Mangrove groundwater salinity feedback model) ausführen zu können, müssen Sie zunächst sich ein Interpreter für die Programmiersprache Python besorgen. Ein Beispiel wäre python<sup>T</sup><sup>M</sup>. Dazu öffnen Sie Ihren Browser und gehen Sie auf die Seite *Python.org.* Im Auswahlmenü unter *Download finden* Sie die aktuelle Release Version für ihr Betriebssystem von Python (in dieser Anleitung wird das Vorgehen unter Windows beschrieben, siehe Abbildung 1).

<figure>
<img src="/pictures/Auswahl_Menue_zum_Downloaden_der_Windows_Variante_von_pythonTM.jpg">
<figcaption><font size = "1"><i><b>Abbildung 1:</b> Auswahl Menü zum Downloaden der Windows Variante von python<sup>T</sup><sup>M</sup>.</i></font></figcaption>
</figure><p>

<figure>
<img src="/pictures/zu_waehlender_Link_für_das_Downloaden_von_python-3_7_7.jpg">
<figcaption><font size = "1"><i><b>Abbildung 2:</b> zu wählender Link für das Downloaden von python-3.7.7.</i></font></figcaption>
</figure><p>

Führen Sie die herunter geladene Datei (*python-3.7.7-amd64.exe*) aus, wie eine normale Windows exe und installieren Sie sie auf Ihren Rechner (siehe Abbildung 3). 

<figure>
<img src="/pictures/Ausfuehrung_der_Windows_exe_von_Python_3_7_7.jpg">
<figcaption><font size = "1"><i><b>Abbildung 3:</b> Ausführung der Windows exe von Python 3.7.7.</i></font></figcaption>
</figure><p>

Damit ist die Installation Python abgeschlossen.

</p>
</details>

<details>
<summary>Installation von Python in Ubuntu MacOS</summary>
<p>
Hier steht der Inhalt zu MacOS
</p>
</details>

<br>
Nachdem Sie Python auf Ihrem Rechner eingerichtet haben, wird im nächsten Schritt pyMANGA installiert. 
</p>

<details>
<summary >Installation von pyMANGA in Ubuntu</summary>
<p>
Um Manga ausführen zu können, müssen ggf. noch nicht in der Python-Bibliothek vorhandene, aber von pyMANGA benötigte Module installiert werden. Da bei Ubuntu auch im Betriebssystem Python eine wichtige Rolle spielt, ist die bereits vorinstallierte Bibliothek sehr umfangreich. Es wird deshalb empfohlen das Programm zunächst zu installieren und ggf. noch fehlende Module nach erster Ausführung des Programms zu installieren - pyMANGA weist sie darauf hin, welche Module benötigt werden.

Um die Software zu downloaden laden Sie sich die aktuelle Version als zip-Datei über diese [Homepage](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") herunter.

<figure>
<img src="/pictures/ubuntu_download.png">
<figcaption><font size = "1"><i><b>Abbildung 1:</b> Download von pyMANGA als zip-Datei</i></font></figcaption>
</figure><p>

Diese zip-Datei muss nun an einem beliebigem Speicherort entpackt werden. Achten Sie darauf, dass sich keine Leerzeichen und keine Umlaute in dem Dateifpad befinden.

Das Programm ist jetzt ausführbar. Öffnen Sie mit der Tastenkombination Strg + Alt + T ein Terminalfenster und navigieren Sie in die Hauptebene des Programms. Alternativ können Sie auch den grafischen Weg wählen, indem Sie über Dateien zu dem Speicherort navigieren. Dort können Sie die Konsole über einen Rechtsklick und in dem sich öffnenden Menü über das Feld "In Terminal öffnen" ein Terminalfenster öffnen, indem Sie sich bereits in der Hauptebene des Programms befinden.

<figure>
<img src="/pictures/ubuntu_Hauptebene_pyMANGA.png">
<figcaption><font size = "1"><i><b>Abbildung 2:</b> Hauptebene von pyMANGA</i></font></figcaption>
</figure><p>

Durch die Eingabe "python main.py" wird das Programm nun gestartet. Die 13-zeilige Ausgabe des Programms gibt in der letzten Zeile folgende Fehlermeldung aus: "Wrong usage of pyMANGA. Type "python main.py -h". Auch wenn Sie zunächst diese Fehlermeldung erhalten bedeutet es, dass pyMANGA richtig installiert und ausgeführt werden kann. Die Berechnung eines ersten Beispiel-Setups wird im folgenden dieses kurzen Tutorials erklärt.

</p>
</details>

<details>
<summary>Installation von pyMANGA in Windows</summary>
<p>

Um MANGA auszuführen zu können, müssen noch ein paar Module für den Python Compiler installiert werden. Dazu müssen Sie die *Eingabeaufforderung* öffnen. Diese finden Sie einfach über die Suche, indem Sie der „Eingabeaufforderung“ eingeben und per Mausklick öffnen. Da es sich bei MANGA um ein Zeilenprogramm handelt, spielt sich alles in der Eingabeaufforderung ab (siehe Abbildung 1). 

<figure>
<img src="/pictures/oeffnen_der_Eingabeaufforderung.jpg">
<figcaption><font size = "1"><i><b>Abbildung 1:</b> öffnen der Eingabeaufforderung.</i></font></figcaption>
</figure><p>

Nun müssen die folgenden Module *numpy*, *vtk*, *lxml* und *matplotlib* installiert werden. Wir beginnen mit dem Modul *numpy*. Geben Sie den aufgezeigten Code in die Eingabeaufforderung, um das Modul zu installieren (siehe Abbildung 2). 

	• py -3.7 -m pip install numpy								     [1]

<figure>
<img src="/pictures/Beispielhafte_Installation_des_Moduls_numpy.jpg">
<figcaption><font size = "1"><i><b>Abbildung 2:</b> Beispielhafte Installation des Moduls numpy.</i></font></figcaption>
</figure><p>

Führen Sie dies analog für die drei anderen Module aus mit dem folgenden Code

	• py -3.7 -m pip install vtk								     [2]
	• py -3.7 -m pip install lxml							  	     [3]
	• py -3.7 -m pip install matplotlib							     [4]

Hinweis: Sollte die Eingabeaufforderung eine Wahrung ausgeben, dass *pip* nicht aktuell ist, können Sie mit upgrade *pip* dies aktualisieren. Dies ist aber nicht zwingend erforderlich.

Zur Erklärung was Sie eingegeben haben: *py* bedeuten, dass Sie Python aufrufen. Dabei ist -3.7 die Version, die Sie nutzen. Mit *-m* wird ein Modul aufgerufen, in diesem Fall *pip*, welches dazu dient andere Module zu installieren. Zum Schluss folgt der Modul Name vom zu installierendem Modul. Nun sind die Vorbereitungen für die Nutzung des Compilers abgeschlossen. Als nächsten Schritt müssen Sie, falls es noch nicht geschehen ist, das Programm MANGA downloaden. Dazu gehen Sie auf die folgende Internetseite [Link](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") und downloaden das Programm als zip Datei und speichern es auf Ihren Rechner (siehe Abbildung 3).

<figure>
<img src="/pictures/Download_von_pyMANGA.jpg">
<figcaption><font size = "1"><i><b>Abbildung 3:</b> Download von pyMANGA.</i></font></figcaption>
</figure><p>

Anschließend entpacken Sie die Datei (*pyMANGA-master.zip*) auf Ihren Desktop. Sie enthält sämtliche Programmbestandteile von MANGA unter anderem *main.py*, welche die Ausführungsdatei darstellt, die zum Ausführen des Programmes aufgerufen werden muss. Dazu muss Sie nun dem Ordner öffnen und mit Rechtsklick in einem leeren Bereich des Ordners die Eingabeaufforderung öffnen (siehe Abbildung 4) und den folgenden Code eingeben.

	• py main.py -h										     [5]

Hierbei bedeutet wiederum *py* das Python aufgerufen wird, *main.py* stellt die Datei dar, die aufgerufen werden soll, und -h ruft die Hilfe auf.

<figure>
<img src="/pictures/oeffnen_der_Eingabeaufforderung_im_pyMANGA_Ordner.jpg">
<figcaption><font size = "1"><i><b>Abbildung 4:</b> öffnen der Eingabeaufforderung im pyMANGA Ordner.</i></font></figcaption>
</figure><p>

Hinweis: Die Eingabeaufforderung wird im Ordner aufgerufen, damit der Ordnerpfad nicht jedes Mal mit eingegeben werden muss. Unter Windows 10 ist dies nur möglich, wenn Sie sich *cmd in Kontextmenü hinzufügen.zip* von der folgenden Internetseite [Link](https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die-eingabeaufforderung-im-kontextmenue-anzeigen/ "https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die- eingabeaufforderung-im-kontextmenue-anzeigen/")  herunterladen und wie auf der Seite beschrieben ausführen. Alternativ ist es möglich in Eingabeaufforderung, die Sie in der Windows Suche mit dem Suchbegriff „Eingabeaufforderung“ finden, zu nutzen und den vollständigen Dateipfad anzugeben, der in diesem Beispiel wie folgt lautet *C:\Users\...\Desktop\pyMANGA-master*. Um Ihren Dateipfad herauszufinden machen Sie einen Rechtsklick auf den Ordner *pyMANGA-master* und gehen Sie auf Eigenschaften. Hier finden sich die Angaben zum Ort des Ordners an den Sie noch mit eine \ den Namen des Ordners anhängen müssen.

</p>
</details>

<details>
<summary>Installation von pyMANGA in MacOS</summary>
<p>
Hier steht der Inhalt zu MacOS
</p>
</details>
