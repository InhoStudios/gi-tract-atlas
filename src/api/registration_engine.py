import nibabel as nib
import numpy as np

# segment high contrast organs
def segment_high_contrast(nifti_file_path: str, threshold: int=0.95):
    """
    Parameters:
    nifti_file_path: file path of the nifti image to load and segment
    """
    nifti_img = nib.load(nifti_file_path)
    img_voxels = nifti_img.get_fdata()
    resultant_voxels = np.zeros(img_voxels.shape)
    resultant_voxels[np.where(img_voxels > threshold * np.max(img_voxels))]


# match points with robust point matching
# register two key points near clavicle and pelvis

"""

"""