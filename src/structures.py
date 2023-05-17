class Atlas:
    def __init__(self):
        self.organs = {}

    def createOrgan(self, name):
        organ = Organ(name)
        self.organs[name] = organ
        return organ


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