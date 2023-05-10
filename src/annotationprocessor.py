import json

class ImageAnnotationProcessor:
    def __init__(self) -> None:
        pass
    
    def addAnnotation(self, filepath):
        f = open(filepath)
        json.load(f)
        f.close()
