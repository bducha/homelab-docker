import bpy
import sys
import bmesh
from scipy.spatial import Delaunay
import numpy as np

def create_mesh_from_points(xyz_file):
    # Remove existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create a new mesh
    mesh = bpy.data.meshes.new('terrain_mesh')
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections["Collection"]
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    
    chunk_size = 10000
    

    # Read points from the XYZ file
    print(f"Reading points from {xyz_file}...")
    
    with open(xyz_file, 'r') as f:
        chunk = []
        for i, line in enumerate(f):
            arr = line.strip().split(",")
            point = (float(arr[0]), float(arr[1]), float(arr[2]))
            chunk.append(point)

            if len(chunk) >= chunk_size:
                # Process the chunk
                process_chunk(chunk, mesh, obj)
                chunk = []

        # Process the last chunk
        if chunk:
            process_chunk(chunk, mesh, obj)
    # Set the object location to the origin
    obj.location = (0, 0, 0)

def process_chunk(chunk, mesh, obj):
    print("Scaling points")
    # Scale the points to fit within a reasonable range
    x_coords = np.array([point[0] for point in chunk])
    y_coords = np.array([point[1] for point in chunk])
    z_coords = np.array([point[2] for point in chunk])

    x_min = np.min(x_coords)
    y_min = np.min(y_coords)
    z_min = np.min(z_coords)


    scaled_points = [(x - x_min, y - y_min, z - z_min) for x, y, z in chunk]

    # Create a bmesh for the mesh
    bm = bmesh.new()

    # Add vertices to the bmesh
    print("Adding vertices to the bmesh...")

    for point in scaled_points:
        bm.verts.new(point)

    bm.verts.ensure_lookup_table()

    # Create faces using Delaunay triangulation
    print("Creating faces using Delaunay triangulation...")
    points_array = np.array([(point[0], point[1]) for point in scaled_points])
    triangulation = Delaunay(points_array)

    for triangle in triangulation.simplices:
        face = (bm.verts[triangle[0]], bm.verts[triangle[1]], bm.verts[triangle[2]])
        bm.faces.new(face)

    # Finalize the bmesh and create the mesh
    print("Finalizing the bmesh and creating the mesh...")

    bm.to_mesh(mesh)
    bm.free()

    # Add a material to the object
    # material = bpy.data.materials.new('terrain_material')
    # material.use_nodes = True
    # material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.2, 0.4, 0.6, 1)  # Blue color
    # obj.data.materials.append(material)

    # Select the object for export
    obj.select_set(True)

def main():
    # Get the arguments passed after "--"
    args = sys.argv[sys.argv.index("--") + 1:]
    xyz_file = args[0]
    fbx_file = args[1]

    # Create the mesh from the points
    create_mesh_from_points(xyz_file)

    # Export the mesh to FBX
    print("Exporting the mesh to FBX...")

    bpy.ops.export_scene.fbx(
        filepath=fbx_file,
        use_selection=True,
        global_scale=1.0,
        apply_unit_scale=True,
        axis_forward='-Z',
        axis_up='Y'
    )

if __name__ == "__main__":
    main()