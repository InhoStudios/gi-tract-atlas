import json
from structures import Atlas
import matplotlib.pyplot as plt
import numpy as np

class AtlasProcessor:
    def __init__(self) -> None:
        self.atlas = Atlas()
    
    def addAnnotation(self, filepath):
        f = open(filepath)
        annotation = json.load(f)[0]

        fname = annotation["documents"][0]["name"]
        print(fname)

        # TODO: parse name to get depth
        # TEMP NAME PARSING
        z = int(fname.split('.')[0][-1]) * 50

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

    def viewAnnotation(self):
        ax = plt.axes(projection="3d")
        minX = np.inf
        maxX = 0
        minY = np.inf
        maxY = 0
        for organName in self.atlas.organs:
            organ = self.atlas.organs[organName]
            x, y, z = organ.linearizeDims()
            minX = min(minX, min(x))
            maxX = max(maxX, max(x))
            minY = min(minY, min(y))
            maxY = max(maxY, max(y))

            ax.scatter(x, y, z)
        ax.set_xlim(minX, maxX)
        ax.set_ylim(minY, maxY)
        ax.set_zlim(0, 1000)
        plt.show()
