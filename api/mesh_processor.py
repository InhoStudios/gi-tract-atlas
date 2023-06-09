import numpy as np
from skimage.measure import marching_cubes
import meshio
import plotly.graph_objects as go

# generate mesh from voxel
# read mesh
class Mesh:
    def __init__(self, vertices:np.ndarray, faces:np.ndarray) -> None:
        """
        Parameters
        vertices: input vertices from marching_cubes
        faces: input faces from marching_cubes
        """
        self.vertices = vertices
        self.faces = faces
    
    def saveMesh(self, file_path:str) -> bool:
        """
        Parameters
        file_path: path to save the mesh to
        Returns
        true on success, false on failure
        """
        try:
            mesh = meshio.Mesh(self.vertices, {"triangle": self.faces})
            meshio.write(file_path, mesh, file_format="obj")

            return True
        except:
            return False
    
    def getVertices(self) -> np.ndarray:
        return self.vertices
    
    def getFaces(self) -> np.ndarray:
        return self.faces

def generate_mesh_from_voxels(voxels:np.ndarray, *, threshold:int=None, step_size:int=1, file_path:str=None) -> Mesh:
    """
    Parameters:
    voxels: 3D array of voxels (from nifti, or generated)
    threshold: threshold level to include from voxels in volume mesh. if not set, threshold is 95% of the maximum value
    step_size: step size for creating vertices
    file_path: file path to save .obj file to. if not set, no file is saved
    
    Returns:
    Mesh: mesh object of vertices and faces
    """
    if (threshold == None):
        maxval = np.max(voxels)
        threshold = int(maxval * 0.95)
    vertices, faces, _, _ = marching_cubes(voxels, level=threshold, step_size=step_size)
    mesh = Mesh(vertices, faces)
    if (file_path != None):
        mesh.saveMesh(file_path)

    return mesh

def read_mesh_from_file(file_path:str) -> Mesh:
    """
    Parameters:
    file_path: .obj file path to read mesh from

    Returns:
    Mesh: mesh object of vertices and faces
    """
    mesh = meshio.read(file_path)
    vertices = mesh.points
    faces = mesh.cells_dict["triangle"]

    return Mesh(vertices, faces)

def visualize_meshes(meshes:list) -> go.Figure:
    """
    Parameters:
    meshes: list of all Meshes you want to render

    Returns:
    figure: Plotly GO figure
    """
    data = []
    for mesh in meshes:
        vertices = mesh.getVertices()
        faces = mesh.getFaces()
        go_mesh = go.Mesh3d(
            x=vertices[:, 0], 
            y=vertices[:, 1], 
            z=vertices[:, 2], 
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2]
        )
        data.append(go_mesh)
    figure = go.Figure(data=data)
    return figure

def decimate_mesh(mesh: Mesh, num_vertices: int) -> Mesh:
    """
    Parameters:
    mesh: input Mesh object
    num_vertices: the target number of vertices to decimate to

    Returns:
    mesh: decimated mesh
    """
    num_faces = 3 * num_vertices
    ms = ml.MeshSet()
    pml_mesh = PMLMesh(mesh.vertices, mesh.faces)
    ms.add_mesh(pml_mesh)
    while (ms.current_mesh().vertex_number() > num_vertices):
        ms.apply_filter("meshing_decimation_quadric_edge_collapse", targetfacenum=num_faces, preservenormal=True)
        num_faces = num_faces - (ms.current_mesh().vertex_number() - num_vertices)
    
    m = ms.current_mesh()
    print('Output mesh has', m.vertex_number(), 'vertex and', m.face_number(), 'faces')
    return Mesh(m.vertex_matrix(), m.face_matrix())