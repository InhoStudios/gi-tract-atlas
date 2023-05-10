import json
from structures import Atlas

class AtlasProcessor:
    def __init__(self) -> None:
        self.atlas = Atlas()
    
    def addAnnotation(self, filepath):
        f = open(filepath)
        annotation = json.load(f)[0]

        fname = annotation["documents"][0]["name"]
        print(fname)

        # parse name to get depth
        # 
        f.close()

    def viewAnnotation(self):
        pass
