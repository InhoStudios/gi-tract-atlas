import numpy as np
from skimage.measure import marching_cubes
from os.path import join
from os import listdir
import json
import cv2

import nibabel as nib

OFFSET_X = 1630
OFFSET_Y = 590

class Atlas:
    def __init__(self, annotationDirectory, calibrationAnnotation) -> None:
        # TODO: Get directory length
        self.calibration: float = None
        self.xOffset: int = None
        self.yOffset: int = None
        self.zOffset: int = None
        self.scale: float = 0.3

        self.atlasDims: tuple = None
        self.affine = None

        self.organs = {}

        self.annotationDirectory = annotationDirectory

        ct = nib.load(".\\assets\\images\\sample\\CT_TS_HEUHR_In111_free_M1039_0h_220721-selfcal.nii")

        annFiles = listdir(annotationDirectory)
        numSlices = 0
        for file in annFiles:
            annList = json.load(open(join(self.annotationDirectory, file)))
            numSlices += len(annList)

        self.calibrateDepth(calibrationAnnotation, numSlices)
        self.calibrateImgSize(ct)
        self.constructAtlasFromList(annFiles, numSlices)
        self.constructImgVoxels()

    def constructAtlasFromList(self, fileList, numSlices):
        if (self.calibration == None):
            print("Requires calibration")
            return
        # get number of slices
        for file in fileList:
            path = join(self.annotationDirectory, file)
            if (path == self.calibrationFile):
                print("Calibration file. Skipping...")
                continue
            print(f"Reading file {file}")
            annotationList = json.load(open(path))
            for annotation in annotationList:
                fname = annotation["documents"][0]["name"]
                index = int(fname.split('.')[0].replace("rat",""))
                try:
                    for entity in annotation["annotation"]["annotationGroups"][0]["annotationEntities"]:
                        name = entity["name"]
                        try:
                            organ = self.organs[name]
                        except(KeyError):
                            organ = Organ(name, 
                                            numSlices, 
                                            self.scale, 
                                            self.calibration, 
                                            self.atlasDims,
                                            self.affine)
                            self.organs[name] = organ
                        organ.appendOrganSlice(index, entity)
                except:
                    print(annotation)

    def calibrateDepth(self, calibrationAnnotation, numSlices):
        f = open(calibrationAnnotation)
        annotation = json.load(f)[0]
        body = annotation["annotation"]["annotationGroups"][0]["annotationEntities"][0]
        domain = []
        for point in body["annotationBlocks"][0]["annotations"][0]["segments"][0]:
            domain.append(point[1])
        minZ = min(domain)
        maxZ = max(domain)
        diff = maxZ - minZ
        self.calibration = 1.0 * float(diff) / float(numSlices)
        self.calibrationFile = calibrationAnnotation
        return self.calibration
    
    def calibrateImgSize(self, inputNifti):
        """
        Parameters:
            inputNifti: nibabel.nifti1.Nifti1Image
        """
        # TODO: use nifi image size to calibrate canvas size for voxelclouds
        shape = inputNifti.get_fdata().shape
        self.atlasDims = shape
        self.affine = inputNifti.affine
        print(self.affine, type(self.affine))
        pass

    def constructImgVoxels(self):
        for organName in self.organs:
            organ = None
            try:
                organ = self.organs[organName]
            except:
                continue
            if (organ != None):
                print(f"Constructing voxel map for {organName}")
                organ.constructVoxelMap(True)
                print("Done")


class Organ:
    def __init__(self, name, numSlices, scale, depth, dims, affine) -> None:
        self.name = name
        self.numSlices = numSlices
        self.slices = [[]] * numSlices
        self.scale = scale
        self.depth = depth * scale
        self.affine = affine
        # offset: [offset_x, offset_y, offset_z]
        self.offset = {
            "x": 124, # OFFSET_X - 36 * 6, # 424.2
            "y": 45, # OFFSET_Y - 80 * 6, # 33
            "z": 50 # 65
        }
        imgSliceDims = (numSlices, dims[1], dims[2])
        self.imageSlices: np.ndarray = np.zeros(imgSliceDims, dtype=np.uint8)
        self.voxelCloud: np.ndarray = np.zeros(dims, dtype=np.uint8)
    
    def appendOrganSlice(self, index, entity):
        for polygon in entity["annotationBlocks"][0]["annotations"]:
            polyPts = np.array(polygon["segments"][0].copy()).astype(int)
            for i, pt in enumerate(polyPts):
                polyPts[i] = [(self.scale * pt[1]) - self.offset['y'], (self.scale * pt[0]) - self.offset['x']]
            self.slices[index].append(polyPts)
            cv2.fillPoly(self.imageSlices[index], pts=[polyPts], color=(255, 255, 255))

    def constructVoxelMap(self, save=False):
        for z in range(self.voxelCloud.shape[0]):
            # i: voxel layer
            i = z - self.offset['z']
            index = float(i) / self.depth
            ind0 = int(np.floor(index))
            if (ind0 < 0):
                continue
            if (ind0 + 1 >= len(self.imageSlices)):
                break
            img0 = self.imageSlices[ind0]
            img1 = self.imageSlices[ind0 + 1]
            img0 = cv2.GaussianBlur(img0, (9, 9), cv2.BORDER_DEFAULT)
            img1 = cv2.GaussianBlur(img1, (9, 9), cv2.BORDER_DEFAULT)
            alpha = (float(i % int(np.round(self.depth)) ) ) / (self.depth)
            additiveImage = np.add(img0 *  (1.0 - alpha), img1 * alpha)
            self.voxelCloud[z][np.where(additiveImage > 196)] = 255
        
        self.customCalibration()

        if (save):
            img = nib.Nifti1Image(self.voxelCloud, self.affine)
            nib.save(img, f".\\data\\{self.name}.nii")
            print(f"Saved {self.name} image at ./data/{self.name}.nii")
    
    def customCalibration(self):
        self.voxelCloud = np.swapaxes(self.voxelCloud, 0, 1);
        self.voxelCloud = self.voxelCloud[::-1,::-1,::-1]

        # smooth between slices
        for i, img in enumerate(self.voxelCloud):
            # smoothImg = 
            self.voxelCloud[i] = cv2.GaussianBlur(img, (13, 13), cv2.BORDER_DEFAULT)
        
    def getMesh(self):
        threshold = 196
        step_size = 2
        print("Getting mesh")
        vertices, faces, _, _ = marching_cubes(self.voxelCloud, level=threshold, step_size=step_size)
        return vertices, faces