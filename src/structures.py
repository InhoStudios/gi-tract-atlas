class Atlas:
    def __init__(self):
        self.organs = {}

    def createOrgan(self, name):
        organ = Organ(name)
        self.organs[name] = organ


class Organ:
    def __init__(self, name):
        self.name = name
        self.pointCloud = []
        self.colour = 0xffffff
        # TODO: add self.mesh for 3D structures