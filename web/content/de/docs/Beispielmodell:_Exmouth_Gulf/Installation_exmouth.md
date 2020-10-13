---
title: "Installation des Modellsetups"
linkTitle: "Installation des Setups"
weight: 3
description:
---

Das Modellsetup kann hier -Link folgt nach Absprache- heruntergeladen werden. Der Ordner wird in die Hauptebene der pyMANGA installation entpackt. 

Um einen Modelllauf mit dem Setup auf dem eigenen Rechner zu starten müssen nun im wesentlichen Dateipfade, die auf Input-Dateien zeigen, im XML-Steuerfile angepasst werden. Alle Dateipfade im Steuerfile werden absolut angegeben, jeder Pfad beginnt also unter Ubuntu mit "/home/..." und unter Windows mit dem Buchstaben des Laufwerks.

Im Steuerfile (setup_pymanga.xml) muss weiter der Dateipfad für die Ausgabe der Modellergebnisse (Zeile 76) und der Ordner mit den OGS-Input-Dateien angegeben werden (Zeile 18). Das Steuerfile finden Sie in der Hauptebene des Modellsetups. Als Ausgabeort können Sie einen individuellen Dateispeicherort wählen; wichtig ist nur, dass dieser Ordner auch existiert - pyMANGA erstellt nicht vorhandene Ausgabeorte nicht automatisch.

Die Grundwassermodellierung mit OGS wird mit Hilfe eines zusätzlichen Python-Scripts detaillierter ausgeführt. Dieses Skript führt OGS unter anderem Werte zum Tidenhub zu. In der Steuerdatei findet sich ein Verweis auf den Dateispeicherort dieser Datei. Bei Installation des Setup-Ordners in die pyMANGA-Hauptebene finden Sie ausgehend von derer die Datei also unter dem Dateipfad "./Study_Site_Exmouth_Gulf/setup_pymanga.xml". In Zeile 140 f. im xml-Inputfile (setup_pymanga.xml) muss der Dateispeicherort der "EXM_Jan-Jul_2019.txt"-Datei an das jeweilige Dateisystem angepasste werden.

Das Programm lässt sich jetzt durch das Öffnen eines Terminals in der Hauptebene von pyMANGA durch Eingabe des Befehls "python main.py -i /Model_Exmouth_Gulf/setup_pymanga.xml" starten. Falls der Standardname des Ordners des Setups ("Model_Exmouth_Gulf") geändert wird, muss der Verweis auf den Dateispeicherort der Steuerdatei entsprechend angepasst werden.
