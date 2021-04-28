---
title: "Das Modell"
linkTitle: "Das Modell"
weight: 3
description:
---

<head>
<style type="text/css">
<!--
#vis {
  border: 1px solid black;
}
#Rahmen {
        border-width: 0.1em; 
        border-style: solid;
        text-align:right;
}
-->
</style>
</head>

Wie bereits im <a href="/de/docs/beispielmodell_exmouth_gulf/der_exmouth_golf/">einführenden Kapitel</a> beschrieben gibt es im Exmouth-Golf zahlreiche Mangrovenwälder. Mithilfe von MANGA wird die Wachstumsdynamik der Mangroven in einem Modell abgebildet. Hauptaugenmerk liegt dabei auf der für Mangrovenwälder typischen Struktur und die Dominanz einzelner Mangrovenarten unter verschiedenen Standortbedingungen. Neben dem Wachstumsverhalten der Mangroven wird die Salinität des Bodenwassers - auch als eine sensitive Einflussgröße auf das Wachstum - genauer betrachtet. Dabei werden die wechselwirkenden Einflüsse des Mangrovenwachstums und der Gradienten der Salinität im Bodenwasser berücksichtigt. In diesem Kapitel wird der Aufbau des Modells, die Grundlagen der Modellierung mit MANGA und die Ergebnisse der Arbeit beschrieben.

# Modellgebiet

