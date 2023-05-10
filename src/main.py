from annotationprocessor import ImageAnnotationProcessor

from os.path import join

annotationProcessor = ImageAnnotationProcessor()
ANNOTATIONS_FOLDER = "../assets/annotations"
IMAGES_FOLDER = "../assets/images"

if __name__=="__main__":
    annotationProcessor.addAnnotation(join(ANNOTATIONS_FOLDER, "annotation1.json"))