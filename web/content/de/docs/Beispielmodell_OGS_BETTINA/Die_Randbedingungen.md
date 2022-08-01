---
title: "Die Randbedingungen"
linkTitle: "Die Randbedingungen"
weight: 1
description:
---

Für das Grundwasserströmungsmodell müssen Randbedingungen und Quelltherme festgelegt werden.
In diesem Beispiel werden die Randbedingungen komplett über ein python-script definiert.
Grundsätzlich gibt es auch andere Wege Randbedingungen zu definieren.
Für Informationen, die über die präsentierten Beispiele hinaus gehen stellt die OGS-community eine ausführliche Dokumentation bereit (www.opengeosys.org).

Das in diesem Beispiel genutzte Script beginnt wie üblich mit Packetimporten.
Wir benötigen die Packete *OpenGeoSys, vtk, numpy, math* und *os*.

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

	def pressure_value(z, tidal_cycle):
	    return 1000 * 9.81 * (tidal_cycle - z)

Mit dieser Hilfsfunktion kann nun der Druck entlang unserer Ränder definiert werden.
Wir führen eine Randbedingung ein, die entweder keinen Fluss über die Grenzflächen zulässt oder bei Überspülung offene Durchmischung mit dem Meerwasser erlaubt.

	## Dirichlet BCs
	class BCSea_p_D(OpenGeoSys.BoundaryCondition):

	    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
		x, y, z = coords
		tide = tidal_cycle(t)
		value = pressure_value(z, tide)
		if tide < z:
		    return (False, 0)
		else:
		    return (True, value)
		    
	class BCLand_p_D(OpenGeoSys.BoundaryCondition):

	    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
		value = pressure_value(z, 0)
		return (True, value)

Für die Konzentrations-Randbedingungen wird angenommen, dass bei Überspülung mit Meerwasser Durchmischung stattfinden kann.


	## Dirichlet BCs
	class BCSea_C(OpenGeoSys.BoundaryCondition):

	    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
		x, y, z = coords
		tide = tidal_cycle(t)
		value = seaward_salinity
		if tide > z:
		    return (True, value)
		else:
		    return (False, 0)
		    
	class BCLand_C(OpenGeoSys.BoundaryCondition):

	    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
		value = seaward_salinity
		return (True, value)

Nun muss nur noch die Meerwassersalinität zugewiesen werden.
Ebenfalls können Periodendauern und Amplituden der Moden unserer Tide angepasst werden.
Für erste eigene Simulationen stellen wir den Tidenhub aus.

	seaward_salinity = 0.035
	tide_daily_amplitude = 0
	tide_monthly_amplitude = 0
	tide_daily_period = 60 * 60 * 12.
	tide_monthly_period = 60. * 60 * 24 * 31 / 2.
	
Nun gilt es nurnoch die Randbedingungen als Objekte für OpenGeoSys zu definieren:

bc_tide_p = BCSea_p_D()
bc_land_p = BCLand_p_D()
bc_tide_C = BCSea_C()
bc_land_C = BCLand_C()