Im Modell wird ein Transekt von 185 m Länge und 10 m Breite abgebildet (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_1">Abbildung 1</a>).
Zur Evaluierung der Modellergebnisse werden sowohl Allometriedaten aus einer Transektenmessung, als auch Messergebnisse einer Langzeitstudie verwendet. In der Langzeitstudie werden die Auswirkungen von Düngung auf das Wachstum von insgesamt 72 Mangroven, von denen jeweils die Hälfte an der land- und an der seeseitigen Seite des Transekts steht, dokumentiert (siehe auch die in <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4</a> eingezeichneten &bdquo;Treatment Averages&ldquo;).

<figure>
<a name="Abbildung_1"></a>
<img src="/pictures/exmouth_gulf/Transect_Sketch.png">
<figcaption><font size = "1"><i><b>Abbildung 1:</b> Vereinfachte Darstellung der Standortbedingungen und des konzeptionellen Modells</i></font></figcaption>
</figure><br>

Das Modell bildet das Mangrovenwachstum an der in nachfolgender Darstellung zu sehenden Stelle im Exmouth-Golf dar.

<iframe src="https://www.google.com/maps/d/embed?mid=1EiX5yyZGJgVSu7pueUi5_jK160ndg0tG" width="640" height="480"></iframe>

<br>
<br>

Die Höhenprofile aus dem digitalen Oberflächenmodell der fünf Transekte (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_2">Abbildung 2 A</a>) wurden übereinander gelegt und aus den fünf Signalen (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_2">Abbildung 2 B</a>) die Geländeoberkante aus der Grundlinie der Signale interpoliert (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_2">Abbildung 2 C</a>). Das so entstehende DGM wurde für die Diskretisierung des Grundwassermodells genutzt.

<figure>
<a name="Abbildung_2"></a>
<img src="/pictures/exmouth_gulf/dem.png" style="width:75%">
<figcaption><font size = "1"><i><b>Abbildung 2:</b> Geländehöhen entland der Transekte</i></font></figcaption>
</figure><br>

# Modellierung

## Modellvarianten

Das Mangrovenwachstum wurde mit Hilfe von drei verschiedenen Modellen simuliert (siehe auch <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_1">Tabelle 1</a>). 

Im Modell &bdquo;<b>Model Without Feedback</b>&ldquo; werden die dynamischen Veränderungen der abiotischen Einflüsse (Gezeiten, Grundwasserneubildung und Salzgehalt des Meerwassers) über entsprechende Randbedingungen berücksichtigt. Der Einfluss der Pflanzenwasserentnahme auf den Salzgehalt des Porenwassers wurde nicht abgebildet.

Das Modell &bdquo;<b>Model Without Tide</b>&ldquo; berücksichtigt die Auswirkungen der Pflanzenwasserentnahme auf den Salzgehalt des Porenwassers und alle abiotischen Einflüsse des ersten Modells&nbsp;&ndash; mit Außnahme der Gezeiten.

Die dritte Modellvariante &bdquo;<b>Full Model</b>&ldquo; bildet schließlich sowohl die Dynamik der Gezeiten als auch die Kopplung der Pflanzenwasserentnahme und des Porenwassers ab.

Nachfolgende <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_1">Tabelle 1</a> fasst die Spezifikationen der drei Modellvarianten zusammen.

<figure>
<figcaption align="top"><font size = "1"><i><b>Tabelle 1:</b> Modellvarianten</i></font></figcaption>
<a name="Tabelle_1"></a>
<table width="100%">
 <tr>
  <td  width="27%" style="text-align: center; vertical-align: middle">
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Gezeiten
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Kopplung Pflanzenwasserhaushalt und Porenwasser
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Sonstige abiotische Faktoren
  </td>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Model Without Feedback
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="red" size="5"> <b> &#10008; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Model Without Tide
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="red" size="5"> <b> &#10008; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Full Model
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
 </tr>
</table>
</figure>
<br>

## Diskretisierung 

### Grundwassermodell

Das Grundwassermodell bildet den Untergrund mit einem Gitter der Ausmaße 10&nbsp;m&nbsp;x&nbsp;230&nbsp;m&nbsp;x&nbsp;3&nbsp;m auf fünf FEM-Layern mit insgesamt 5880 Zellen ab. Nachfolgende <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_2">Abbildung 2</a> zeigt die räumliche Diskretisierung aus seeseitiger Perspektive.

<figure>
<a name="Abbildung_2"></a>
<img src="/pictures/exmouth_gulf/dis.png">
<figcaption><font size = "1"><i><b>Abbildung 2:</b> Räumliche Diskretisierung des Grundwassermodells</i></font></figcaption>
</figure><p>

Die Mangroven entnehmen dem Untergrund Bodenwasser aus einer Tiefe von 40&nbsp;cm bis 80&nbsp;cm unter der Geländeoberkante. <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_3">Abbildung 3</a> zeigt das Modellgebiet (Grau) und den Bereich der Wasserentnahme durch die Mangroven (Blau). Zu beachten ist die 50-fache vertikale Skalierung. 

<figure>
<a name="Abbildung_3"></a>
<img src="/pictures/exmouth_gulf/model_area_legend.png">
<figcaption><font size = "1"><i><b>Abbildung 3:</b> Bereich der Porenwasserentnahme durch Mangroven</i></font></figcaption>
</figure><p>

Zeitlich diskretisiert wird das Grundwassermodell mit einer Zeitschrittlänge von einer Stunde. Der Tidenhub als dynamische Randbedingung wird mit der Zeitreihe der Jahre 1991 bis 1993, die über die gesamte Modelllaufzeit immer wieder wiederholt wird, abgebildet.

### Baumwachstumsmodell

Da jede Mangrove als einzelnes Individuum abgebildet wird findet eine räumliche Diskretisierung im eigentlichen Sinne nicht statt. Zeitlich wird das Baumwachstumsmodell mit einer Zeitschrittlänge von einem halben Jahr (1&nbsp;a&nbsp;=&nbsp;365.25&nbsp;d) diskretisiert.

## Randbedingungen Grundwassermodell

Der Salzgehalt des Meerwassers wurde mit 50 g/kg festgelegt, das Bodenwasser am landseitigen Ende des Transsekts bekam eine Salinität von 70 g/kg zugewiesen. Durch die Transpiration der Mangroven erhöhen diese lokal den Salzgehalt im Porenwasser. Der Wasserstand wird in Form des hydrostatischen Drucks an der see- und landseitigen Kante des Modellgebiebts bestimmt. Zur Abbildung der Gezeiten wurde der seeseitige Wasserstand dabei als dynamische Randbedingung 1. Art in das Modell integriert. Als Datengrundlage dienen hier die Wasserstandsmessungen des Department of Transport der Government of Western Australia. Der landseitige Wasserstand wird über eine konstante Randbedingung 1. Art abgebildet. Die Evapotranspiration der Bäume wird durch Senken im Bereich der Wurzeln abgebildet (vgl. <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_3">Abbildung 3</a>). Zufluss in Form von Niederschlag wird indirekt über den Salzgehalt am landseitigen Rand des Modellgebiets berücksichtigt. Die hier nicht erwähnten Modellränder werden alle als No-Flow-Randbedingungen definiert. Eine schematische Übersicht des Modellgebiets stellt auch <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_1">Abbildung 1</a> dar.



<a name="Parametrisierung"></a>
## Parametrisierung

In den nachfolgenden Tabellen finden sich die Parametrisierungen des Untergrunds (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_2">Tabelle 2</a>) und der Mangroven (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_3">Tabelle 3</a>), globale Gewichtungsfaktoren (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_4">Tabelle 4</a>) sowie die Anfangswerte der Geoemtrieen der Mangrovensetzlinge (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_5">Tabelle 5</a>).

### Untergrund

<table>
<tablecaption align="top"><font size = "1"><i><b>Tabelle 2:</b> Parametrisierung des Untergrunds</i></font></tablecaption>
<a name="Tabelle_2"></a>
<thead>
<tr class="header">
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Parametername</th>
<th style="text-align: left;">Wert</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>D</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">molekularer Diffusionskoeffizient</td>
<td style="text-align: left;">1&nbsp;×&nbsp;10<sup>-9</sup> m<sup>2</sup>/s</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>β</em><sub><em>T</em></sub></span></td>
<td style="text-align: left;">transversale Dispersivität</td>
<td style="text-align: left;">0,5 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>β</em><sub><em>L</em></sub></span></td>
<td style="text-align: left;">longitudinale Dispersivität</td>
<td style="text-align: left;">1 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>ρ</em></span></td>
<td style="text-align: left;">Dichte von Wasser</td>
<td style="text-align: left;">1&nbsp;×&nbsp;10<sup>3</sup> kg/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>μ</em></span></td>
<td style="text-align: left;">dynamische Viskosität</td>
<td style="text-align: left;">1&nbsp;×&nbsp;10<sup>-3</sup> Pas</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>κ</em></span></td>
<td style="text-align: left;">intrinsische Permeabilität</td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-11</sup> m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>Φ</em></span></td>
<td style="text-align: left;">Porosität des Untergrunds</td>
<td style="text-align: left;"><span class="math inline">0,5</span></td>
</tr>
</tbody>
</table>

### Botanik

#### Wasserhaushalt der Mangroven

<table>
<tablecaption align="top"><font size = "1"><i><b>Tabelle 3:</b> Parametrisierung der biotischen Faktoren</i></font></tablecaption>
<a name="Tabelle_3"></a>
<thead>
<tr class="header">
<th width="10%" style="text-align: left;">Symbol</th>
<th width="40%" style="text-align: left;">Parametername</th>
<th width="25%" style="text-align: left;">Avicennia marina</th>
<th width="25%" style="text-align: left;">Rhizophora mangle </th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>D</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Wasserpotential der Mangroven</td>
<td style="text-align: left;">-8,15&nbsp;×&nbsp;10<sup>6</sup> kg/s<sup>2</sup>/m</td>
<td style="text-align: left;">-6,45&nbsp;×&nbsp;10<sup>6</sup> kg/s<sup>2</sup>/m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>f</em></sub></span></td>
<td style="text-align: left;">Xylem-Leitfähigkeit</td>
<td style="text-align: left;">1,04&nbsp;×&nbsp;10<sup>-10</sup> kg/s/m<sup>2</sup></td>
<td style="text-align: left;">3,12&nbsp;×&nbsp;10<sup>-10</sup> kg/s/m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>L</em><sub><em>p</em></sub> ⋅ <em>k</em><sub><em>g</em><em>e</em><em>o</em></sub></span></td>
<td style="text-align: left;">Feine Wurzelpermeabilität  ⋅  Skalierungsfaktor</td>
<td style="text-align: left;">1,32&nbsp;×&nbsp;10<sup>-11</sup> kg/s/m<sup>4</sup></td>
<td style="text-align: left;">1,32&nbsp;×&nbsp;10<sup>-11</sup> kg/s/m<sup>4</sup></td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Resourcenbedarf zur Biomasseerhaltung</td>
<td style="text-align: left;">1,4&nbsp;×&nbsp;10<sup>-6</sup> kg/s/m<sup>3</sup></td>
<td style="text-align: left;">1,4&nbsp;×&nbsp;10<sup>-6</sup> kg/s/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>g</em><em>r</em><em>o</em><em>w</em><em>t</em><em>h</em></sub></span></td>
<td style="text-align: left;">Skalierungsfaktor der Wachstumsgeschwindigkeit</td>
<td style="text-align: left;">3,5&nbsp;×&nbsp;10<sup>-3</sup></td>
<td style="text-align: left;">3,5&nbsp;×&nbsp;10<sup>-3</sup></td>
</tr>
</tbody>
</table>

#### Globale Gewichtungsfaktoren

<table>
<tablecaption align="top"><font size = "1"><i><b>Tabelle 4:</b> Globale Gewichtungsfaktoren</i></font></tablecaption>
<a name="Tabelle_4"></a>
<thead>
<tr class="header">
<th width="10%" style="text-align: left;">Symbol</th>
<th width="40%" style="text-align: left;">Gewichtungsfaktor</th>
<th width="25%" style="text-align: left;">Avicennia marina</th>
<th width="25%" style="text-align: left;">Rhizophora mangle </th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>C</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Sonnenstrahlung</td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-8</sup> kg/s/m<sup>2</sup></td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-8</sup> kg/s/m<sup>2</sup></td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>σ</em></span></td>
<td style="text-align: left;">erste Steigung der Sigmoidfunktion</td>
<td style="text-align: left;">1,5&nbsp;×&nbsp;10<sup>-2</sup> </td>
<td style="text-align: left;">1,5&nbsp;×&nbsp;10<sup>-2</sup> </td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>σ</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">zweite Steigung der Sigmoidfunktion</td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-2</td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-2</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>ω</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">Skalierungsfaktor für Baumhöhenwachstum</td>
<td style="text-align: left;">0,12</td>
<td style="text-align: left;">0,12</td>
</tr>
</tr>
</tbody>
</table>

#### Anfangswerte der geometrischen Kennwerte für Mangrovensetzlinge

<table>
<tablecaption align="top"><font size = "1"><i><b>Tabelle 5:</b> Anfangswerte der geometischen Kennwerte der Mangrovensetzlinge</i></font></tablecaption>
<a name="Tabelle_5"></a>
<thead>
<tr class="header">
<th width="10%" style="text-align: left;">Symbol</th>
<th width="40%" style="text-align: left;">Geometrische Abmessung</th>
<th width="25%" style="text-align: left;">Avicennia marina</th>
<th width="25%" style="text-align: left;">Rhizophora mangle </th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Wurzelradius</td>
<td style="text-align: left;">0,25 m</td>
<td style="text-align: left;">0,25 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>C</em></sub></span></td>
<td style="text-align: left;">Kronenradius</td>
<td style="text-align: left;">0,3 m</td>
<td style="text-align: left;">0,3 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stammradius</td>
<td style="text-align: left;">0,01 m</td>
<td style="text-align: left;">0,01 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stammhöhe</td>
<td style="text-align: left;">0,015 m</td>
<td style="text-align: left;">0,015 m</td>
</tr>
</tbody>
</table>


<!--english version

<table>
<thead>
<tr class="header">
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Species parameter</th>
<th style="text-align: left;">Value</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>D</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Leaf water potential</td>
<td style="text-align: left;">8.15 × 10<sup>6</sup> kg/s<sup>2</sup>/m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>f</em></sub></span></td>
<td style="text-align: left;">Xylem conductivity</td>
<td style="text-align: left;">1.04e-10 kg/s/m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>L</em><sub><em>p</em></sub> ⋅ <em>k</em><sub><em>g</em><em>e</em><em>o</em></sub></span></td>
<td style="text-align: left;">Fine root permeability <span class="math inline">⋅</span> scaling factor</td>
<td style="text-align: left;">1.32e-11 kg/s/m<sup>4</sup></td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Maintenance cost per biomass</td>
<td style="text-align: left;">1.4e-6 kg/s/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>g</em><em>r</em><em>o</em><em>w</em><em>t</em><em>h</em></sub></span></td>
<td style="text-align: left;">Growth speed scaling</td>
<td style="text-align: left;">2.5e-3</td>
</tr>
<tr class="even">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;">Symbol</td>
<td style="text-align: left;">Global weighting factor</td>
<td style="text-align: left;">Value</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>C</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Solar resource inputs</td>
<td style="text-align: left;">5e-8 kg/s/m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>σ</em></span></td>
<td style="text-align: left;">First sigmoidal slope</td>
<td style="text-align: left;">1.5e-2</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>σ</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">Second sigmoidal slope</td>
<td style="text-align: left;">5e-2</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>ω</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">Heigth growth scaling factor</td>
<td style="text-align: left;">0.5</td>
</tr>
<tr class="even">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;">Symbol</td>
<td style="text-align: left;">Geometric measure</td>
<td style="text-align: left;">Value</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Root radius</td>
<td style="text-align: left;">0.26 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>C</em></sub></span></td>
<td style="text-align: left;">Crown radius</td>
<td style="text-align: left;">0.2 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stem radius</td>
<td style="text-align: left;">0.005 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Root depth</td>
<td style="text-align: left;">0.004 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>C</em></sub></span></td>
<td style="text-align: left;">Crown depth</td>
<td style="text-align: left;">0.004 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stem heigth</td>
<td style="text-align: left;">0.015 m</td>
</tr>
</tbody>
</table>

-->

# Ressourcenkonkurrenz

Um die Mangroven im Modellgebiet abzubilden, bedarf es der Herstellung einer stabilen Population, also dem Erreichen von quasi-stationären Verhältnissen. Hierzu werden zunächst 30 Mangroven zufällig im Modellgebiet als Setzlinge positioniert. In jedem Zeitschritt (Länge: halbes Jahr) kommen nun 30 neue Mangroven hinzu, die ebenfalls zufällig im Modellgebiet positioniert werden. Aufgrund des wettbewerbsbasierten Baumwachstumsmodells sterben diese neuen Mangroven mehr oder weniger schnell wieder ab. So ist die Wahrscheinlichkeit, dass eine junge Mangrove im Einzugsgebiet einer bereits älteren sehr schnell wieder stirbt sehr hoch. Ursächlich hierfür ist die überirdische Konkurenz betreffend vor allem das fehlende Sonnenlicht. Durch die Aufkonzentrierung des Salzgehalts, bedingt durch die Entnahme von Frischwasser der anderen Mangroven, entstehen im Porenwasser Salzfahnen. Diese sorgen für schlechtere Wachstumsbedingungen der sich im Abstrom befindenden (jungen) Mangroven. Unterschiedliche Mangrovenarten haben eine jeweils höhere oder niedrigere Toleranz gegenüber hohen Salzkonzentrationen. In dieser Arbeit wurden in diesem Zusammenhang die beiden Arten Avicennia marina (&bdquo;<a href="https://www.biologie-seite.de/Biologie/Avicennia_marina" target="_blank">graue Mangrove</a>&ldquo;) und Rhizophora mangle (&bdquo;<a href="https://www.biologie-seite.de/Biologie/Rote_Mangrove" target="_blank">rote Mangrove</a>&ldquo;) genauer betrachtet.


# Ergebnisse

In dieser Arbeit wurden mit Hilfe des MANGA-Modells zwei Prozesse genauer betrachtet. Zum einen sollte die Entwicklung der typischen Strukturen in Mangrovenwäldern abgebildet werden, zum anderen sollte das Wachstumsverhalten der beiden Mangrovenarten unter verschiedenen Umweltbedingungen Untersucht werden. Im nachfolgenden werden die Ergebnisse kurz zusammengefasst.

## Waldstruktur

Nachfolgende Visualisierung zeigt die dynamische Entwicklung der Mangrovenpopulation im Modellgebiet und die Entwicklung der Biomasse. Gut nachvollziehbar ist hier, bereits in den ersten 100 Zeitschritten, die immer stabiler werdende Mangrovenpopulation. Es bilden sich relativ schnell Bereiche über die X-Länge des Transsekts aus, in denen große und somit Mangroven die sehr alt werden wachsen, und solche, in denen junge Mangroven schnell wieder sterben. Dadurch, dass in jedem Zeitschritt 30 neue Mangroven als Setzlinge in das Modell hinzukommen und die Nährstoffkonkurenz anfangs sehr gering ist, wächst die Biomasse im Modell zunächst sehr stark an. Mit steigender Anzahl an Mangroven im Modellgebiet wird die Konkurenz zwischen den einzelnen Bäumen immer größer. Nach dem globalen Maximum der Biomasse fällt diese durch für einige Mangroven immer schlechter werdende Nährstoffbedingungen zunächst wieder leicht ab. Nach einer gewissen Zeit stellt sich dann ein quasi-stationärer Zustand der Mangrovenpopulation ein. 


<figure id="vis">
<a name="Visualisierung_1"></a>
<form oninput="x.value=parseInt(a.value)" id="slider" >
<script type="text/javascript">
 /*<![CDATA[*/
  document.getElementById("slider").addEventListener("input", aktualisiere);
   function aktualisiere() {
	  var TS = (document.querySelector("output[name=x]")) ;
	  var a = '/pictures/exmouth_gulf/TS/ts_'+TS.value+'.png' ;
          document.getElementById("abb").setAttribute('src', a) ;
}
/*]]>*/
</script>
<img src='/pictures/exmouth_gulf/TS/ts_0.png' id="abb">
</br>
</br>
<p align="left">
<font size = "6">&nbsp;  Zeitschritt:&nbsp;&nbsp;&nbsp;&nbsp; </font>
  <input type="range" id="a" min="0" max="1650" step="50"> &nbsp;
<font size = "6">  <output name="x" for="a">0</output> </font>&nbsp;&nbsp;
</p>
</figure>
<figcaption><font size = "1"><i><b>Visualisierung 1:</b> Dynamische Entwicklung der Mangrovenpopulation über die Modellierungszeit</i></font></figcaption>
<p>


Im nachfolgenden Video wurde das Modellgebiet in zehn Sektoren unterteilt. Dargestellt wird die dynamische Entwicklung der Mangrovenpopulation und der Salzkonzentration im Bodenwasser sowie die Biomasse der Mangroven in den einzelnen Sektoren. Im Vergleich zur vorhergehenden Visualisierung ist in diesem Video eine Hauptursache der Ausbildung der typischen Waldstruktur zu erkennen, nämlich die Aufkonzentrierung des Salzgehalts im Bodenwasser durch Transpirationsprozesse der Mangroven. Die hohe Korrelation zwischen Salzkonzentration und Biomasse in den einzelnen Sektoren ist bereits ab einer Modelllaufzeit von 40 Jahren zu erkennen. Bereits ab 100 Jahren ist die sich langsam ausbildende, für Mangrovenwälder typische, Struktur erkennbar.

<br>

<figure>
<iframe src="https://player.vimeo.com/video/481362688" width="640" height="360" frameborder="1" allow="autoplay; fullscreen" allowfullscreen></iframe>
<figcaption><font size = "1"><i><b>Video 1:</b> Dynamische Entwicklung der Mangrovenpopulation und Salzkonzentration im Bodenwasser über die Modellierungszeit</i></font></figcaption>
</figure>

<br>

Die Ergebnisse des &bdquo;<b>Full Models</b>&ldquo; stimmen mit den gemessenen Felddaten qualitativ überein (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4</a>). Dies trifft sowohl auf das Baumhöhenprofil (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4 A</a>) als auch auf das Profil des Salzgehalts des Porenwassers (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4 B</a>) in dem untersuchten Transekt zu. Insbesondere die Variation des Porenwassersalzgehalts konnte gut abgebildet werden (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4 A</a>). Das Bestimmtheitsmaß der Bravais-Pearson-Korellation beträgt für die Baumhöhe R²&nbsp;=&nbsp;0,64 und für die Salinität des Porenwassers R²&nbsp;=&nbsp;0,88. Ein Vergleich der Ergebnisse des &bdquo;<b>Full Models</b>&ldquo; mit den Ergebnissen der beiden Modellvarianten &bdquo;<b>Model Without Feedback</b>&ldquo; und &bdquo;<b>Model Without Tide</b>&ldquo; zeigt eine deutlich schlechtere Wiedergabe der gemessenen Felddaten durch die beiden einfacheren Modelle (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4 C und 4 D</a>). 

<figure>
<a name="Abbildung_4"></a>
<img src="/pictures/exmouth_gulf/Figure_3.png">
<figcaption><font size = "1"><i><b>Abbildung 4:</b> Simulierte und gemessene Baumhöhen des Mangrovenbestands und Porenwassersalinität</i></font></figcaption>
</figure><p>

Die in der <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4</a> eingezeichneten &bdquo;Treatment Averages&ldquo; sind zwei Bereiche, in denen schon seit längerer Zeit die dort wachsenden Mangroven genauer untersucht werden. Ein Vergleich der Ergebnisse dieser Beobachtungen mit den Ergebnissen der Modellierung zeigt ebenfalls eine hohe Übereinstimmung.

Um die Auswirkungen der Berücksichtung der zeitlichen Dynamik der Gezeiten und der Pflanzenwasserentnahme auf den Salzgehalt im Porenwasser zu untersuchen, wurde diese mit folgender Formel normiert:

<figure>
<div align="center">
<img src="/pictures/exmouth_gulf/formel.png" width="50%">
</div>
</figure><p>

Diese relativen Auswirkungen sind in nachfolgender <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_5">Abbildung 5</a> für die Baumhöhe und den Porenwassersalzgehalt abgebildet. Ein Wert von Null würde bedeuten, dass sich die Ergebnisse zwischen Full Model und dem jeweiligen vereinfachtem Modelltyp nicht unterscheiden. Je größer der Wert wird, umso höher ist die Abweichung.

<figure>
<a name="Abbildung_5"></a>
<img src="/pictures/exmouth_gulf/Figure_3_2.png">
<figcaption><font size = "1"><i><b>Abbildung 5:</b> Relative Auswirkung der Nichtberücksichtigung des Tidenhubs ("Model Wihtout Tide") und der Pflanzenwasserentnahme ("Model Without Feedback")</i></font></figcaption>
</figure><p>

Aufgrund der größeren Auswirkungen des Tidenhubs im seenahen Bereich kann das Modell &bdquo;<b>Without Tide</b>&ldquo; sowohl die Bäumhöhen als auch den Porenwassersalzgehalt hier nur mit relativ großer Abweichung im Vergleich zum &bdquo;<b>Full Model</b>&ldquo; abbilden. Je weiter man sich aber in Richtung Festland bewegt, desto geringer werden die Wasserstandsschwankungen aufgrund der Gezeiten. Die Baumhöhen und Salzgehalte können in diesem Bereich (x > 75 m) mit geringeren relativen Abweichungen zum &bdquo;<b>Full Model</b>&ldquo; abgebildet werden.

Das Modell &bdquo;<b>Without Feedback</b>&ldquo; hat insbesondere im mittleren bis landseitigem Bereich (60 m < x < 165 m) des Transsekts Probleme, die Wachstumshöhe der Mangroven so abzubilden, wie es das &bdquo;<b>Full Model</b>&ldquo; macht. In diesem Bereich kommt es zur Aufkonzentrierung der Salinität des Bodenwassers durch die Pflanzenwasserentnahme, welche in diesem Modelltyp aber nicht abgebildet wird.

## Speziendominanz

Im vorangegangenem Abschnitt wurde gezeigt, dass MANGA mit der Berücksichtigung von Salzkonzentration im Bodenwasser und des Tidenhubs in der Lage ist, die für Mangrovenwälder typischen Waldstrukturen abzubilden. Mit Hilfe der umfangreichen Parametrisierungsmöglichkeiten des Baumwachstumsmodells (siehe hierzu auch den Abschnitt <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Parametrisierung">Parametrisierung</a>) kann mit MANGA auch das Wachstum einzelner bestimmter Individuenarten untersucht werden. Verschiedene Mangrovenarten zum Beispiel weisen verschiedene Toleranzen gegenüber zu hohen Salzgehalten auf. In diesem Projekt wurde das Wachstumsverhalten der beiden Arten Avicennia marina (&bdquo;<a href="https://www.biologie-seite.de/Biologie/Avicennia_marina">graue Mangrove</a>&ldquo;) und Rhizophora mangle (&bdquo;<a href="https://www.biologie-seite.de/Biologie/Rote_Mangrove">rote Mangrove</a>&ldquo;) genauer betrachtet.

<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abbildung 6</a> zeigt die Speziendominanz dieser beiden Mangrovenarten bei unterschiedlichen Salzkonzentration (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_6">Tabelle 6</a>) im Bodenwasser. Die verschiedenen in der Abbildung dargestellten Setups unterscheiden sich nur hinsichtlich der Randbedingungen der seeseitigen und landseitigen Salzkonzentrationen des Bodenwassers. Für die Betrachtung der Speziendominanz im Modellgebiet wir die Speziendominanz d eingeführt und wie folgt definiert:

<figure style="width:75%">
<div align="center">
<img src="/pictures/exmouth_gulf/formel_normierung_speziendominanz_2.jpg" style="width:70%">
</div>
</figure><p>

V<sub>i</sub>(x,t) stehen hierbei für das Volumen der im betrachteten Zeitschritt (t) und X-Koordinatenabschnitt (x) vorhandenen Mangrovenarten Rhizophora mangle (V<sub>Rhi</sub>(x,t)) und Avicennia marina (V<sub>Avi</sub>(x,t)).

<table>
<tablecaption align="top"><font size = "1"><i><b>Tabelle 6:</b> Setupkonfiguration</i></font></tablecaption>
<a name="Tabelle_6"></a>
            <tr>
                <th>Setup</th>
                <td style="text-align: center;">A</td>
		<td style="text-align: center;">B</td>
		<td style="text-align: center;">C</td>
                <td style="text-align: center;">D</td>
		<td style="text-align: center;">E</td>
		<td style="text-align: center;">F</td>
            </tr>
            <tr>
                <th>seeseitige Salinität [g/kg]</th>
                <td>15</td>
		<td>15</td>
		<td>25</td>
                <td>50</td>
		<td>50</td>
		<td>35</td>
            </tr>
            <tr>
                <th>landseitige Salinität [g/kg]</th>
                <td>25</td>
		<td>40</td>
		<td>55</td>
                <td>60</td>
		<td>45</td>
		<td>35</td>
            </tr>
</table>
<br>

<figure>
<a name="Abbildung_6"></a>
<img src="/pictures/exmouth_gulf/Spezien_1.png" style="width:75%">
<figcaption><font size = "1"><i><b>Abbildung 6:</b> Zusammenhang zwischen Salinität des Bodenwassers und Speziendominanz </i></font></figcaption>
</figure><p>

Dabei zeigen die <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abb. 6A bis 6D</a> einen zunächst bedingt durch sowohl seeseitige sowie landseitige niedrigen Salzkonzentrationen monospezifischen Rhizophora-Wald (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abb. 6A</a>). Mit steigender Salinität stellt sich ein Mischwald aus beiden Arten ein (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abb. 6B und 6C</a>). <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abb. 6D</a> bildet dann aufgrund der hohen Salzkonzentrationen einen monospezifischen Avicennia marina Wald ab. Die beiden <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abb. 6E und 6F</a> sind den Setup-Konfigurationen <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abb. 6B und 6C</a> dahingehend ähnlich, dass die Werte der Salinitäten an land- bzw. seeseitiger Seite des Transsekts in etwa den jeweils anderen Wert annehmen. Auch sie bilden somit einen Mischwald aus beiden Arten ab. Diese Ergebnisse werden in folgender <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_7">Abbildung 7</a> noch einmal auf eine andere Art dargestellt.


<figure>
<a name="Abbildung_7"></a>
<img src="/pictures/exmouth_gulf/Spezien_2.png" style="width:75%">
<figcaption><font size = "1"><i><b>Abbildung 7:</b> Speziendominanz bei unterschiedlicher Salinität</i></font></figcaption>
</figure><p>

Bei der Betrachtung der Mischwälder fällt auf, dass sich nur in einzelnen Abschnitten wirkliche Mischpopulationen einstellen. In den meisten Bereichen bildet sich eine eindeutige Dominanz einer Spezienart. Diese scharfen Übergänge zwischen den einzelnen Dominanzzonen zeigen, dass eine Koexistenz zwischen den verschiedenen Arten nur in Bereichen bestimmter Porenwassersalinitäten möglich ist. Die Lage der Grenzen und die Änderung der Speziendominanz d (Steigung der Kurve) hängen von den individuenspezifischen Parametern im Baumwachstumsmodell ab. Zu Beachten ist hier, dass der Salzgehalt im Bodenwasser auch durch die Individuenanzahl pro Fläche und die Baumhöhen beeinflusst wird. Diese beiden Kennwerte werden wiederum von eben jenen individuenspezifischen Parametern beeinflusst. 

Die Kopplung zwischen Pflanzenwasserhaushalt und Porenwasser beeinflusst folglich die Ausbildung der Waldstruktur maßgeblich. In den Setups die zur Ausbildung eines Mischwaldes führen entstehen entweder zwei- (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abbildungen 6C und 6E</a>) oder dreizonige (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_6">Abbildungen 6B und 6F</a>) Mischwälder. Die beiden Zonen an see- und landseitigem Modellrand werden dabei maßgeblich durch die Parameter der Salinität als Randbedingung definiert. In der Modellmitte kommt es durch die Transpiration der Mangroven zu einer Aufkonzentration des Porenwassersalzgehalts. Überschreitet diese einen gewissen Wert, dominiert die salzresistentere Art Avicennia marina.


Wie auch in <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_8">Abbildung 8</a> dargestellt, stimmen die Ergebnisse der Betrachtung der Speziendominanz im Modell mit den gemessenen Felddaten in denen im Projekt betrachteten Transsekten überein.

<figure>
<a name="Abbildung_5"></a>
<img src="/pictures/exmouth_gulf/Spezien_3.png" style="width:75%">
<figcaption><font size = "1"><i><b>Abbildung 8:</b> Vergleich von Feldmessungen und Modellergebnissen</i></font></figcaption>
</figure><p>

Die Modellsoftware MANGA ist folglich in der Lage nicht nur die sich entwickelnde Struktur eines Mangrovenwaldes abzubilden, sondern auch dessen Zusammensetzung aus verschiedenen Spezien.


# Fazit

Mit Hilfe des &bdquo;<b>Full Models</b>&ldquo; konnte die für Mangrovenwälder typische Struktur abgebildet werden. Konkret konnte die Waldstruktur des Avicennia marina Monokulturwalds im betrachteten Gebiet im Exmouth-Golf in Western Australia mit den zur Verfügung stehenden Felddaten auf eine übereinstimmende Weise reproduziert werden. Die Abweichungen der Baumhöhen und des Salzgehalts des Bodenwassers zwischen Modell und gemessenen Werten liegen im Bereich der Variablität der Feldmessungen. MANGA ist hierzu auch ohne weitere Kalibrierung der pflanzenspezfischen Parameter in der Lage. Im &bdquo;<b>Full Model</b>&ldquo; konnten Bereiche im Modellgebiet erkenntlich gemacht werden, in denen entweder die Gezeiten oder die Vegetation die Struktureigenschaften maßgeblich beeinflusst. 

Aufgrund der Ergebnisse der Modellierung muss davon ausgegangen werden, dass eine korrekte Abbildung des Mangrovenwachstums mit MANGA nur unter Berücksichtigung des Tidenhubs und der Einflüsse der Wasserentnahme der Mangroven aus dem Untergrund möglich ist. Eine Kalibrierung der Pflanzenparameter ist hierfür nicht notwendig. Ebenfalls nicht berücksichtigt werden Heterogenitäten hydrogeologischer Eigenschaften des Untergrunds, z.B. die hydraulische Leitfähigkeit oder Porosität betreffend. 

Die durch die Pflanzenwasserentnahme verursachten Gradienten der Salzkonzentration im Bodenwasser wirken sich vor allem im landseitigen Bereich signifikant auf die Wachstumsdynamik der Mangrovenpopulation aus. Weiter lässt sich aus den Ergebnissen schließen, dass der Einfluss der Gezeiten ein Haupteinflussfaktor auf die Gradienten der Salzkonzentration im Bodenwasser ist. Dieser Einfluss ist am seeseitigen Ende des Transsekts am größten. Mit sinkender Höhe der Flut, bzw. kleinerer Überflutungsdauer, nimmt die Rückkopplung zwischen Pflanzenwasser- und Bodenwasserhaushalt dabei eine immer größere Bedeutung an.

Mit Hilfe der Sensitivtätsanalyse des Modells hinsichtlich der Speziendominanz konnte gezeigt werden, dass die Artenzusammensetzung durch die gekoppelte Betrachtung von Bodenwasserhaushalt und Pflanzenwasserentnahme über die Systemgrenze hinweg beschrieben werden kann. Durch die Variation von nur zwei Parametern (vgl. <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_3">Tabelle 3</a>), die sich direkt auf die Wasseraufnahme der Bäume auswirken, konnten typische Zonierungsmuster in Mangroven-Mischwäldern reproduziert werden. Dies gelang auch mit nur grob geschätzten pflanzenspezifischer Parameter für eine der beiden Arten. Werden die Randbedingungen der Salzkonzentrationen an land- und seeseitiger Seite beide sehr hoch oder sehr niedrig gewählt bilden sich überwiegend Wälder aus Monokulturen aus. Wählt man einen moderaten Mittelwert der Salinitäten bilden sich Mischwälder aus beiden Arten. Diese weisen Zonen mit klarer Dominanz einer Art auf, die durch scharfe Übergänge getrennt sind. Diese Übergänge hängen dabei nachweislich vom Bodendwassersalzgehalt ab. Die Spezienzusammensetzung im Modell stimmt mit den gemessenen Felddaten überein.

# Ausblick

In der Literatur gibt es Hinweise darauf, dass sich Mangroven über die Zeit an ihre Umweltbedingungen anpassen. Eine niedrigere Salzkonzentration im Bodenwasser sorgt für eine höhere Xylemleitfähigkeit und damit für eine größere Transpiration. Gleichzeitig sorgt eine geringe Salzkonzentration im Untergrund aber auch für höhere Blattwasserpotentiale, die die Transpiration hemmen. Diese sich gegenseitig ausgleichenden Prozesse sorgen für insgesamt etwa gleichbleibende Transpirationsraten bei unterschiedlichen Salinitäten des Porenwassers. Eine genauere Betrachtung dieser Prozesse kann dabei helfen, die Fähigkeit der Mangroven ihre Physiologie an entsprechenden Standorten vorherrschende Umweltbedingungen anzupassen detailiert zu untersuchen.

Der Niederschlag wurde in diesem Projekt, wie bereits weiter oben beschrieben, nicht dynamisch und als eigener Prozess integriert, sondern über die landseitige konstante Randbedingung des Wasserstands und Salzgehalts abgebildet. Der Exmouth-Golf ist im Allgemeinen eine Region mit sehr niedrigen Jahrsniederschlagssummen. Die Variabilität der einzelnen Regenereignisse ist jedoch sehr hoch. Durch Zyklone kommt es regelmäßig zu ausgeprägten Starkregenereignissen, die einen nicht unerheblichen Anteil an der Gesamtsumme des Niederschlags ausmachen. Der Einfluss des Niederschlags auf die Mangrovenpopulation wurde indirekt durch das Setzen unterschiedlicher Werte der Randbedingung der landseitigen Porenwassersalinität untersucht. Da sich diese Randbedingung als sehr sensitive Größe gezeigt hat, folgt daraus, dass auch der Niederschlag einen Einfluss auf die Zusammensetzung der Mangrovenarten und im Allgemeinen die Ausbildung der typischen Mangrovenwaldstrukturen hat. Im Zuge des Klimawandels ist davon auszugehen, dass Starkregenereignisse bzw. Extremwettersituationen im Allgemeinen zunehmen werden und der Meeresspiegel ansteigt. Da das Modell in der Lage war, die Populationen der Realität entsprechend abzubilden, könnte es auch dafür verwendet werden die Auswirkungen des Klimawandels auf die empfindlichen Ökosysteme der Mangrovenwälder zu untersuchen. Weiter kann das Modell wichtige Hinweise bei der Untersuchung sämtlicher Zusammenhänge zwischen Waldstrukturen und Pflanzenmerkmalen liefern. Modelle, die die Prozesse auf konzeptionelleren Ansätzen basierend abbildet als es bei MANGA der Fall ist, können mit letzterem kalibriert und verifiziert werden.
