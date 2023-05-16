from annotationprocessor import AtlasProcessor

from os.path import join
from os import listdir

atlas = AtlasProcessor()
ANNOTATIONS_FOLDER = ".\\assets\\annotations"
IMAGES_FOLDER = ".\\assets\\images"

if __name__=="__main__":
    calibration = atlas.calibrate(join(ANNOTATIONS_FOLDER, "calibrate.json"), 27)
    print(calibration)
    for file in listdir(ANNOTATIONS_FOLDER):
        print(f"Processing {file}")
        try:
            atlas.addAnnotation(join(ANNOTATIONS_FOLDER, file))
        except:
            print(f"For {file}, error thrown")
    atlas.viewAnnotation()