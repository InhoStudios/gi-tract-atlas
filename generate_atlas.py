from api.gen_nii_atlas import Atlas
# from atlas_man_cal import ManCalAtlas
# from construct_imaios_mesh import IMAIOSMesh
import numpy as np
import cv2
import nibabel as nib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from os.path import join

def displayOrgan(organName, atlas, fig):
    organ = atlas.organs[organName]
    vertices, faces = organ.getMesh()
    # fig.mesh_3d(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2], faces=faces)
    return getMeshFromVerticesAndFaces(vertices, faces)

def getMeshFromVerticesAndFaces(vertices, faces):
    return go.Mesh3d(
        x=vertices[:, 0], 
        y=vertices[:, 1], 
        z=vertices[:, 2], 
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2])
    
if __name__=="__main__":
    atlas = Atlas(join("assets", "annotations"), join("assets", "annotations", "calibrate.json"), save=True)
    # nifti_mouse = nib.load(join("assets", "images", "sagittal_mouse.nii")).get_fdata()
    # # slice1 = 500
    # # slice2 = 610
    # # fig, axis = plt.subplots(1,2)
    # # axis[0].imshow(nifti_mouse[slice1, :, :], 'gray')
    # # axis[1].imshow(nifti_mouse[:, slice2, :], 'gray')
    # # for organName in atlas.organs:
    # #     organ = atlas.organs[organName]
    # #     axis[0].imshow(organ.voxelCloud[slice1, :, :], 'inferno', alpha=0.25)
    # #     axis[1].imshow(organ.voxelCloud[:, slice2, :], 'inferno', alpha=0.25)
    # # plt.show()
    # mouse = IMAIOSMesh()
    # ax = plt.figure().add_subplot(projection='3d')
    # meshes = []
    # m_vertices, m_faces = mouse.getMesh()
    # meshes.append(getMeshFromVerticesAndFaces(m_vertices, m_faces))

    # for organName in atlas.organs:
    #     mesh = displayOrgan(organName, atlas, None)
    #     meshes.append(mesh)
    # fig = go.Figure(data=meshes)
    # fig.show()
