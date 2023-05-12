class Atlas:
    def __init__(self):
        self.organs = {}

    def createOrgan(self, name):
        organ = Organ(name)
        self.organs[name] = organ
        return organ


class Organ:
    def __init__(self, name: str):
        self.name = name
        self.pointCloud = []
        self.colour = 0xffffff
        # TODO: add self.mesh for 3D structures
    
    def addPoint(self, point: list):
        self.pointCloud.append(point)

    def linearizeDims(self):
        x = []
        y = []
        z = []
        for point in self.pointCloud:
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        return x, y, z