import nibabel as nib

# segment high contrast organs
def segment_high_contrast(nifti_file_path: str):
    """
    Parameters:
    nifti_file_path: file path of the nifti image to load and segment
    """
    nifti_img = nib.load(nifti_file_path)
    img_voxels = nifti_img.get_fdata()
    pass


# match points with robust point matching
# register two key points near clavicle and pelvis

"""

"""