---
title: "Die Randbedingungen"
linkTitle: "Die Randbedingungen"
weight: 2
description:
---

Für das Grundwasserströmungsmodell müssen Randbedingungen und Quelltherme festgelegt werden.
In diesem Beispiel werden die Randbedingungen komplett über ein python-script definiert.
Grundsätzlich gibt es auch andere Wege Randbedingungen zu definieren.
Für Informationen, die über die präsentierten Beispiele hinaus gehen stellt die OGS-Community <a href="https://www.opengeosys.org/" target="_blank">eine ausführliche Dokumentation</a> bereit.

In diesem Beispiel werden entlang der yz-Grenzflächen der Domain Randbedingungen vorgegeben. 
Außerdem wird - tidenabhängig - zeitlich begrenz ein Meerwasseranschluß an der Geländeoberfläche erzeugt.
Das in diesem Beispiel genutzte Script beginnt wie üblich mit Paketimporten.
Wir benötigen die Pakete *OpenGeoSys, vtk, numpy, math* und *os*.

	import OpenGeoSys
	import vtk as vtk
	import numpy as np
	from math import pi, sin
	import os

Für spätere Einführung von tidaler Aktivität können die Gezeiten wie folgt beschrieben werden:

    def tidal_cycle(t):
        return (sin(2 * pi * t / tide_daily_period) *
            (tide_daily_amplitude +
             tide_monthly_amplitude * sin(2 * pi * t / tide_monthly_period)))

Wichtig ist eigentlich nur, wie sich der Druck entlang unserer Randflächen berechnet.
Ein einfacher Ansatz wäre:

    def transectElevation(x, m=1e-3):
        return float(m * x)

    def pressure_value(z,x, tidal_cycle):
        return 1000 * 9.81 * (tidal_cycle - z + transectElevation(x))

Mit dieser Hilfsfunktion kann nun der Druck entlang unserer Ränder definiert werden.
Wir führen jeweils eine Randbedingung ein, die entweder keinen Fluss über die Grenzflächen zulässt (kein Anschluss an das Meerwasser) oder bei Überspülung offene Durchmischung mit dem Meerwasser erlaubt.

    ## Dirichlet BCs
    class BCSea_p_D(OpenGeoSys.BoundaryCondition):

        def getDirichletBCValue(self, t, coords, node_id, primary_vars):
            x, y, z = coords
            tide = tidal_cycle(t)
            value = pressure_value(z, x, tide)
            if tide < z:
                return (False, 0)
            else:
                return (True, value)

    class BCLand_p_D(OpenGeoSys.BoundaryCondition):

        def getDirichletBCValue(self, t, coords, node_id, primary_vars):
            x, y, z = coords
            value = pressure_value(z, x, 0)
            return (True, value)

Für die Konzentrations-Randbedingungen wird angenommen, dass bei Überspülung mit Meerwasser Durchmischung stattfinden kann.


    ## Dirichlet BCs
    class BCSea_C(OpenGeoSys.BoundaryCondition):

        def getDirichletBCValue(self, t, coords, node_id, primary_vars):
            x, y, z = coords
            tide = tidal_cycle(t)
            value = seaward_salinity
            if tide + 1e-6 > z:
                return (True, value)
            else:
                return (False, 0)

    class BCLand_C(OpenGeoSys.BoundaryCondition):

        def getDirichletBCValue(self, t, coords, node_id, primary_vars):
            value = seaward_salinity
            return (True, value)

Nun muss nur noch die Meerwassersalinität zugewiesen werden.
Außerdem können Periodendauer und Amplitude den Moden der Tide angepasst werden.
Für dieses Beispiel wird der Tidenhub deaktiviert (Amplitude = 0).
Diese kann später durch Änderung der Parameter in der Funktion *tidal_cycle* hinzugefügt werden.
Dies kann später angepasst werden.

    seaward_salinity = 0.035
    tide_daily_amplitude = 0
    tide_monthly_amplitude = 0
    tide_daily_period = 60 * 60 * 12.
    tide_monthly_period = 60. * 60 * 24 * 31 / 2.
	
Nun gilt es nur noch die Randbedingungen als Objekte für OGS zu definieren:

    bc_tide_p = BCSea_p_D()
    bc_land_p = BCLand_p_D()
    bc_tide_C = BCSea_C()
    bc_land_C = BCLand_C()

PyMANGA fügt diesem Script automatisch noch die für die Wasseraufnahme der Bäume benötigten Funktionalitäten hinzu.
