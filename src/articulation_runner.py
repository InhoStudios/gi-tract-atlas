from skimage.measure import marching_cubes
import nibabel as nib
from os.path import join

voxels = nib.load(join("data", "stomach.nii")).get_fdata()

vertices, faces, _, _ = marching_cubes(voxels, level=50)

print(type(vertices), type(faces))
print(vertices, faces)

