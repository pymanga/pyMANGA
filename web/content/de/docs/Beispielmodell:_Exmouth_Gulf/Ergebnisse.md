---
title: "Das Modell (Arbeitstitel)"
linkTitle: "Das Modell (Arbeitstitel)"
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





# Modellgebiet

Im Modell wird ein Transekt von 185 m Länge und 10 m Breite abgebildet (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_1">Abbildung 1</a>).
Zur Evaluierung der Modellergebnisse werden sowohl Allometrydaten aus einer Transektenmessung, als auch Messergebnisse einer Langzeitstudie verwendet. In der Langzeitstudie werden die Auswirkungen von Düngung auf das Wachstum von insgesamt 72 Mangroven, von denen jeweils die Hälfte an der land- und an der seeseitigen Seite des Transekts steht, dokumentiert (siehe auch <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4</a>).

<figure>
<a name="Abbildung_1"></a>
<img src="/pictures/exmouth_gulf/Transect_Sketch.png">
<figcaption><font size = "1"><i><b>Abbildung 1:</b> Modellgebiet</i></font></figcaption>
</figure><br>


# Modellierung (Arbeitstitel)

## Modellvarianten

Das Mangrovenwachstum wurde mit Hilfe von drei verschiedenen Modellen simuliert (siehe auch <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_1">Tabelle 1</a>). 

Im Modell <b>"Model Without Feedback"</b> werden die dynamischen Veränderungen der abiotischen Einflüsse (Gezeiten, Grundwasserneubildung und Salzgehalt des Meerwassers (!!!!!!nicht dynamisch abgedildet, oder?) über entsprechende Randbedinungen berücksichtigt. Der Einfluss der Pflanzenwasserentnahme auf den Salzgehalts des Porenwassers wurde nicht abgebildet.

Das Modell <b>"Model Without Tide"</b> berücksichtigt die Auswirkungen der Pflanzenwasserentnahme auf den Salzgehalt des Porenwassers und alle abiotischen Einflüsse des ersten Modells - mit Außnahme der Gezeiten.

Die dritte Modellvariante (<b>"Full Model"</b>) bildet schließlich sowohl die Dynamik der Gezeiten als auch die Kopplung der Pflanzenwasserentnahme und des Porenwassers ab.

Nachfolgende <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_1">Tabelle 1</a> fasst die Spezifikationen der drei Modellvarianten zusammen.

<figure>
<figcaption align="top"><font size = "1"><i><b>Tabelle 1:</b> Modellvarianten</i></font></figcaption>
<a name="Tabelle_1"></a>
<table border="1" rules="all" width="100%">
 <tr>
  <td  width="27%" style="text-align: center; vertical-align: middle;" style="display:none;">
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
   Gezeiten
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle;">
   Kopplung Pflanzenwasserhaushalt und Porenwasser
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
   Sonstige abiotische Faktoren
  </td>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle;">
   Model Without Feedback
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle;">
    <font color="red" size="5"> <b> &#10008; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle;">
   Model Without Tide
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="red" size="5"> <b> &#10008; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle;">
   Full Model
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
 </tr>
</table>
</figure>
<br>

## Diskretisierung 

### Grundwassermodell

Das Grundwassermodell bildet den Untergrund mit einem Gitter der Ausmaße 10 m x 230 m x 3 m auf fünf FEM-Layern mit 5880 Zellen ab. Nachfolgende <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_2">Abbildung 2</a> zeigt die räumliche Diskretisierung aus seeseitiger Perspektive.

<figure>
<a name="Abbildung_2"></a>
<img src="/pictures/exmouth_gulf/dis.png">
<figcaption><font size = "1"><i><b>Abbildung 2:</b> Räumliche Diskretisierung des Grundwassermodells</i></font></figcaption>
</figure><p>

Die Mangroven entnehmen dem Untergrund Bodenwasser aus einer Tiefe von 40 cm bis 80 cm unter der Geländeoberkante. <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_3">Abbildung 3</a> zeigt das Modellgebiet (Grau) und den Bereich der Wasserentnahme durch die Mangroven (Blau). Zu beachten ist die 50-fache Skalierung in z-Richtung. 

<figure>
<a name="Abbildung_3"></a>
<img src="/pictures/exmouth_gulf/model_area_legend.png">
<figcaption><font size = "1"><i><b>Abbildung 3:</b> Bereich der Wasserentnahme durch Mangroven</i></font></figcaption>
</figure><p>

Zeitlich diskretisiert wird das Grundwassermodell mit einer Zeitschrittlänge von einer Stunde. Der Tidenhub als dynamische Randbedingung wird mit der Zeitreihe der Jahre 1991 bis 1993, die über die gesamte Modelllaufzeit immer wieder wiederholt wird, abgebildet.

### Baumwachstumsmodell

Da jede Mangrove als einzelnes Individuum abgebildet wird findet eine räumliche Diskretisierung im eigentlichen Sinne nicht statt. Zeitlich wird das Baumwachstumsmodell mit einer Zeitschrittlänge von einem halben Jahr (1 a = 365.25 d) diskretisiert.

## Randbedingungen

### Grundwassermodell




## Parametrisierung

In den nachfolgenden Tabellen finden sich die Parametrisierungen des Untergrunds (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_2">Tabelle 2</a>) und der Mangroven (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_3">Tabelle 3</a>), globale Gewichtungsfaktoren (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_4">Tabelle 4</a>) sowie die Anfangswerte der Geoemtrieen der Mangrovensetzlinge (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Tabelle_5">Tabelle 5</a>).

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
<td style="text-align: left;">1 × 10<sup>-9</sup> m<sup>2</sup>/s</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>β</em><sub><em>T</em></sub></span></td>
<td style="text-align: left;">transversale Dispersivität</td>
<td style="text-align: left;">0.5 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>β</em><sub><em>L</em></sub></span></td>
<td style="text-align: left;">longitudinale Dispersivität</td>
<td style="text-align: left;">1 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>ρ</em></span></td>
<td style="text-align: left;">Dichte von Wasser</td>
<td style="text-align: left;">1 × 10<sup>3</sup> kg/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>μ</em></span></td>
<td style="text-align: left;">dynamische Viskosität</td>
<td style="text-align: left;">1 × 10<sup>-3</sup> Pas</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>κ</em></span></td>
<td style="text-align: left;">intrinsische Permeabilität</td>
<td style="text-align: left;">5 × 10<sup>-11</sup> m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>Φ</em></span></td>
<td style="text-align: left;">Porosität des Untergrunds</td>
<td style="text-align: left;"><span class="math inline">0.5</span></td>
</tr>
</tbody>
</table>

<!--english version

<table>
<thead>
<tr class="header">
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Parameter Name</th>
<th style="text-align: left;">Value</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>D</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Molecular diffusion coefficient</td>
<td style="text-align: left;">1 × 10<sup>-9</sup> m<sup>2</sup>/s</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>β</em><sub><em>T</em></sub></span></td>
<td style="text-align: left;">Transversal dispersivity</td>
<td style="text-align: left;">0.5 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>β</em><sub><em>L</em></sub></span></td>
<td style="text-align: left;">Longitudinal dispersivity</td>
<td style="text-align: left;">1 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>ρ</em></span></td>
<td style="text-align: left;">Water density</td>
<td style="text-align: left;">1 × 10<sup>3</sup> kg/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>μ</em></span></td>
<td style="text-align: left;">Dynamic Viscosity</td>
<td style="text-align: left;">1 × 10<sup>-3</sup> Pas</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>κ</em></span></td>
<td style="text-align: left;">Intrinsic permeability</td>
<td style="text-align: left;">5 × 10<sup>-11</sup> m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>Φ</em></span></td>
<td style="text-align: left;">Soil porosity</td>
<td style="text-align: left;"><span class="math inline">0.5</span></td>
</tr>
</tbody>
</table>


-->

### Botanik

#### Wasserhaushalt der Mangroven


<table>
<tablecaption align="top"><font size = "1"><i><b>Tabelle 3:</b> Parametrisierung der biotischen Faktoren</i></font></tablecaption>
<a name="Tabelle_3"></a>
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
<td style="text-align: left;">Wasserpotential der Mangroven</td>
<td style="text-align: left;">8.15 × 10<sup>6</sup> kg/s<sup>2</sup>/m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>f</em></sub></span></td>
<td style="text-align: left;">Xylem-Leitfähigkeit</td>
<td style="text-align: left;">1.04 × 10<sup>-10</sup> kg/s/m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>L</em><sub><em>p</em></sub> ⋅ <em>k</em><sub><em>g</em><em>e</em><em>o</em></sub></span></td>
<td style="text-align: left;">Feine Wurzelpermeabilität  ⋅  Skalierungsfaktor</td>
<td style="text-align: left;">1.32 × 10<sup>-11</sup> kg/s/m<sup>4</sup></td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Maintenance cost per biomass</td>
<td style="text-align: left;">1.4 × 10<sup>-6</sup> kg/s/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>g</em><em>r</em><em>o</em><em>w</em><em>t</em><em>h</em></sub></span></td>
<td style="text-align: left;">Skalierungsfaktor der Wachstumsgeschwindigkeit</td>
<td style="text-align: left;">2.5 × 10<sup>-3</sup></td>
</tr>
</tbody>
</table>

#### Globale Gewichtungsfaktoren

<table>
<tablecaption align="top"><font size = "1"><i><b>Tabelle 4:</b> Globale Gewichtungsfaktoren</i></font></tablecaption>
<a name="Tabelle_4"></a>
<thead>
<tr class="header">
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Gewichtungsfaktor</th>
<th style="text-align: left;">Wert</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>C</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Sonnenstrahlung</td>
<td style="text-align: left;">5 × 10<sup>-8</sup> kg/s/m<sup>2</sup></td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>σ</em></span></td>
<td style="text-align: left;">erste Steigung der Sigmoidfunktion</td>
<td style="text-align: left;">1.5 × 10<sup>-2</sup> </td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>σ</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">zweite Steigung der Sigmoidfunktion</td>
<td style="text-align: left;">5 × 10<sup>-2</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>ω</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">Skalierungsfaktor für Baumhöhenwachstum</td>
<td style="text-align: left;">0.5</td>
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
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Geometrische Abmessung</th>
<th style="text-align: left;">Wert</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Wurzelradius</td>
<td style="text-align: left;">0.26 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>C</em></sub></span></td>
<td style="text-align: left;">Kronenradius</td>
<td style="text-align: left;">0.2 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stammradius</td>
<td style="text-align: left;">0.005 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Wurzeltiefe</td>
<td style="text-align: left;">0.004 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>C</em></sub></span></td>
<td style="text-align: left;">Kronenhöhe</td>
<td style="text-align: left;">0.004 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stammhöhe</td>
<td style="text-align: left;">0.015 m</td>
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

# Runtime [Arbeitstitel]

Um die Mangroven im Modellgebiet abzubilden, bedarf es der Herstellung einer stabilen Population, also dem Erreichen von quasi-stationären Verhältnissen. Hierzu werden zunächst 30 Mangroven zufällig im Modellgebiet als Setzlinge positioniert. In jedem Zeitschritt (Länge: halbes Jahr) kommen nun 30 neue Mangroven hinzu, die ebenfalls zufällig im Modellgebiet positioniert werden. Aufgrund des wettbewerbsbasiertem Baumwachstumsmodell sterben diese neuen Mangroven mehr oder weniger schnell wieder ab. So ist die Wahrscheinlich, dass eine junge Mangrove im Einzugsgebiet einer bereits älteren sehr schnell wieder stirbt sehr hoch. Ursächlich hierfür ist die überirdische Konkurenz betreffend vor allem das fehlende Sonnenlicht. Durch die Aufkonzentrierung des Salzgehalts, bedingt durch die Entnahme von Frischwasser der anderen Mangroven, entstehen im Porenwasser Salzfahnen. Diese sorgen für schlechtere Wachstumsbedingungen der sich im Abstrom befindenden (jungen) Mangroven. 


# Ergebnisse

Nachfolgende Visualisierung zeigt die dynamische Entwicklung der Mangrovenpopulation im Modellgebiet und die Entwicklung der Biomasse. Gut nachzuvollziehen ist hier bereits in den ersten 100 Zeitschritten die immer stabiler werdende Mangrovenpopulation. Es bilden sich relativ schnell Bereiche über die X-Länge des Transsekts aus, in denen große und somit Mangroven die sehr alt werden wachsen, und solche, in denen junge Mangroven schnell wieder sterben.


<figure id="vis">
<a name="Visualisierung_1"></a>
<form oninput="x.value=parseInt(a.value)" id="slider" >
<script type="text/javascript">
 /*<![CDATA[*/
  document.getElementById("slider").addEventListener("input", aktualisiere);
   function aktualisiere() {
	  var TS = (document.querySelector("output[name=x]")) ;
	  var a = '/pictures/exmouth_gulf/TS/ts_'+TS.value+'.png' ;
          document.getElementById("abb").setAttribute("src", a) ;
}
</script>
<img src="/pictures/exmouth_gulf/TS/ts_0.png" id="abb">
</br>
</br>
<p align="left">
<font size = "6">&nbsp;  Zeitschritt:&nbsp;&nbsp;&nbsp;&nbsp; </font>
  <input type="range" id="a" min="0" max="10" value="0"> &nbsp;
<font size = "6">  <output name="x" for="a">0</output> </font>&nbsp;&nbsp;
</p>
</figure>
<figcaption><font size = "1"><i><b>Visualisierung 1:</b> Dynamische Entwicklung der Mangrovenpopulation über die Modellierungszeit</i></font></figcaption>
<p>

<!--
<p>
<input type="button" value="click to go fullscreen" onclick="toggleFullScreen()">
</p>

<script type="text/javascript">
 /*<![CDATA[*/
function toggleFullScreen() {
  if ((document.fullScreenElement && document.fullScreenElement !== null) ||    
   (!document.mozFullScreen && !document.webkitIsFullScreen)) {
    if (document.documentElement.requestFullScreen) {  
      document.documentElement.requestFullScreen();  
    } else if (document.documentElement.mozRequestFullScreen) {  
      document.documentElement.mozRequestFullScreen();  
    } else if (document.documentElement.webkitRequestFullScreen) {  
      document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);  
    }  
  } else {  
    if (document.cancelFullScreen) {  
      document.cancelFullScreen();  
    } else if (document.mozCancelFullScreen) {  
      document.mozCancelFullScreen();  
    } else if (document.webkitCancelFullScreen) {  
      document.webkitCancelFullScreen();  
    }  
  }  
}

</script>
-->


Nachfolgendes Video zeigt die dynamische Entwicklung der Biomasse im gesamten Modellgebiet und in einzelnen Abschnitten. Gut nachzuvollziehen ist hier die Ausbildung von verschiedenen Zonen unterschiedlicher Wuchshöhe und Individuendichte innerhalb des Mangrovenwalds.

Test mit youtube, SimpleTest:

<iframe width="560" height="315" src="https://www.youtube.com/embed/rtIQ-Zg-t_M" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


<br>
<br>
<br>

Test mit Vimeo:

<br>
<br>
<br>


<iframe src="https://player.vimeo.com/video/481362688" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>





<br>
<br>
<br>


Die Ergebnisse des "<b>Full Models</b>" stimmen mit den gemessenen Felddaten qualitativ überein (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4</a>). Dies trifft sowohl auf das Baumhöhenprofil (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4 A</a>) als auch auf das Profil des Salzgehalts des Porenwassers (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4 B</a>) in dem untersuchten Transekt zu. Insbesondere die Variation des Porenwassersalzgehalts konnte gut abgebildet werden (<a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4 A</a>). Ein Vergleich der Ergebnisse des "Full Models" mit den Ergebnissen der beiden Modellvarianten "Model Without Feedback" und "Model Without Tide" zeigt eine deutlich schlechtere Wiedergabe der gemessenen Felddaten durch die beiden einfacheren Modelle (siehe <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4 C und 4 D</a>). 

<figure>
<a name="Abbildung_4"></a>
<img src="/pictures/exmouth_gulf/Figure_3.png">
<figcaption><font size = "1"><i><b>Abbildung 4:</b> Ergebnisse</i></font></figcaption>
</figure><p>

Die in der <a href="/de/docs/beispielmodell_exmouth_gulf/ergebnisse/#Abbildung_4">Abbildung 4</a> eingezeichneten "Treatment Averages" sind zwei Bereiche, in denen schon seit längerer Zeit die dort wachsenden Mangroven genauer untersucht werden. Ein Vergleich der Ergebnisse dieser Beobachtungen mit den Ergebnissen der Modellierung zeigt ebenfalls eine hohe Übereinstimmung.

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

Aufgrund der größeren Auswirkungen des Tidenhubs im seenahen Bereich kann das Modell "<b>Without Tide</b>" sowohl die Bäumhöhen als auch den Porenwassersalzgehalt hier nur mit reltiv großer Abweichung im Vergleich zum "<b>Full Model</b>" abbilden. Je weiter man sich aber in Richtung Festland bewergt, desto geringer werden die Wasserstandsschwankungen aufgrund der Gezeiten. Die Baumhöhen und Salzgehalte können in diesem Bereich (x > 75 m) mit geringeren relativen Abweichungen zum Full Model abgebildet werden.

Das Modell "<b>Without Feedback</b>" hat insbesondere im mittleren bis landseitigem Bereich <pre>(60 m < x < 165 m) </pre> des Transsekts Probleme, die Wachstumshöhe der Mangroven so abzubilden, wie es das "<b>Full Model</b>" macht. 

!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Fazit

Mit Hilfe des "<b>Full Models</b>" konnte die für Mangrovenwälder typische Struktur abgebildet werden. Die gemessenen Felddaten und modellierten Werte liegen innerhalb der Variabilität der Feldbeobachtungen. MANGA ist hierzu auch ohne weitere Kalibrierung der pflanzenspezfischen Parameter in der Lage. Das "<b>Full Model</b>" konnten Bereiche im Modellgebiet erkenntlich gemacht werden, in denen entweder die Gezeiten oder die Vegetation die Struktureigenschaften maßgeblich beeinflusst. 

Aufgrund der Ergebnisse der Modellierung muss davon ausgegangen werden, dass eine korrekte Abbildung des Mangrovenwachstums mit MANGA nur unter Berücksichtigung des Tidenhubs und der Einflüsse der Wasserentnahme der Mangroven aus dem Untergrund möglich ist. Die durch die Pflanzenwasserentnahme verursachten Gradienten der Salzkonzentration im Grundwasser wirken sich signifikant auf die Wachstumsdynamik der Mangrovenpopulation aus.
