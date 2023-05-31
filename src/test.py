from atlas import Atlas
import numpy as np
import cv2
import nibabel as nib
import matplotlib.pyplot as plt

if __name__=="__main__":
    atlas = Atlas(".\\assets\\annotations", ".\\assets\\annotations\\calibrate.json")
    # ax = plt.figure().add_subplot(projection='3d')
    # for organName in atlas.organs:
    #     organ = atlas.organs[organName]
    #     orgx, orgy, orgz = np.where(organ.voxelCloud > 0)
    #     ax.scatter(orgx[0::500], orgy[0::500], orgz[0::500], label=organName)
    # ax.set_xlim(0, 600)
    # ax.set_ylim(0, 600)
    # ax.set_zlim(0, 600)
    # ax.legend()
    # plt.show()
