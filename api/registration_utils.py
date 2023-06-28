def segment_high_contrast(nifti_file_path: str, threshold: int=0.95):
    """
    Parameters:
    nifti_file_path: file path of the nifti image to load and segment
    threshold: percentage of maximum response to threshold the contrast to

    Returns:
    NIFTI image of only the highest values
    """
    nifti_img = nib.load(nifti_file_path)
    img_voxels = nifti_img.get_fdata()
    resultant_voxels = np.zeros(img_voxels.shape)
    indices = np.where(img_voxels > threshold * np.max(img_voxels))
    resultant_voxels[indices] = img_voxels[indices]
    return resultant_voxels