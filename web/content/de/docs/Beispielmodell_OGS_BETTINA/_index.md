---
title: "Beispielmodell: Die Kopplung von OGS und BETTINA"
linkTitle: "Beispielmodell: Die Kopplung von OGS und BETTINA"
weight: 3
description:
---

In diesem Abschnitt wird anhand eines Beispielmodells erklärt, wie das Grundwasserströmungsmodell OGS verwendet werden kann.
Hierbei orientieren wir uns an den Modellsetups aus <a href="https://linkinghub.elsevier.com/retrieve/pii/S0304380020300454" target="_blank">Bathmann et al. 2020</a>.

<figure>
<img src="/pictures/ogs_example/conceptual_setup.png" style="width:90%">
<figcaption><font size = "1"><i><b>Abbildung 1:</b> Skizze des hier reproduzierten Modellsetups.</a></i></font></figcaption>
</figure>

Hier wird beschrieben, wie die benötigten Input-Dateien erstellt und modifiziert werden können.
Das gesamte Setup besteht aus 5 Dateien, die die Grundwaserdomain definieren. Zudem wird noch ein python Script zur Definition der Randbedingungen, ein OGS-Steuerfile und das pyMANGA Steuerfile benötigt.

<figure>
<img src="/pictures/ogs_example/input_files.png" style="width:90%">
<figcaption><font size = "1"><i><b>Figure 1:</b> Skizze der benötigten Input Dateien.</a></i></font></figcaption>
</figure>
