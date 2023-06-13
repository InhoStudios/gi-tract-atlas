import numpy as np
from skimage.measure import marching_cubes
import meshio
import plotly.graph_objects as go

# generate mesh from voxel
# read mesh

class Mesh:
    def __init__(self, vertices:np.ndarray, faces:np.ndarray):
        self.vertices = vertices
        self.faces = faces
    
    def save_mesh(self, file_path:str):
        pass

def generate_mesh_from_voxels(voxels:np.ndarray, threshold:int=None, step_size:int=1, save_file:str=None) -> tuple[np.ndarray, np.ndarray]:
    """
    Parameters:
    voxels: 3D array of voxels (from nifti, or generated)
    threshold: threshold level to include from voxels in volume mesh. if not set, threshold is 95% of the maximum value
    step_size: step size for creating vertices
    save_file: file path to save .obj file to. if not set, no file is saved
    
    Returns:
    vertices: list of vertices
    faces: list of triangles
    """
    if (threshold == None):
        maxval = np.max(voxels)
        threshold = int(maxval * 0.95)
    vertices, faces, _, _ = marching_cubes(voxels, threshold, step_size)
    if (save_file != None):
        mesh = meshio.Mesh(vertices, {"triangle": faces})
        meshio.write(save_file, mesh, file_format="obj")

    return vertices, faces


def read_mesh_from_file(file:str) -> tuple[np.ndarray, np.ndarray]:
    """
    Parameters:
    file: .obj file path to read mesh from

    Returns:
    vertices: list of vertices
    faces: list of triangles
    """
    mesh = meshio.read("mesh.obj")
    vertices = mesh.points
    faces = mesh.cells["triangle"]

    return vertices, faces

def visualize_meshes(meshes:list):
    data = []
    for mesh in meshes:
        pass
    figure = go.Figure(data=meshes)
