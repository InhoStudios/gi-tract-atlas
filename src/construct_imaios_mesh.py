import nibabel as nib
import numpy as np
from skimage.measure import marching_cubes
from os.path import join
from os import listdir
import cv2
from api import mesh_processor
from api.mesh_processor import Mesh

class IMAIOSMesh:
    def __init__(self) -> None:
        print("loading image")
        self.nifti = nib.load(join("assets", "images", "sagittal_mouse.nii"))
        print("image loaded, getting voxel data")
        self.voxels = self.nifti.get_fdata()
        print("generating mesh")
        self.generateMesh()
        del self.voxels
        del self.nifti

    def generateMesh(self):
        threshold = 0.92 * np.max(self.voxels)
        print("highest response: ", np.max(self.voxels), "\nthreshold: ", threshold)
        step_size = 3
        self.vertices, self.faces, _, _ = marching_cubes(self.voxels, level=threshold, step_size=step_size)
        print("mesh generated")
        mesh = Mesh(self.vertices, self.faces)
        mesh.saveMesh("./data/skeleton.obj")

    def getMesh(self):
        return self.vertices, self.faces