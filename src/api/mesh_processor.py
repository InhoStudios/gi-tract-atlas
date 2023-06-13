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

def generate_mesh_from_voxels(voxels:np.ndarray, *, threshold:int=None, step_size:int=1, save_file:str=None) -> Mesh:
    """
    Parameters:
    voxels: 3D array of voxels (from nifti, or generated)
    threshold: threshold level to include from voxels in volume mesh. if not set, threshold is 95% of the maximum value
    step_size: step size for creating vertices
    save_file: file path to save .obj file to. if not set, no file is saved
    
    Returns:
    Mesh: mesh object of vertices and faces
    """
    if (threshold == None):
        maxval = np.max(voxels)
        threshold = int(maxval * 0.95)
    vertices, faces, _, _ = marching_cubes(voxels, level=threshold, step_size=step_size)
    mesh = Mesh(vertices, faces)
    if (save_file != None):
        mesh.saveMesh(save_file)

    return mesh


def read_mesh_from_file(file:str) -> Mesh:
    """
    Parameters:
    file: .obj file path to read mesh from

    Returns:
    Mesh: mesh object of vertices and faces
    """
    mesh = meshio.read("mesh.obj")
    vertices = mesh.points
    faces = mesh.cells["triangle"]

    return Mesh(vertices, faces)

def visualize_meshes(meshes:list[Mesh]) -> go.Figure:
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
    figure.show()
    return figure