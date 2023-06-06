import numpy as np
from skimage.measure import marching_cubes

threshold = 196

vertices, faces, _, _ = marching_cubes(voxels, level=threshold)

