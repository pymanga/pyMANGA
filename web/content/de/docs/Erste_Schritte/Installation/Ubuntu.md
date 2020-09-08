---
title: "Ubuntu 18.04"
linkTitle: "Ubuntu"
weight: 3
description: >
---
Installation
------------

### Installation mit GIT

Um mit der eigentlichen Installation des Programms beginnen zu können,
muss Git zunächst installiert werden. Indem man den Befehl \<\<sudo
apt-get update\>\> folgend mit \<sudo apt-get install git\> in das
Terminal (aufrufbar mit STRG + ALT + T) eingibt, startet man die
Installation. Mit der Abfrage \<\<git --version\>\> kann die
Installation überprüft werden (Ausgabe gibt Version der Git-Installation
an - wenn die Installation erfolgreich war). Mit der Eingabe \<\<cd
Pfad/zu/dem/gewünschten/Speicherort/des/Programms\>\> wird mit dem
Terminal zu dem Pfad navigiert, an dem das Programm gespeichert werden
soll. Der Befehl \<\<git clone
https://github.com/jbathmann/pyMANGA.git\>\> lädt das Programm auf den
heimischen Rechner und speichert es an dem zuvor angegebenen
Dateispeicherort.

### Manuelle Installation

Diese Homepage befindet sich derzeit noch im Aufbau. Hier fehlt leider noch etwas. Wir arbeiten daran, Ihnen möglichst bald den gesamten Inhalt präsentieren zu können. Bis dahin müssen Sie sich leider noch etwas gedulden.

Erste Schritte
--------------

Um das Programm zu starten, muss zunächst zu dem Dateispeicherort
navigiert werden (\<\<cd Pfad/zum/Speicherort/des/Programms\>\>). Hier
kann das Programm mit der Eingabe von \<python main.py\> gestartet
werden. Sollten noch nicht alle benötigten Python-Pakete installiert
sein, wird dies über die Ausgabe angezeigt (\<\<ModuleNotFoundError: No
module named 'NameDesFehlendenModuls'\>\>). Fehlende Pakete lassen sich
mit dem Befehl \<\<pip install NameDesFehlendenModuls\>\> installieren.
Nach der Installation eines Pakets wird die Eingabe \<python main.py\>
wiederholt, bis keine fehlenden Pakete mehr angezeigt werden und der
letzte Teil der Ausgabe \<\<UnboundLocalError: Wrong usage of pyMANGA.
Type \"python main.py -h\" for additional help.\>\> lautet.

pyMANGA ist jetzt ausführbar. Um die Berechnung eines Modell-Setups zu
starten, muss die Steuerdatei des Setups angegeben werden werden. Hierzu
muss folgendes in das Terminal eingegeben werden:

``` {.numberLines numbers="left" breaklines="true"}
python main.py --project_file ./Pfad/zu/Steuerdatei
```

### Beispielsetup AllSimple\_WithOutput.xml

In der Steuerdatei zum ersten Beispiel-Setup ist die Anzeige einer
Visualisierung vom Typ SimplePyplotvoreingestellt. Eine Ausgabe der
Ergebnisse soll in der Form OneTreeOneFile erfolgen. Der Pfad der
Ausgabe der Ergebnisdateien wird in Zeile 57 des Quellcodes (siehe
Anhang) vorgegeben.

Um einen Modelllauf mit dem Beispielsetup zu starten, muss, nachdem im
Terminal zum Dateispeicherort navigiert wurde, folgendes eingegeben
werden:

``` {.numberLines numbers="left" breaklines="true"}
python main.py --project_file ./ProjectLib/ExampleSetups/AllSimple_WithOutput.xml
```

Eine fehlerfreie Berechnung des Beispiel-Setups ist am Erscheinen der
grafischen Ausgabe und deren Visualisierung der Ergebnisse bis zum Ende
der Berechnung ($1 * 10^9\ s$ bzw. $31,69\ a$) sowie an den im
Steuerfile definierten Dateiort für die Ergebnisdateien (Standardmäßig:
./ProjectLib/ExampleSetups/testoutputs) zu erkennen. Dieser Ordner
sollte auch vor jedem Modelllauf geleert werden, andernfalls kommt es zu
Problem (Fehlermeldung: \<\<ValueError: Output directory
'./ProjectLib/ExampleSetups/testoutputs/' is not empty.\>\>).

### Beispielsetup FON\_SAZOI\_KIWI.xml

Dieses Beispiel-Setup ist so voreingestellt, dass eine Visualisierung
während der Berechnung des Modells gezeigt wird, aber keine
Ergebnisdateien geschrieben werden. Die Modelllaufzeit beträgt $150\ a$
(bzw. $4733640000\ s$, Quellcode Zeile 67 f.).

Gestartet wird der Modelllauf analog zum ersten Beispiel-Setup. Befehl
muss also lauten:

``` {.numberLines numbers="left" breaklines="true"}
python main.py --project_file ./ProjectLib/ExampleSetups/FON/SAZOI/KIWI.xml
```

Eine fehlerfreie Berechnung erkennt man an der Visualisierung der
Modellergebnisse bis zum Endzeitpunkt des Modelllaufs.

### Beispielsetup OGS3D\_SAZOI\_BETTINA.xml

In diesem Beispiel ist weder eine Visualisierung noch ein Speichern der
Modellergebnisse vorgesehen. Im Gegensatz zu den ersten beiden
Beispielen wird die Grundwasserströmung mit berücksichtigt. Um die
Modellergebnisse berechnen zu können, wird die numerische
Grundwassermodellierungssoftware OGS benötigt. Die Software kann hier
heruntergeladen werden und so installiert werden, dass der bin-Ordner
direkt im Dateipfad ./TreeModelLib/BelowgroundCompetition/OGS der
pyMANGA Installation liegt. Ob OGS nun bereits ausführbar ist, kann mit
dem Befehl

``` {.numberLines numbers="left" breaklines="true"}
Pfad\zum\Speicherort\von\pyMANGA\TreeModelLib\BelowgroundCompetition\OGS\bin\ogs
```

überprüft werden. Eventuell müssen noch fehlende Python-Pakete auch hier
zunächst installiert werden. Das dritte Beispiel-Setup wird nun analog
zu den ersten beiden Setups gestartet. Wird die Grundwasserströmung mit
OGS nicht korrekt berechnet, stellt die Installation von Python der
Version 3.6.X und pip3 einen Lösungsversuch dar. Das Modell wird nun mit
folgendem Befehl gestartet:

``` {.numberLines numbers="left" breaklines="true"}
python3.6 main.py --project_file ./ProjectLib/ExampleSetups/FON/SAZOI/KIWI.xml
```

Noch fehlende Pakete für die Python-Version 3.6 müssen mit dem Befehl
\<\<pip3 install fehlendesPythonpaket\>\> zunächst installiert werden.

Startet die Berechnung des Modells korrekt, liefert das Terminal
folgende Ausgabe:

