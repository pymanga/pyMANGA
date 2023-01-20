from __future__ import absolute_import
import numpy as np
import pygmsh
import os
import vtk as vtk
import subprocess


hydraulic_gradient = -0.1/22.
l_z_top = 0.3
l_z_mid = 0.3
l_z_bottom = 1.4
num_top = 1
num_mid = 1
num_bottom = 3
l_y = 22
l_x = 22
lcar = 3.
c_left = 0.025
c_right = 0.035

def transectElevation(x, m):
    return float(m * x)


# Pressure at a given point. Here, pressure is 0 at the surface


def ini_pressure_function(point):
    return -(1000 * 9.81 * (point[2] - transectElevation(x=point[0])))

# Concentration at a given point. Here, c_ini is constant 0.035 kg/kg.


def c(point):
    c_sea = c_left + (c_right-c_left)*point[0]/l_x
    return c_sea


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

    baum_1 = [10, 11, transect_elevation(10, m=m) + z]
    p_baum_1 = geom.add_point(baum_1, lcar / 3)
    geom.in_surface(p_baum_1, surface)

    baum_2 = [12, 11, transect_elevation(12, m=m) + z]
    p_baum_2 = geom.add_point(baum_2, lcar / 3)
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


# Generating bulk mesh
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


bulk = vtk.vtkUnstructuredGrid()
bulk_points = vtk.vtkPoints()
for i in range(len(points)):
    point = points[i]
    iD = i
    bulk_points.InsertNextPoint(point)
bulk.SetPoints(bulk_points)



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


# Adding pressure and concentration field to mesh
addCandPtoMesh(bulk)
# Output of bulk-mesh
writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName("my_first_model.vtu")
writer.SetInputData(bulk)
writer.Write()

# Generating source mesh
sourcey = meshGen(z=-l_z_top,
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
source_writer.SetFileName("my_first_model.vtu")
source_writer.SetInputData(source)
source_writer.Write()


ogs_utilities_string = "ABSOLUTE/PATH/TO/PYMANGA/pyMANGA" \
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
