---
title: "Die Grundwasserdomain"
linkTitle: "Die Grundwasserdomain"
weight: 1
description:
---

Zur Simulation des Salztransports im Grundwasser muss eine Repräsentation der Modelldomain erstellt werden.
Dazu benötigen wir eine Domain, in der die Wasserflüsse stattfinden und Randnetze, auf denen wir Randbedingungen definieren können.
Zudem wird ein Gitter benötigt, welches die Subdomain repräentiert, in welcher Bäume über die Wurzeln Wasser aufnehmen.
Das Grundwasserströmungsmodell OGS arbeitet mit <a href="https://www.vtk.org/" target="_blank"> vtk-Gittern</a>.
In diesem Abschnitt wird eine Methode erläutert, wie ein solches Gitter erstellt werden kann.
Hierfür wird ein Beispiel-Python Script genutzt und Abschnittsweise erkärt.
Für das folgende Script wird $vtk>=9.2.0.$ benötigt.

Wir verwenden das Paket *pygmsh* als Hilfsmittel.
Außerdem benötigen wir die Funktionalitäten von *vtk, numpy, os, subprocess* und *absolute_import*.
Entsprechend müssen diese Pakete zu Beginn des Scripts importiert werden:

	from __future__ import absolute_import
	import numpy as np
	import pygmsh
	import os
	import vtk as vtk
	import subprocess 

Mit diesen Paketen ist es nun möglich die benötigten Funktionen und Klassen zu implementieren.

Der Verlauf der Geländeoberkante wird ein einer Funktion beschrieben.
In diesem Beispiel handelt es sich um ein entlang der x-Achse konstant abfallendes Gelände (Steigung *m* in Promille).

    def transectElevation(x, m):
        return float(m * x)
	    
Druck  (in Pa) und Bodensalinität (in ppt) werden ebenfalls durch ortsabhängige Funktionen beschrieben.

    # Pressure at a given point. Here, pressure is 0 at the surface


    def ini_pressure_function(point):
        return -(1000 * 9.81 * (point[2] - transectElevation(x=point[0])))

    # Concentration at a given point. Here, c_ini is constant 0.035 kg/kg.


    def c(point):
        return .035

Mit der folgenden Funktion wird später das definierte Druck- und Konzentrationsfeld der Domain hinzufügt:

    def addCandPtoMesh(mesh):
        points = mesh.GetPoints()
        # Preparing lists for initial conditions
        p_ini = vtk.vtkDoubleArray()
        p_ini.SetName("p_ini")
        c_ini = vtk.vtkDoubleArray()
        c_ini.SetName("c_ini")
        # Calculating initial conditions
        for point in range(points.GetNumberOfPoints()):
            point = points.GetPoint(point)
            c_ini.InsertNextTuple1(c(point))
            p_ini.InsertNextTuple1(-(1000 * 9.81 *
                                   (point[2] -
                                      transectElevation(x=point[0],
                                                      m=hydraulic_gradient))))
        mesh.GetPointData().AddArray(p_ini)
        mesh.GetPointData().AddArray(c_ini)


