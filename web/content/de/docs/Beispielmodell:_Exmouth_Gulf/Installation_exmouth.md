---
title: "Installation des Modellsetups"
linkTitle: "Installation des Setups"
weight: 3
description:
---

Das Modellsetup kann hier -Link folgt nach Absprache- heruntergeladen werden. Der Ordner kann an einer beliebigen Stelle entpackt werden, es bietet sich aber zum Beispiel die Hauptebene der pyMANGA-Installation an.

Um einen Modelllauf mit dem Setup auf dem eigenen Rechner zu starten müssen nun im wesentlichen Dateipfade, die auf Input-Dateien zeigen, im XML-Steuerfile angepasst werden. Alle Dateipfade im Steuerfile werden absolut angegeben, jeder Pfad beginnt also unter Ubuntu mit "/home/..." und unter Windows mit dem Buchstaben des Laufwerks. Bei Installation des Setup-Ordners in die pyMANGA-Hauptebene finden Sie ausgehend von derer die Datei also unter dem Dateipfad "

	./Study_Site_Exmouth_Gulf/setup_pymanga.xml.

Im Steuerfile (setup_pymanga.xml) muss der Dateipfad für die Ausgabe der Modellergebnisse (Zeile 76) und der Ordner mit den OGS-Input-Dateien angegeben werden (Zeile 18). Als Ausgabeort können Sie einen individuellen Dateispeicherort wählen; wichtig ist nur, dass dieser Ordner auch existiert und leer ist - pyMANGA erstellt nicht vorhandene Ausgabeorte nicht automatisch.

Ein Beispiel für den Ausgabeort der Ergebnisse und dem Ordner mit den OGS-Input Dateien könnte also wie folgt aussehen:

	/home/Dokumente/pyMANGA-master/Study_Site_Exmouth_Gulf/output

	/home/Dokumente/pyMANGA-master/Study_Site_Exmouth_Gulf/Input_OGS


Die Grundwassermodellierung mit OGS wird mit Hilfe eines zusätzlichen Python-Scripts detaillierter ausgeführt. Dieses Skript stellt für OGS unter anderem Werte zum Tidenhub aus der Datei "EXM_Jan-Jul_2019.txt" bereit, setzt diese Daten ein eine Schleife (da der Modellierungszeitraum deutlich länger als der Zeitraum der Tide-Daten ist) und sorgt für eine Anpassung des mittleren Wasserspiegels. Im Python-Script findet sich ein Verweis auf den Dateispeicherort dieser Datei, in Zeile 140 f. muss der Dateispeicherort der "EXM_Jan-Jul_2019.txt"-Datei an das jeweilige Dateisystem angepasste werden.

Das Programm lässt sich jetzt durch das Öffnen eines Terminals in der Hauptebene von pyMANGA durch Eingabe des Befehls 

	python3 main.py -i /Model_Exmouth_Gulf/setup_pymanga.xml

starten. Falls der Standardname des Ordners des Setups ("Model_Exmouth_Gulf") geändert wurde oder das Setup nicht in der pyMANGA-Hauptebene installiert wurde muss der Verweis auf den Dateispeicherort der Steuerdatei entsprechend angepasst werden. Die allgemeine Form würde also so aussehen:

	python3 absolute/path/to/main.py -i absolute/path/to/Model_Exmouth_Gulf/setup_pymanga.xml
