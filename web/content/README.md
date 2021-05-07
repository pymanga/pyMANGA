English version below

# Hinweise zum Hauptmenüpunkt Dokumentation

Innerhalb des Abschnitts Dokumentation sind aufgrund der Design-Vorlage einige Besonderheiten zu beachten.

## Markdown

Die Verwendung von Markdown-Syntax hat in einigen Fällen für Probleme gesorgt.
Insbesondere Gliederungs- und Verlinkungsbefehle wurden nicht richtig umgesetzt.
Da innerhalb eines Markdown-Dokuments jederzeit HTML-Syntax verwendet werden kann, wurde ein großteil des Inhalts der Homepage komplett in HTLM geschrieben.
Sollte es zu Problemen kommen, wird empfohlen den Inhalt zunächst in HTML zu übersetzen.

Da innerhalb eines Markdown-Dokuments HTML-Passagen automatisch erkannt werden, kann ein Dokument, das komplett in HTML geschrieben ist, auch als ".md" gespeichet werden.
Wird eine Datei hingegeben als ".html" gespeichert so muss darauf geachtet werden, dass ausschließlich HTML-Syntax darin verwendung findet.

## Grafiken

Um Grafiken in die Homepage einzubinden müssen diese im Ordner 

		/web/themes/docsy/static/pictures

liegen.
Innerhalb des Links wird der Dateipfad dann relativ vom Ordner "static" aus angegeben (siehe auch im bereits vorhandenem Inhalt "Dokumentation"). 

## Java-Script

Das Gleiche gilt für die Einbindung von Java-Scripts.
Diese müssen als eigene Datei abgespeichert werden und können nicht direkt im Dokument integriert werden. 
Innerhalb des Dokuments muss dann auf die externe Datei verlinkt werden (siehe z.B. "Das Modell" im Kapitel "Beispielmodell: Exmouth-Golf"). 
Auch hier kann die Datei nicht an einem beliebigem Ort gespeichert werden, sondern muss im Ordner "static" liegen.
Der Dateipfad lautet dann:

		/web/themes/docsy/static/js

Auch hier wird der Verweis auf die Datei wieder relativ vom Ordner "static" aus angegeben.

# Notes on the main menu item Documentation

Within the documentation section, due to the design template, there are some peculiarities that have to be considered.

## Markdown

The use of Markdown syntax has caused problems in some cases. 
In particular, outline and linking commands were not properly implemented correctly.
Since within a Markdown document HTML syntax can be used at any time, a large part of the content of the homepage was written completely in HTLM.
In case of problems it is recommended to translate the content into HTML first.

Since within a Markdown document HTML passages are automatically recognized, a document written completely in HTML can also be saved as ".md".
However, if a file is stored as ".html", you have to make sure that only HTML syntax is used in it.

## Graphics

To include graphics in the homepage they have to be stored in the folder

		/web/themes/docsy/static/pictures

Within the link the file path is then relative from the folder
"static" (see also in the already existing content "Documentation").

## Java Script

The same applies to the integration of Java-Scripts.
These must be saved as file and cannot be integrated directly into the document.
Within the document you have to link to the external file (see e.g. "The model" in the chapter "Sample Setup: Exmouth-Golf").
Again, the file cannot be stored in any location, but must be stored in the folder "static".
The file path is then:

		/web/themes/docsy/static/js

Again, the reference to the file is relative to the folder
"static" folder.
