import numpy as np
from os.path import join
from os import listdir
import json
import cv2

import nibabel as nib

OFFSET_X = 1630 - 17 * 6
OFFSET_Y = 590 - 21 * 6

class Atlas:
    def __init__(self, annotationDirectory, calibrationAnnotation) -> None:
        # TODO: Get directory length
        self.calibration: int = None
        self.xOffset: int = None
        self.yOffset: int = None
        self.zOffset: int = None
        self.scale: float = 0.30

        self.atlasDims: tuple = None
        self.affine = None

        self.organs = {}

        self.annotationDirectory = annotationDirectory

        ct = nib.load(".\\assets\\images\\sample\\CT_TS_HEUHR_In111_free_M1039_0h_220721-selfcal.nii")

        annFiles = listdir(annotationDirectory)
        numSlices = len(annFiles)

        self.calibrateDepth(calibrationAnnotation, numSlices)
        self.calibrateImgSize(ct)
        self.constructAtlasFromList(annFiles)
        self.constructImgVoxels()

    def constructAtlasFromList(self, fileList):
        if (self.calibration == None):
            print("Requires calibration")
            return
        numSlices = len(fileList)
        for file in fileList:
            path = join(self.annotationDirectory, file)
            if (path == self.calibrationFile):
                print("Calibration file. Skipping...")
                continue
            print(f"Reading file {file}")
            annotation = json.load(open(path))[0]
            fname = annotation["documents"][0]["name"]
            index = int(fname.split('.')[0].replace("rat",""))
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
        self.calibration = int(diff / numSlices)
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
                organ.constructVoxelMap()
                print("Done")


class Organ:
    def __init__(self, name, numSlices, scale, depth, dims, affine) -> None:
        self.name = name
        self.numSlices = numSlices
        self.slices = [[]] * numSlices
        self.scale = scale
        self.depth = int(depth * scale)
        self.affine = affine
        imgSliceDims = (numSlices, dims[1], dims[2])
        self.imageSlices: np.ndarray = np.zeros(imgSliceDims, dtype=np.uint8)
        self.voxelCloud: np.ndarray = np.zeros(dims, dtype=np.uint8)
    
    def appendOrganSlice(self, index, entity):
        for polygon in entity["annotationBlocks"][0]["annotations"]:
            polyPts = np.array(polygon["segments"][0].copy()).astype(int)
            for i, pt in enumerate(polyPts):
                polyPts[i] = [self.scale * (pt[1] - OFFSET_Y), self.scale * (pt[0] - OFFSET_X)]
            self.slices[index].append(polyPts)
            cv2.fillPoly(self.imageSlices[index], pts=[polyPts], color=(255, 255, 255))

    def constructVoxelMap(self):
        for z in range(self.voxelCloud.shape[0]):
            # i: voxel layer
            i = z - 39 * 3
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
            alpha = (float(i % self.depth)) / self.depth
            additiveImage = np.add(img0 *  (1.0 - alpha), img1 * alpha)
            self.voxelCloud[i][np.where(additiveImage > 128)] = 255
        
        img = nib.Nifti1Image(self.voxelCloud, self.affine)
        nib.save(img, f".\\data\\{self.name}.nii")
        print(f"Saved {self.name} image at ./data/{self.name}.nii")