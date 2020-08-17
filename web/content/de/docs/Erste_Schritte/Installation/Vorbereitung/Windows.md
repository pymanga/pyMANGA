---
title: "Vorbereitungen zu Start von pyMANGA unter Microsoft Windows 10"
linkTitle: "Microsoft Windows"
weight: 3
description: >
---
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
