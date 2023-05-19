import json

from structures import Atlas

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk

class AtlasProcessor:
    def __init__(self) -> None:
        self.atlas = Atlas()
        self.calibration: int = None
        self.calibrationFile = ""
        self.shownOrgans = []
        self.scale = 1.0
        self.offsetX = 0
        self.offsetY = 0
        self.offsetZ = 0
        # self.root = Tk()
        # self.frame = ttk.Frame(self.root, padding=10)
        # self.frame.grid()
        # ttk.Button(self.frame, text="Quit", command=self.root.destroy).grid(column=1, row=0)
        # self.root.mainloop()
    
    def addAnnotation(self, filepath):
        if (self.calibration == None):
            print("Calibration not set yet. Please update calibration before adding annotations")
            return
        if (filepath == self.calibrationFile):
            print("Calibration file. Skipping...")
            return
        f = open(filepath)
        annotation = json.load(f)[0]

        fname = annotation["documents"][0]["name"]
        print(fname)

        # TODO: parse name to get depth
        # TEMP NAME PARSING
        z = int(fname.split('.')[0][-1]) * self.calibration

        for entity in annotation["annotation"]["annotationGroups"][0]["annotationEntities"]:
            eName = entity["name"]
            try:
                organ = self.atlas.organs[eName]
            except(KeyError):
                organ = self.atlas.createOrgan(eName)
            for point in entity["annotationBlocks"][0]["annotations"][0]["segments"][0]:
                point.append(z)
                organ.addPoint(point)
        f.close()
        self.shownOrgans = list(self.getCategories())
        return
    
    def calibrate(self, calibrationAnnotation, numZslices):
        f = open(calibrationAnnotation)
        annotation = json.load(f)[0]
        body = annotation["annotation"]["annotationGroups"][0]["annotationEntities"][0]
        zvals = []
        for point in body["annotationBlocks"][0]["annotations"][0]["segments"][0]:
            zvals.append(point[1])
        minZ = min(zvals)
        maxZ = max(zvals)
        diff = maxZ - minZ + 150
        self.calibration = diff / numZslices
        self.calibrationFile = calibrationAnnotation
        return self.calibration

    def viewAnnotation(self):
        self.setAnnotationFig(plt)
        plt.show()

    def tweakCoords(self, x, y, z):
        return x, z, -y
    
    def adjustScale(self, scale, ax):
        self.scale = scale
        self.refreshFig(ax)
    
    def refreshFig(self, ax):
        for organName in self.shownOrgans:
            organ = self.atlas.organs[organName]
            x, y, z = organ.linearizeDims()
            x, y, z = self.tweakCoords(x, y, z)
            x = np.array(x) * self.scale
            y = np.array(y) * self.scale
            z = np.array(z) * self.scale
            x = x + self.offsetX
            y = y + self.offsetY
            z = z + self.offsetZ
            ax.scatter(x, y, z, label=organName)
        ax.legend()

    

    def setAnnotationFig(self, ax):
        minX = 10000
        maxX = 0
        minY = 10000
        maxY = 0
        for organName in self.shownOrgans:
            organ = self.atlas.organs[organName]
            x, y, z = organ.linearizeDims()
            x, y, z = self.tweakCoords(x, y, z)
            minX = min(minX, min(x))
            maxX = max(maxX, max(x))
            minY = min(minY, min(y))
            maxY = max(maxY, max(y))

            ax.scatter(x, y, z, label=organName)
        minDim = min(minX, minY)
        maxDim = max(maxX, maxY)
        ax.set_xlim(minDim, maxDim)
        ax.set_ylim(minDim, maxDim)
        ax.set_zlim(0, maxDim - minDim)
        ax.legend()
    
    def toggleCategory(self, name):
        if name in self.shownOrgans:
            self.shownOrgans.remove(name)
        else:
            self.shownOrgans.append(name)
    
    def getCategories(self):
        return self.atlas.organs.keys()
        
    def centreAtlas(self):
        return self.atlas.centre()