Außerdem kann der folgende Block verwendet werden, um ein quaderförmiges Gitter zu erstellen.
Das Gitter ist in drei Schichten mit den Schichtdicken *l_z_top*, *l_z_mid* und *l_z_bottom* unterteilt.
Für jede dieser Schichten kann eine vertikale Auflösung angegeben werden (*num_top*, *num_bottom*, *num_mid*).
Der Parameter *z* gibt eine mögliche Verschiebung der Geländeoberkante, deren prinzipieller Verlauf in *TransectElevation* definiert ist, in Metern vor.
*two_layers* und *three_layers* definiert, wieviele unterschiedliche Schichten vorliegen.
Durch *points_in_y* wird die Ausdehnung bzw Auflösung in die y-Richtung vorgegeben.
*l_x* definiert die Länge des transects und *lcar* die charackteristische Länge des Gitters.

			
    def createSurface(l_x, l_y, z,
                      m, lcar, transect_elevation, geom, origin=[0.,0.,0.]):
        p1 = [origin[0], origin[1], origin[2] + transect_elevation(0, m=m)]
        p2 = [origin[0], origin[1] + l_y, origin[2] +
              transect_elevation(0, m=m)]
        p3 = [origin[0] + l_x, origin[1] + l_y, origin[2] +
              transect_elevation(l_x, m=m)]
        p4 = [origin[0] + l_x, origin[1], origin[2] +
              transect_elevation(l_x, m=m)]
        p1[2] = p1[2] + z
        p2[2] = p2[2] + z
        p3[2] = p3[2] + z
        p4[2] = p4[2] + z
        p1 = geom.add_point(p1, lcar)
        p2 = geom.add_point(p2, lcar)
        p3 = geom.add_point(p3, lcar)
        p4 = geom.add_point(p4, lcar)

        points = [p1, p2, p3, p4]

        lines = []
        lines.append(geom.add_line(points[0], points[3]))
        lines.append(geom.add_line(points[3], points[2]))
        lines.append(geom.add_line(points[2], points[1]))
        lines.append(geom.add_line(points[1], points[0]))

        line_loop = geom.add_curve_loop(lines)
        surface = geom.add_plane_surface(line_loop)

        baum_1 = [20, 5, transect_elevation(20, m=m) + z]
        p_baum_1 = geom.add_point(baum_1, lcar / 2)
        geom.in_surface(p_baum_1, surface)

        baum_2 = [22.5, 5, transect_elevation(22.5, m=m) + z]
        p_baum_2 = geom.add_point(baum_2, lcar / 2)
        geom.in_surface(p_baum_2, surface)
        return surface


    ## Generates a mesh for given parameters
    #  @param z: shift in z-direction
    #  @param l_z_top: depth of the top layer (if only one layer created, value
    #  defines the depth)
    #  @param l_z_bottom: depth of the bottom layer (if two layers created, value
    #  defines the depth of the bottom layer)
    #  @param num_top: resolution of top layer
    #  @param num_bottom: resolution of bottom layer
    #  @param l_y: y-extension of grid
    #  @param l_z_mid: depth of mid layer, if constructed
    #  @param num_mid: resolution of mid layer
    #  @param l_x: x-extension of model
    #  @param lcar: characteristic lengthscale in x-direction
    #  @param transect_elevation: Function, which returns a z-value for given x-val
    def meshGen(z,
                l_z_top,
                l_z_bottom=0,
                num_top=1,
                num_bottom=0,
                l_y=10,
                l_z_mid=0,
                num_mid=0,
                l_x=230,
                lcar=5,
                transect_elevation=transectElevation,
                m=1e-3):

        with pygmsh.occ.Geometry() as geom:
            geom.characteristic_length_min = lcar / 20
            geom.characteristic_length_max = lcar * 20
            # Creating the points as they are supposed to be later
            surface = createSurface(l_x, l_y, z,
                                    m, lcar, transect_elevation, geom)
            geom.extrude(surface, [0, 0, -l_z_top], num_layers=num_top)
            if l_z_mid != 0:
                mid_surface = geom.copy(surface)
                geom.translate(mid_surface, [0, 0, -l_z_top])

                geom.extrude(
                    mid_surface, [0, 0, -l_z_mid], num_layers=num_mid)
            if l_z_bottom != 0:
                bottom_surface = geom.copy(surface)
                geom.translate(bottom_surface, [0, 0, -l_z_top - l_z_mid])

                geom.extrude(
                    bottom_surface, [0, 0, -l_z_bottom], num_layers=num_bottom)

            mesh = geom.generate_mesh()
            return mesh

