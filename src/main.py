from annotationprocessor import AtlasProcessor

from os.path import join
from os import listdir

atlas = AtlasProcessor()
ANNOTATIONS_FOLDER = ".\\assets\\annotations"
IMAGES_FOLDER = ".\\assets\\images"

if __name__=="__main__":
    for file in listdir(ANNOTATIONS_FOLDER):
        atlas.addAnnotation(join(ANNOTATIONS_FOLDER, file))
    atlas.viewAnnotation()