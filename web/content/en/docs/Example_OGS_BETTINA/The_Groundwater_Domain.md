---
title: "The groundwater domain"
linkTitle: "The groundwater domain"
weight: 4
description:
---

The groundwater model domain is represented by a a grid or mesh.
The first step is to create this flow mesh and associated boundary meshes for the definition of the boundary conditions, including the inner boundary for the layer with the roots of the trees.
The groundwater flow model OGS works with <a href="https://www.vtk.org/" target="_blank"> vtk grids</a>.
This section explains one method of creating such a grid, using a Python script.
*vtk>=9.2.0* is required to successfully run the following script.

We use the *pygmsh* package as a resource.
In addition, we need the functionalities of *vtk, numpy, os, subprocess* and *absolute_import*.
Accordingly, these packages must be imported at the beginning of the script:

	from __future__ import absolute_import
	import numpy as np
	import pygmsh
	import os
	import vtk as vtk
	import subprocess 

With these packages it is now possible to implement the required functions and classes.

First, we define all required mesh configurations.

    hydraulic_gradient = 1e-2
    l_z_top = 0.1
    l_z_mid = 0.2
    l_z_bottom = 1.7
    num_top = 2
    num_mid = 1
    num_bottom = 3
    l_y = 15
    l_x = 130
    lcar = 5
    c_sea = 0.035

The course of the elevation of the ground surface is described as a function of x with x=0 at the seaward boundary of the domain.
In this example, the terrain is constantly sloping along the x-axis (x in [m], m in [m/m]).

    def transectElevation(x, m):
        return float(m * x)
	    
Pressure (in Pa) and porewater salinity (in kg per kg) are described using position dependent functions.

    # Pressure at a given point. Here, pressure is 0 at the surface


    def ini_pressure_function(point):
        return -(1000 * 9.81 * (point[2] - transectElevation(x=point[0])))

    # Concentration at a given point. Here, c_ini is constant 0.035 kg/kg.


    def c(point):
        return c_sea

The following function will be used later to add the defined pressure and concentration field to the domain:

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

The following block can be used to create a cuboid domain.
Vertically, the domain is divided into three layers with the layer thicknesses *l_z_top*, *l_z_mid* and *l_z_bottom*.
If one of the lengths is set to zero, the layer is not created.
A vertical resolution can be specified for each of these layers (*num_top*, *num_bottom*, *num_mid*).
The *z* parameter specifies a possible displacement of the top edge of the terrain, the basic course of which is defined in *TransectElevation*, in meters.
*l_x* defines the length of the transect and *lcar* the characteristic length of the grid.

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
    #  @param l_z_mid: depth of mid layer
    #  @param l_z_bottom: depth of the bottom layer
    #  @param num_top: resolution of top layer
    #  @param num_mid: resolution of mid layer
    #  @param num_bottom: resolution of bottom layer
    #  @param l_x: x-extension of domain
    #  @param l_y: y-extension of domain
    #  @param lcar: characteristic lengthscale in x- and y-direction in meters 
    #  @param transect_elevation: Function, which returns a z-value for given x-val
    #  @param m: terrain slope
    def meshGen(z,
                l_z_top=l_z_top,
                l_z_mid=l_z_mid,
                l_z_bottom=l_z_bottom,
                num_top=num_top,
                num_mid=num_mid,
                num_bottom=num_bottom,
                l_y=l_y,
                l_x=l_x,
                lcar=lcar,
                transect_elevation=transectElevation,
                m=hydraulic_gradient):

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

Now, the functions are defined and the mesh can be created.
The points of our mesh are created using the previously programmed function *meshGen* and saved for later.

    # Generating bulk mesh
    hydraulic_gradient = 1e-3
    bulky = meshGen(z=0,
                    l_z_top=l_z_top,
                    l_z_mid=l_z_mid,
                    l_z_bottom=l_z_bottom,
                    num_top=num_top,
                    num_mid=num_mid,
                    num_bottom=num_bottom,
                    l_y=l_y,
                    l_x=l_x,
                    lcar=lcar,
                    transect_elevation=transectElevation,
                    m=hydraulic_gradient)
    # Extraction of Bulk Mesh points
    points = bulky.points
    
Now the grid previously created with *pygmsh* is created again as vtk-grid.
The bulk-node-ids are also saved as a property vector.

    bulk = vtk.vtkUnstructuredGrid()
    bulk_points = vtk.vtkPoints()
    for i in range(len(points)):
        point = points[i]
        iD = i
        bulk_points.InsertNextPoint(point)
    bulk.SetPoints(bulk_points)

        
In the following, cell data, which are necessary for later calculations with OGS, are added.
This includes the permeability field of the soil and the property of the cells as tetrahedrons.

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

Since some points were created twice during mesh creation, the vtkStaticCleanUnstructuredGrid filter must be applied to merge them.
Then the property "bulk_node_ids", which is necessary for OGS, is inserted.

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

When the initial pressure field and the initial concentration field have been added, the bulk mesh can be saved.

    # Adding pressure and concentration field to mesh
    addCandPtoMesh(bulk)
    # Output of bulk-mesh
    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName("my_first_model.vtu")
    writer.SetInputData(bulk)
    writer.Write()

Now the main domain is ready and filled with properties.
Next, the layer from which the trees take water is sampled.
It has to fit one of the previous layers
Our previously defined *meshGen* is used again for this.

    # Generating source mesh
    sourcey = meshGen(z=-.4,
                      l_z_top=l_z_mid,
                      l_z_mid=0,
                      l_z_bottom=0,
                      num_top=num_mid,
                      num_mid=0,
                      num_bottom=0,
                      l_y=l_y,
                      l_x=l_x,
                      lcar=lcar,
                      transect_elevation=transectElevation,
                      m=hydraulic_gradient)
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

For later flow calculations, the volume of each cell must be calculated and stored in an array in the grid.

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

To copy the properties we assigned to the main domain, vtk's *ResampleWithDataset* filter is used.

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

At the end, only the boundary meshes are missing.
Finally, we create the boundary meshes using the ExtractSurface utility from the OGS project.
If OGS is operated under Ubuntu, it works like this:

    ogs_container_string = "singularity exec ABSOLUTE/PATH/TO/PYMANGA/pyMANGA/TreeModelLib/BelowgroundCompetition/OGS/container/ogs_container.sif "

    subprocess.call(ogs_container_string + "ExtractSurface -x -1 -y 0 -z 0 -a 0. -i my_first_model.vtu -o right_boundary.vtu", shell=True)
    subprocess.call(ogs_container_string + "ExtractSurface -x 1 -y 0 -z 0 -a 0. -i my_first_model.vtu -o left_boundary.vtu", shell=True)
    subprocess.call(ogs_container_string + "ExtractSurface -x 0 -y 0 -z -1 -a 30. -i my_first_model.vtu -o top_boundary.vtu", shell=True)
    
If OGS is operated under Windows, it works like this (tested with OGS 6.4.0 & 6.4.2):

    gs_utilities_string = "ABSOLUTE/PATH/TO/PYMANGA/pyMANGA" \
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