Nun geht es an das eigentliche Erstellen des Meshes.
Als erstes werden die Punkte unseres Meshes über die zuvor programmierte Funktion *meshGen* erzeugt und für später abgespeichert.


    # Generating bulk mesh
    hydraulic_gradient = 1e-3
    bulky = meshGen(z=0,
                    l_z_top=0.4,
                    l_z_bottom=0.3,
                    num_top=3,
                    num_bottom=1,
                    l_z_mid=.8,
                    num_mid=2,
                    m=hydraulic_gradient,
                    l_x=30,
                    l_y=10,
                    lcar=2)
    # Extraction of Bulk Mesh points
    points = bulky.points
    
Nun wird das zuvor mit *pygmsh* erzeugte Gitter nochmals als vtk-grid erzeugt.
Dabei werden auch gleich die bulk-node-ids als Eigenschaftsvektor abgespeichert.

    bulk = vtk.vtkUnstructuredGrid()
    bulk_points = vtk.vtkPoints()
    for i in range(len(points)):
        point = points[i]
        iD = i
        bulk_points.InsertNextPoint(point)
    bulk.SetPoints(bulk_points)

        
Im Folgenden werden noch Zelldaten, die für die späteren Rechnungen mit OGS notwendig sind, hinzugefügt.
Dazu gehört das Durchlässigkeitsfeld des Bodens und die Eigenschaft der Zellen als Tetrahedrons.

    propertyvector = vtk.vtkDoubleArray()
    propertyvector.SetName("permeability")
    bulk_cells = vtk.vtkCellArray()
    for cell_point_ids in bulky.cells[2].data:
        cell = vtk.vtkTetra()
        for i in range(4):
            cell.GetPointIds().SetId(i, cell_point_ids[i])

        propertyvector.InsertNextTuple1(3.0e-11)

        bulk_cells.InsertNextCell(cell)
    bulk.SetCells(10, bulk_cells)
    bulk.GetCellData().AddArray(propertyvector)

Da während der Mesherzeugung einige Punkte doppelt erzeugt wurden, muss noch der vtkStaticCleanUnstructuredGrid Filter angewendet werden, um diese zu zusammenzuführen.
Anschließend wird die Eigenschaft "bulk_node_ids", welche für OGS notwendig ist, eingefügt.

    # Clean the data with non-zero tolerance
    clean1 = vtk.vtkStaticCleanUnstructuredGrid()
    clean1.SetInputData(bulk)
    clean1.ToleranceIsAbsoluteOff()
    clean1.SetTolerance(0.0001)
    clean1.RemoveUnusedPointsOn()

    clean1.Update()
    bulk = clean1.GetOutput()
    propertyvector = vtk.vtkDataArray.CreateDataArray(
        vtk.VTK_UNSIGNED_LONG_LONG)
    propertyvector.SetName("bulk_node_ids")
    for i in range(bulk.GetNumberOfPoints()):
        propertyvector.InsertNextTuple1(i)
    bulk.GetPointData().AddArray(propertyvector)

Nachdem noch das initiale Druckfeld und das initiale Konzentrationsfeld. hinzugefügt wurden, kann das bulk-mesh gespeichert werden.

    # Adding pressure and concentration field to mesh
    addCandPtoMesh(bulk)
    # Output of bulk-mesh
    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName("my_first_model.vtu")
    writer.SetInputData(bulk)
    writer.Write()

Jetzt ist die Hauptdomain fertig und mit Eigenschaften belegt.
Als nächstes wird der Layer gesampled, aus dem die Bäume Wasser entnehmen.
Dafür wird wieder unser zuvor definiertes *meshGen* verwendet.



    # Generating source mesh
    sourcey = meshGen(z=-.4,
                      l_z_top=0.4,
                      num_top=1,
                      m=hydraulic_gradient,
                      l_x=30,
                      l_y=10,
                      lcar=2)
    source = vtk.vtkUnstructuredGrid()
    source_points = vtk.vtkPoints()
    for i in range(len(sourcey.points)):
        point = sourcey.points[i]
        source_points.InsertNextPoint(point)
    source.SetPoints(source_points)

    source_cells = vtk.vtkCellArray()
    for cell_point_ids in sourcey.cells[2].data:
        cell = vtk.vtkTetra()
        for i in range(4):
            cell.GetPointIds().SetId(i, cell_point_ids[i])
        source_cells.InsertNextCell(cell)
    source.SetCells(10, source_cells)

