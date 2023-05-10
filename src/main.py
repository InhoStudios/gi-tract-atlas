from annotationprocessor import AtlasProcessor

from os.path import join

atlas = AtlasProcessor()
ANNOTATIONS_FOLDER = ".\\assets\\annotations"
IMAGES_FOLDER = ".\\assets\\images"

if __name__=="__main__":
    atlas.addAnnotation(join(ANNOTATIONS_FOLDER, "annotation1.json"))