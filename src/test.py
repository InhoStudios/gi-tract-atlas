from atlas import Atlas
import numpy as np
import cv2
import nibabel as nib

if __name__=="__main__":
    atlas = Atlas(".\\assets\\annotations", ".\\assets\\annotations\\calibrate.json")
    organName="Cecum"
    organ = atlas.organs[organName]
    # cv2.imshow("img", organ.voxelCloud[100])
    # cv2.imshow("img2", organ.voxelCloud[200])
    # cv2.waitKey(0)