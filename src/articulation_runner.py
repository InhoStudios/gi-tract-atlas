from skimage.measure import marching_cubes
import nibabel as nib
from os.path import join
from . import mesh_processor as mp

# voxels = nib.load(join("data", "stomach.nii")).get_fdata()

mesh = mp.read_mesh_from_file("./data/Stomach.obj")# mp.generate_mesh_from_voxels(voxels, threshold=128, step_size=3, save_file="test.obj")
mp.visualize_meshes([mesh])

