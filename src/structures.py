import numpy as np

class Atlas:
    def __init__(self):
        self.organs = {}
        self.width = 0
        self.height = 0
        self.depth = 0

    def createOrgan(self, name):
        organ = Organ(name)
        self.organs[name] = organ
        return organ

    def centre(self):
        minX = 10000
        maxX = 0
        minY = 10000
        maxY = 0
        maxZ = 0
        for organ in self.organs:
            x, y, z = self.organs[organ].linearizeDims()
            minX = min(minX, min(x))
            maxX = max(maxX, max(x))
            minY = min(minY, min(y))
            maxY = max(maxY, max(y))
            maxZ = max(maxZ, max(z))
        meanX = (minX + maxX) / 2
        meanY = (minY + maxY) / 2
        print(minX, minY)
        for organ in self.organs:
            self.organs[organ].axes["x"] = \
                np.array(self.organs[organ].axes["x"]) - meanX
            self.organs[organ].axes["y"] = \
                np.array(self.organs[organ].axes["y"]) - meanY
        self.width = maxX - minX
        self.height = maxY - minY
        self.depth = maxZ
        return


class Organ:
    def __init__(self, name: str) -> None:
        self.name = name
        self.colour = 0xffffff
        self.axes = {"x":[], "y":[], "z":[]}
        # TODO: add self.mesh for 3D structures
    
    def addPoint(self, point: list) -> None:
        self.axes["x"].append(point[0])
        self.axes["y"].append(point[1])
        self.axes["z"].append(point[2])

    def linearizeDims(self):
        return self.axes["x"], self.axes["y"], self.axes["z"]