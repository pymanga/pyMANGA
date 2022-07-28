---
title: "Die Grundwasserdomain"
linkTitle: "Die Grundwasserdomain"
weight: 1
description:
---

Zur Simulation des Salztransports im Grundwasser muss eine Repräsentation der Modelldomain erstellt werden.
Das Grundwasserströmungsmodell OGS arbeitet mit vtk-Gittern.
In diesem Abschnitt wird eine Methode erläutert, wie ein solches Gitter erstellt werden kann.
Hierfür wird ein Beispiel-Python Script genutzt und Abschnittsweise erkärt.

Wir verwenden das Packet pygmsh als Hilfsmittel.
Außerdem benötigen wir die Funktionalitäten von vtk, numpy, os, subprocess und absolute_import.
Entsprechend müssen diese Packete zu Beginn des Scripts importiert werden:

	from __future__ import absolute_import
	import numpy as np
	import pygmsh
	import os
	import vtk as vtk
	import subprocess 

Mit diesen Packeten ist es nun möglich die benötigten Funktionen und Klassen zu implementieren.
Als erstes wird eine Klasse zum erleichterten Speichern und Ermitteln von Zellinformationen erstellt.

	## Just a helper to store data on  CellIds and access the CellVolumes.
	class CellInformation:
	    def __init__(self, source_mesh):
		meshReader = vtk.vtkXMLUnstructuredGridReader()
		meshReader.SetFileName(source_mesh)
		meshReader.Update()
		self.grid = meshReader.GetOutput()
		self.cell_finder = vtk.vtkCellLocator()
		self.cell_finder.SetDataSet(self.grid)
		self.cell_finder.LazyEvaluationOn()
		cells = self.grid.GetCellData()
		self.volumes = cells.GetArray("Volume")

	    def getCellId(self, x, y, z):
		cell_id = self.cell_finder.FindCell([x, y, z])
		return cell_id

	    def getCellVolumeFromId(self, cell_id):
		cell_volume = self.volumes[cell_id]
		return cell_volume

	    def getCellVolumeFromCoordinates(self, x, y, z):
		cell_id = self.getCellId(self, x, y, z)
		return self.getCellVolumeFromId(self, cell_id)

Außerdem kann der Folgende Block verwendet werden, um ein quaderförmiges Gitter zu erstellen.
Das Gitter ist in drei Schichten mit den Schichtdicken l_z_top, l_z_bottom und l_z_mid unterteilt.
Für jede dieser Schichten kann eine vertikale Auflösung angegeben werden (num_top, num_bottom, num_mid)

		
	## Generates a mesh for given parameters
	#  @param z: shift in z-direction
	#  @param l_z_top: depth of the top layer (if only one layer created, value
	#  defines the depth)
	#  @param l_z_bottom: depth of the bottom layer (if two layers created, value
	#  defines the depth of the bottom layer)
	#  @param num_top: resolution of top layer
	#  @param num_bottom: resolution of bottom layer
	#  @param y_extend: y-extension of grid
	#  @param l_z_mid: depth of mid layer, if constructed
	#  @param num_mit: resolution of mid layer
	#  @param two_layers: True, if model consists of exatly two vert. layers
	#  @param three_layers: True, if model consists of exatly three vert. layers
	#  @param l_x: x-extension of model
	#  @param lcar: characteristic lengthscale in x-direction
	#  @param points_in_y: resolution in y-direction
	#  @param transect_elevation: Function, which returns a z-value for given x-val
	def meshGen(z,
		    l_z_top,
		    l_z_bottom=0,
		    num_top=1,
		    num_bottom=0,
		    y_extend=10,
		    l_z_mid=0,
		    num_mid=0,
		    two_layers=False,
		    three_layers=True,
		    l_x=230,
		    lcar=5,
		    points_in_y=3,
		    transect_elevation=transectElevation,
		    m=1e-3):

	    l_y = y_extend
	    n_surfaces = int(l_x / lcar)
	    x_array = np.linspace(-20, -20 + l_x, num=int(n_surfaces + 1))

	    surfaces = []
	    line_loops = []

	    with pygmsh.occ.Geometry() as geom:
		geom.characteristic_length_min = lcar / 20 
		geom.characteristic_length_max = lcar * 20  

		for i in range(n_surfaces):
		    # Creating the points as they are supposed to be later
		    p1 = [x_array[i], 0., transect_elevation(x_array[i], m=m)]
		    p2 = [x_array[i], y_extend, transect_elevation(x_array[i], m=m)]
		    p3 = [x_array[i + 1], y_extend, transect_elevation(x_array[i + 1], m=m)]
		    p4 = [x_array[i + 1], 0., transect_elevation(x_array[i + 1], m=m)]
		    p1[2] = p1[2] + z
		    p2[2] = p2[2] + z
		    p2[1] = lcar * (points_in_y - 1)
		    p3[2] = p3[2] + z
		    p3[1] = lcar * (points_in_y - 1)
		    p4[2] = p4[2] + z            
		    p1 = geom.add_point(p1, lcar)
		    p2 = geom.add_point(p2, lcar)
		    p3 = geom.add_point(p3, lcar)
		    p4 = geom.add_point(p4, lcar)
		    
		    points = [p1,p2,p3,p4]

		    lines = []
		    lines.append(geom.add_line(points[0], points[3]))
		    lines.append(geom.add_line(points[3], points[2]))
		    lines.append(geom.add_line(points[2], points[1]))
		    lines.append(geom.add_line(points[1], points[0]))

		    line_loop = geom.add_curve_loop(lines)
		    surface = geom.add_plane_surface(line_loop)
		    line_loops.append(line_loop)
		    surfaces.append(surface)

		 # Extrude set of surfaces in third dimension (z)
		surfaces_final = []
		for surface, line_loop in zip(surfaces, line_loops):
		    geom.extrude(surface, [0, 0, -l_z_top],
		                 num_layers=num_top)  #, recombine = True)
		    surfaces_final.append(surface)
		    # If two layers, varying resolution can be used for the two layers
		    if two_layers:
		        surface21 = geom.add_plane_surface(line_loop)
		        geom.translate(surface21, [0, 0, -l_z_top])
		        geom.extrude(surface21, [0, 0, -l_z_bottom],
		                     num_layers=num_bottom)
		        surfaces_final.append(surface21)
		    # If three layers, varying resolution can be used for the three layers
		    if three_layers:
		        surface21 = geom.add_plane_surface(line_loop)
		        geom.translate(surface21, [0, 0, -l_z_top])
		        geom.extrude(surface21, [0, 0, -l_z_mid], num_layers=num_mid)
		        surfaces_final.append(surface21)

		        surface31 = geom.add_plane_surface(line_loop)
		        geom.translate(surface31, [0, 0, -l_z_top - l_z_mid])
		        geom.extrude(surface31, [0, 0, -l_z_bottom],
		                     num_layers=num_bottom)
		        surfaces_final.append(surface31)
		# Combining all quaders (extruded surfaces)
		geom.boolean_union(surfaces_final)
		
		mesh = geom.generate_mesh()

		# Rescaling y-coordinates of all points
		points = mesh.points
		for point, i in zip(points, range(len(points))):
		    if point[1] > 0:
		        point[1] = point[1] / (lcar * (points_in_y - 1)) * l_y
		        points[i] = point
		# Updating points
		mesh.points = points
		return mesh

		mesh.write("test.vtk")
