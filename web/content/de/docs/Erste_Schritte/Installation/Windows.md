---
title: "Microsoft Windows 10"
linkTitle: "Microsoft Windows"
weight: 3
description: >

---
Installation
------------

### Installation mit GIT

Diese Homepage befindet sich derzeit noch im Aufbau. Hier fehlt leider noch etwas. Wir arbeiten daran, Ihnen möglichst bald den gesamten Inhalt präsentieren zu können. Bis dahin müssen Sie sich leider noch etwas gedulden.

### Manuelle Installation

Um das Programm manuell zu installieren, muss der Quellcode von dieser
[Homepage](https://github.com/jbathmann/pyMANGA/) heruntergeladen
werden. Die ZIP-Datei wird an einer beliebigen Stelle entpackt. Um
Modelle mit Simulation des Grundwassergeschehens rechnen zu können, muss
die numerische Grundwassersimulationssoftware Open Geo System
installiert werden. Auf dieser
[Homepage](https://jenkins.opengeosys.org/job/ufz/job/ogs/job/master/lastSuccessfulBuild/artifact/build/)
kann die aktuelle Version des OGS heruntergeladen werden. Um
Grundwassermodell und Baumwachstumsmodell koppeln zu können, bedarf es
der Version mit pythonim Dateinamen. Die Dateien müssen in den Ordner
.\\TreeModelLib\\BelowgroundCompetition\\OGS so entpackt werden, dass in
diesem Ordner (OGS) der bin-Ordner des Downloadordners liegt. Eine
genauere Beschreibung des Installationsvorgang findet sich in der
Beschreibung des dritten Beispiel-Setups OGS3D\_SAZOI\_BETTINA.xml.

Erste Schritte
--------------

Um ein Beispiel-Modellsetup zu rechnen, muss zunächst das Windows
Terminal geöffnet werden. Eine Möglichkeit hierfür ist das Öffnen des
Ausführen-Dialogs mit der Tastenkombination WINDOWS + R. In das sich
öffnende Fenster kann die Windows-Konsole mit der Eintragung von
\<\<cmd.exe\>\> gestartet werden. Im Windows Terminal muss nun zunächst
mit \<\<cd Dateipfad\\zum\\Programm\>\> zum Dateispeicherort des
Programmes navigiert werden. Das Programm pyMANGA wird nun über die
Eingabe folgendes Befehls gestartet: \<\<python main.py\>\>. Je nachdem
wieviele Python-Pakete in der jeweiligen Python-Distribution bereits
installiert sind, müssen zunächst mehr oder weniger viele Pakete
nachinstalliert werden. Das Fehlen eines Paketes wird mit
\<\<ModuleNotFoundError: No module named 'NameDesFehlendenModuls'\>\> in
der letzten Zeile der Ausgabe angezeigt. Fehlende Pakete können über das
Windows-Terminal mit \<\<pip install NameDesFehlendenPaketes\>\>
installiert werden. Nachdem das erste fehlende Paket installiert wurde,
wird durch die erneute Eingabe von \<\<python main.py\>\> überprüft, ob
weitere Pakete fehlen. Sollte dies der Fall sein, werden auch diese
Pakete nachinstalliert. Dieses Schema wird solange wiederholt, bis das
Terminal auf die Eingabe \<\<python main.py\>\> folgende Ausgabe
liefert: \<\<UnboundLocalError: Wrong usage of pyMANGA. Type \"python
main.py -h\" for additional help.\>\>

pyMANGA ist jetzt ausführbar. Um die Berechnung eines Modell-Setups zu
starten, muss die Steuerdatei des Setups angegeben werden werden. Hierzu
muss folgendes in das Windows-Terminal eingegeben werden:

``` {.numberLines numbers="left" breaklines="true"}
main.py --project_file "Pfad\zu\Steuerdatei"
```

Im Allgemeinen ist bei der Angabe eines Dateipfades in der
Windows-Konsole stets auf die Verwendung des Backshlashes zu achten. Bis
auf dieses Detail unterscheiden sich die Installation und die Bedienung
der Software kaum zwischen den beiden Betriebssystemen Microsoft Windows
und Ubuntu.

### Beispielsetup AllSimple\_WithOutput.xml

In der Steuerdatei zum ersten Beispiel-Setup ist die Anzeige einer
Visualisierung vom Typ SimplePyplotvoreingestellt. Eine Ausgabe der
Ergebnisse soll in der Form OneTreeOneFile erfolgen. Der Pfad der
Ausgabe der Ergebnisdateien wird in Zeile 57 des Steuerfiles vorgegeben
(siehe Anhang). Diese Zeile im Quellcode ist die einzige Stelle, an der
in der Steuerdatei noch etwas geändert werden muss. Der Dateipfad für
das Abspeichern der Ergebnisse muss zunächst erstellt werden und
anschließend der Pfad in die Steuerdatei geschrieben werden.
Standardmäßig wird hierfür der auch im Anhang in die Steuerdatei
eingetragene Dateipfad \<\<./ProjectLib/ExampleSetups/testoutputs\>\>
genutzt.

Um einen Modelllauf mit dem Beispielsetup AllSimple\\WithOutput zu
starten, muss, nachdem im Windows-Terminal zum Dateispeicherort
navigiert wurde, folgendes eingegeben werden:

``` {.numberLines numbers="left" breaklines="true"}
python main.py --project_file\text".\ProjectLib\ExampleSetups\AllSimple_WithOutput.xml"
```

Eine fehlerfreie Berechnung des Beispiel-Setups ist am Erscheinen der
grafischen Ausgabe und der Visualisierung der Ergebnisse bis zum Ende
der Berechnung ($31,69\ a$) und an den in den zuvor definierten
Ausgabeort geschriebenen Ergebnisdateien zu erkennen. Dieser Ordner
sollte auch vor jedem Modelllauf geleert werden, andernfalls kommt es zu
Problem (Fehlermeldung: \<\<ValueError: Output directory
'./ProjectLib/ExampleSetups/testoutputs/' is not empty.\>\>).

### Beispielsetup FON\_SAZOI\_KIWI.xml

Dieses Beispiel-Setup ist so voreingestellt, dass eine Visualisierung
während der Berechnung des Modells gezeigt wird, aber keine
Ergebnisdateien geschrieben werden. Die Modelllaufzeit beträgt $150\ a$
(bzw. $4733640000\ s$, Quellcode Zeile 67 f.). Dementsprechend entfällt
hier auch die Notwendigkeit einen Dateispeicherort für die
Modellergebnisdateien in der Steuerdatei anzugeben.

Das Beispiel kann analog zu dem Setup AllSimple$\_$WithOutputgestartet
werden. In das Windows-Terminal wird also - nachdem an den Speicherort
des Programms navigiert wurde - folgender Befehl ausgeführt:

``` {.numberLines numbers="left" breaklines="true"}
python main.py --project_file\text".\ProjectLib\ExampleSetups\FON_SAZOI_KIWI.xml"
```

Die korrekte Modellberechnung ist wieder an der grafischen Ausgabe,
welche die Modellergebnisse bis zu einer Modelllaufzeit von 150 a
visualisiert, zu erkennen.

### Beispielsetup OGS3D\_SAZOI\_BETTINA.xml

In diesem Beispiel ist weder eine Visualisierung noch ein Speichern der
Modellergebnisse vorgesehen. Im Gegensatz zu den ersten beiden
Beispielen wird die Grundwasserströmung mit berücksichtigt. Um die
Modellergebnisse zu berechnen, wird die numerische
Grundwassermodellierungssoftware OGS benötigt. Das Software-Paket kann
von dieser
[Homepage](https://jenkins.opengeosys.org/job/ufz/job/ogs/job/master/lastSuccessfulBuild/artifact/build/)
heruntergeladen werden. Die ZIP-Datei wird so entpackt, dass der
bin-Ordner direkt im Dateipfad ./TreeModelLib/BelowgroundCompetition/OGS
der pyMANGA Installation liegt. Ob OGS nun bereits ausführbar ist, kann
mit dem Befehl

``` {.numberLines numbers="left" breaklines="true"}
Pfad\zum\Speicherort\von\pyMANGA\TreeModelLib\BelowgroundCompetition\OGS\bin\ogs
```

überprüft werden. Das dritte Beispiel-Setup wird nun analog zu den
ersten beiden Setups gestartet. Ob die Berechnung korrekt durchgeführt
wird, erkennt man an der Ausgabe des Terminals.