Für spätere Flussberechnungen muss das Volumen einer jeder Zelle berechnet und in einem Array im Grid gespeichert werden.

    ncells = (source.GetCells().GetNumberOfCells())
    cells = source.GetCells()
    points = source.GetPoints()
    cell_volumes = np.zeros(ncells)
    pts = vtk.vtkIdList()
    cells.InitTraversal()
    propertyvector = vtk.vtkDoubleArray()
    propertyvector.SetName("Volume")
    # Calculating cell volume, as it is required by ogs
    for i in range(ncells):
        cells.GetNextCell(pts)
        if pts.GetNumberOfIds() == 4:
            p0 = np.array(points.GetPoint(pts.GetId(0)))
            p1 = np.array(points.GetPoint(pts.GetId(1)))
            p2 = np.array(points.GetPoint(pts.GetId(2)))
            p3 = np.array(points.GetPoint(pts.GetId(3)))
            v0 = (p1 - p0)
            v1 = (p2 - p0)
            v2 = (p3 - p0)
            V = np.absolute(np.dot(v0, np.cross(v1, v2))) / 6.
            cell_volumes[i] = V

Um die Eigenschaften, die wir der Hauptdomain zugewiesen haben, zu kopieren, wird der *ResampleWithDataset* Filter von vtk verwendet.

    resample_filter = vtk.vtkResampleWithDataSet()
    resample_filter.SetSourceData(bulk)
    resample_filter.SetInputData(source)
    resample_filter.Update()
    source = resample_filter.GetOutput()

    for value in cell_volumes:
        propertyvector.InsertNextTuple1(value)
    source.GetCellData().AddArray(propertyvector)

    # Output of source-mesh
    source_writer = vtk.vtkXMLUnstructuredGridWriter()
    source_writer.SetFileName("my_first_source.vtu")
    source_writer.SetInputData(source)
    source_writer.Write()

Am Ende fehlen nur noch die Boundary meshes.
Zum extrahieren des Boundary Meshes kann die ExtractSurface Utility aus dem opengeosys-Projekt verwendet werden.
Sollte OGS unter Ubuntu betrieben werden funktioniert das so:

    ogs_container_string = "singularity exec ABSOLUTER/PFAD/ZU/PYMANGA/pyMANGA/TreeModelLib/BelowgroundCompetition/OGS/container/ogs_container.sif "

    subprocess.call(ogs_container_string + "ExtractSurface -x -1 -y 0 -z 0 -a 0. -i my_first_model.vtu -o right_boundary.vtu", shell=True)
    subprocess.call(ogs_container_string + "ExtractSurface -x 1 -y 0 -z 0 -a 0. -i my_first_model.vtu -o left_boundary.vtu", shell=True)
    subprocess.call(ogs_container_string + "ExtractSurface -x 0 -y 0 -z -1 -a 30. -i my_first_model.vtu -o top_boundary.vtu", shell=True)
    
Wird OGS unter Windows betrieben funktioniert das so (getestet mit OGS 6.4.0 & 6.4.2):

    gs_utilities_string = "ABSOLUTER/PFAD/ZU/PYMANGA/pyMANGA" \
                           "/TreeModelLib/BelowgroundCompetition/OGS" \
                           "/bin/"
    subprocess.call(ogs_utilities_string + "ExtractSurface -i "
                                           "my_first_model.vtu -o "
                                           "right_boundary.vtu -x -1 -y 0 -z 0 -a 0.")
    subprocess.call(ogs_utilities_string + "ExtractSurface -i "
                                           "my_first_model.vtu -o "
                                           "left_boundary.vtu -x 1 -y 0 -z 0 -a 0.")
    subprocess.call(ogs_utilities_string + "ExtractSurface -i "
                                           "my_first_model.vtu -o "
                                           "top_boundary.vtu -x 0 -y 0 -z -1 -a 30.")
