from atlas import Atlas
import numpy as np
import cv2
import nibabel as nib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def displayOrgan(organName, atlas, fig):
    organ = atlas.organs[organName]
    vertices, faces = organ.getMesh()
    # fig.mesh_3d(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2], faces=faces)
    return go.Mesh3d(
        x=vertices[:, 0], 
        y=vertices[:, 1], 
        z=vertices[:, 2], 
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2])
    
if __name__=="__main__":
    atlas = Atlas("./assets/annotations", "./assets/annotations/calibrate.json")
    # ax = plt.figure().add_subplot(projection='3d')
    meshes = []
    for organName in atlas.organs:
        mesh = displayOrgan(organName, atlas, None)
        meshes.append(mesh)
    fig = go.Figure(data=meshes)
    fig.update_layout(
        scene = dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        )
    )
    fig.show()
    # displayOrgan("Jejunum", atlas, ax)
    # ax.set_aspect('equal')
    # plt.show()
