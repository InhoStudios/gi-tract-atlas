import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

from os.path import join

ct = nib.load(".\\assets\\images\\sample\\CT_TS_HEUHR_In111_free_M1039_0h_220721-selfcal.nii")
spect = nib.load(".\\assets\\images\\sample\\SPECT_REG_TS_HEUHR_In111_free_M1039_0h_220721_171kev_04vox_16ss_6it_dc-ac.nii")

ct_arr = ct.get_fdata()
spect_arr = spect.get_fdata()


ct_x, ct_y, ct_z = np.where(ct_arr > 1200)
spect_x, spect_y, spect_z = np.where(spect_arr > 0.02)

ax = plt.figure().add_subplot(projection='3d')
ax.scatter(ct_x[0::250], ct_y[0::250], ct_z[0::250], c='g')
ax.scatter(spect_x[0::50], spect_y[0::50], spect_z[0::50], c='r')
# ax.voxels(img_arr)
ax.set_xlim(0, 600)
ax.set_ylim(0, 600)
ax.set_zlim(0, 600)
plt.show()

class NIFTIManager:
    def __init__(self) -> None:
        self.nii_images = {}
        pass

    def importImage(self, path, name):
        img = nib.load(path)
        self.nii_images[name] = img
