---
title: "Setup selbst berechnen"
linkTitle: "Setup selbst berechnen"
weight: 4
description:
---
# Setup selbst berechnen

Das Modellsetup des &bdquo;<b>Full Models</b>&ldquo; befindet sich in der aktuellen Version von pyMANGA in folgendem Ordner: 

	./Benchmarks/Exmouth_Gulf/full_model

Um einen Modelllauf mit dem Setup auf dem eigenen Rechner zu starten müssen im wesentlichen Dateipfade, die auf Input-Dateien zeigen, im XML-Steuerfile angepasst werden.
Alle Dateipfade im Steuerfile werden absolut angegeben, jeder Pfad beginnt also unter Ubuntu mit &bdquo;/home/...&ldquo; und unter Windows mit dem Buchstaben des Laufwerks.
Wird der Dateispeicherort des Setups nicht verändert, so befindet sich die Steuerdatei an folgendem Ort:

	./Benchmarks/Exmouth_Gulf/full_model/setup_pymanga.xml

Im Steuerfile (&bdquo;setup_pymanga.xml&ldquo;) muss der Dateipfad für den Ordner mit den OGS-Input-Dateien (Zeile 18), die Datei mit der Parametrisierung des Baumwachstumsmodells (Zeile 36) und der Ordner für die Ausgabe der Modellergebnisse (Zeile 62) angegeben werden.
Als Ausgabeort können Sie auch einen individuellen Dateispeicherort wählen; wichtig ist nur, dass dieser Ordner auch existiert und leer ist - pyMANGA erstellt nicht vorhandene Ausgabeorte nicht automatisch und löscht vorhandene Dateien nicht.

Ein Beispiel für die Dateipfade in oben erwähnter Reihenfolge könnte also wie folgt aussehen:

	/home/Dokumente/pyMANGA-master/Benchmarks/Exmouth_Gulf/full_model/TreeOutput

	/home/Dokumente/pyMANGA-master/Benchmarks/Exmouth_Gulf/full_model/Avicennia.py

	/home/Dokumente/pyMANGA-master/Benchmarks/Exmouth_Gulf/full_model


Die Grundwassermodellierung mit OGS wird mit Hilfe eines zusätzlichen Python-Scripts ausgeführt.
Dieses Script stellt für OGS unter anderem Werte zum Tidenhub aus der Datei &bdquo;EXM_Jan-Jul_2019.txt&ldquo; bereit, setzt diese Daten in eine Schleife (da der Modellierungszeitraum deutlich länger als der Zeitraum der Tide-Daten ist) und sorgt für eine Anpassung des mittleren Wasserspiegels.
In der Datei (&bdquo;python_script.py&ldquo;) findet sich ein Verweis auf den Dateispeicherort dieser Datei, in Zeile 140 f. muss der Dateispeicherort der &bdquo;EXM_Jan-Jul_2019.txt&ldquo;-Datei an die lokale Ordnerstruktur angepasste werden.

Das Setup lässt sich jetzt durch das Öffnen eines Terminals in der Hauptebene von pyMANGA durch Eingabe des Befehls 

	python3 main.py -i /Benchmarks/Exmouth_Gulf/full_model/setup_pymanga.xml

starten. Die allgemeine Form würde wie folgt aussehen:

	python3 absolute/path/to/main.py -i absolute/path/to/full_model/setup_pymanga.xml

Bei Fragen oder Problemen kontaktieren Sie uns gerne.
