---
title: "Modelsetup Exmouth Golf"
linkTitle: "Modell-Setup"
weight: 3
description:
---

# Beschreibung des Modellsetups

Das Modell-Setup des "Full Models" kann hier !!!!!link setzen!!!! gedownloaded werden. Im folgenden werden die wichtigsten Dateien des Setups genauer beschrieben. Möchten Sie das Setup installieren und einen Modelllauf starten, sehen Sie sich hierzu gerne die <a href="/de/docs/erste_schritte/">allgemeinen Hinweise zur Installation und den ersten Schritten von pyMANGA</a> und die <a href="/de/docs/erste_schritte/">Hinweise zur Installation des "Full Models"</a> an.

In der Hauptebene des Setups liegen ein Ordner "Input_OGS" und die zwei Dateien Avicennia.py und setup_pymanga.xml. Wie der Name vermuten lässt, befinden sich im Ordner "Input_OGS" die für die Grundwassermodellierung nötigen Modelleingangsdateien. "Avicennia.py" enthält Einstellungen zur Mangrovenart "Graue Mangrove". Hier können zum Beispiel die Wachstumsgeschwindigkeit, maximale Wachstumshöhe, maximale Lebenszeit und andere individuenspezifische Parameter definiert werden. Die Steuerdatei "Dateiname.xml" stellt das Herzstück eines jeden Modellsetups dar. Sie wird aufgerufen, um einen Modelllauf zu starten. Das Dokument README.md dient lediglich Informationszwecken und spielt bei der Modellierung mit pyMANGA keine Rolle.

# Steuerdatei: setup_pymanga.xml

Eine Beschreibung der Steuerdatei dieses Setups finden Sie  <a href="/de/docs/steuerdatei/">hier</a>.


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

Mithilfe dieser Datei können Randbedingungen und Quellterme für das OGS-Modell definiert werden. Diese Angabe ist optional; die Notwendigkeit hängt von der Komplexität des Grundwassermodells ab. In diesem Modell sorgt die Datei für eine Schleife der aus der Datei EXM_Jan-Jul_2019.txt eingelesenen Informationen zum Tidehub und für eine dynamische Anpassung des mittleren Wasserstands.

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
