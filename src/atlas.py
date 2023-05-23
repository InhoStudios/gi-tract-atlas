import numpy as np
from os.path import join
from os import listdir
import json

class Atlas:
    def __init__(self, annotationDirectory, calibrationAnnotation) -> None:
        # TODO: Get directory length
        self.calibration: int = None
        self.organs = {}
        annFiles = listdir(annotationDirectory)
        # TODO: ATLAS STORES CALIBRATION FACTORS
        # xOff, yOff, zOff, scale, layerDepth
        pass

    def constructAtlasFromList(self, fileList):
        numSlices = len(fileList)
        for file in fileList:
            annotation = json.load(open(file))
            fname = annotation["documents"][0]["name"]
            index = int(fname.split('.')[0][-1])
            for entity in annotation["annotation"]["annotationGroups"][0]["annotationEntities"]:
                name = entity["name"]
                try:
                    organ = self.organs[name]
                except(KeyError):
                    organ = Organ(name, numSlices)

    def calibrate(self, calibrationAnnotation, numSlices):
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


class Organ:
    def __init__(self, name, numSlices) -> None:
        self.name = name
        self.slices = [None] * numSlices
        self.voxelCloud: np.ndarray = None
        # self.voxelCloud = n x m x z matrix
    
    def appendOrganSlice(self, index, entity):
        pass

    def constructVoxelMap(self):
        pass