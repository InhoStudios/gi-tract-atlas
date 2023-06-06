from atlas import Atlas
import numpy as np
import cv2
import nibabel as nib
import matplotlib.pyplot as plt

def displayOrgan(organName, atlas, ax):
    organ = atlas.organs[organName]
    vertices, faces = organ.getMesh()
    ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles=faces, cmap='cool')
    
if __name__=="__main__":
    atlas = Atlas(".\\assets\\annotations", ".\\assets\\annotations\\calibrate.json")
    ax = plt.figure().add_subplot(projection='3d')
    displayOrgan("Duodenum", atlas, ax)
    displayOrgan("Jejunum", atlas, ax)
    ax.set_aspect('equal')
    plt.show()
