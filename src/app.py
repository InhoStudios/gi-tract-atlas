from annotationprocessor import AtlasProcessor
from niftiprocessor import NIFTIManager

from os.path import join
from os import listdir

import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
import cv2

atlas = AtlasProcessor()
ANNOTATIONS_FOLDER = ".\\assets\\annotations"
IMAGES_FOLDER = ".\\assets\\images\\sample"

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.initWindow()
        self.initAtlas()
        self.initNIFTI()
        self.initCanvas()
        self.initUI()
        self.offsetX = 0
        self.offsetY = 0
        self.offsetZ = 0

    def initWindow(self):
        self.title("Rat GIT Processor")
        self.geometry("1920x1080")
        self.minsize(1920, 1080)

    def initCanvas(self):
        self.fig = Figure(figsize = (15, 10), dpi=100)
        self.ax = self.fig.add_subplot(projection="3d")
        self.atlas.setAnnotationFig(self.ax)
        self.nifti.setAnnotationFig(self.ax)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=15, padx=25)
    
    def initAtlas(self):
        self.atlas = AtlasProcessor()
        self.calibrateAtlas()
        self.initSliders()
    
    def initSliders(self):
        scale = tk.IntVar()
        def update(evt):
            x = (xOffset.get() - 50) * 6
            y = (yOffset.get() - 50) * 6
            z = (zOffset.get() - 50) * 6
            sf = scale.get() / 100.0
            self.fig.clf()
            self.ax = self.fig.add_subplot(projection="3d")
            self.nifti.setAnnotationFig(self.ax)
            self.atlas.offsetX = x
            self.atlas.offsetY = y
            self.atlas.offsetZ = z
            self.atlas.scale = sf
            print(x, y, z, sf)
            self.atlas.refreshFig(self.ax)
            self.canvas.draw()

            
        scaleSlider = Scale(self, 
                            variable=scale,
                            from_=0, 
                            to=100, 
                            length=200,
                            orient=HORIZONTAL)
        scaleSlider.set(30)
        scaleSlider.bind("<ButtonRelease-1>", update)
        scaleSlider.grid(row=0, column=1)
        xOffset = tk.IntVar()
        yOffset = tk.IntVar()
        zOffset = tk.IntVar()
        xSlider = Scale(self,
                        variable=xOffset,
                        from_=0,
                        to=100,
                        length=200,
                        orient=HORIZONTAL)
        xSlider.set(67)
        xSlider.grid(row=1, column=1)
        xSlider.bind("<ButtonRelease-1>", update)
        ySlider = Scale(self,
                        variable=yOffset,
                        from_=0,
                        to=100,
                        length=200,
                        orient=HORIZONTAL)
        ySlider.set(71)
        ySlider.grid(row=2, column=1)
        ySlider.bind("<ButtonRelease-1>", update)
        zSlider = Scale(self,
                        variable=zOffset,
                        from_=0,
                        to=100,
                        length=200,
                        orient=HORIZONTAL)
        zSlider.set(89)
        zSlider.grid(row=3, column=1)
        zSlider.bind("<ButtonRelease-1>", update)
        calBtn = Button(self, text="Calibrate")
        calBtn.bind("<ButtonRelease-1>", update)
        calBtn.grid(row=4, column=1)
    
    def initUI(self):
        sliceBtn = Button(self, text="Slice")
        sliceBtn.grid(row=5, column=1)
        pass

    def initAtlasChecks(self):
        vars = {}
        def toggle():
            print(vars)
            self.atlas.toggleCategory(vars[key].get())
            self.fig.clf()
            self.atlas.setAnnotationFig(self.fig)
            self.canvas.draw()
        for i, key in enumerate(self.atlas.getCategories()):
            vars[key] = tk.StringVar()
            check = Checkbutton(self, text=key, variable=vars[key], onvalue=key, offvalue="", command=toggle)
            check.select()
            check.grid(row=i, column=1)

    def calibrateAtlas(self):
        calibration = self.atlas.calibrate(join(ANNOTATIONS_FOLDER, "calibrate.json"), 27)
        print(calibration)
        for file in listdir(ANNOTATIONS_FOLDER):
            print(f"Processing {file}")
            try:
                self.atlas.addAnnotation(join(ANNOTATIONS_FOLDER, file))
            except:
                print(f"For {file}, error thrown")
        self.atlas.centreAtlas()
    
    def initNIFTI(self):
        self.nifti = NIFTIManager()
        CT_path = ".\\assets\\images\\sample\\CT_TS_HEUHR_In111_free_M1039_0h_220721-selfcal.nii"
        SPECT_path = ".\\assets\\images\\sample\\SPECT_REG_TS_HEUHR_In111_free_M1039_0h_220721_171kev_04vox_16ss_6it_dc-ac.nii"
        self.nifti.importImage(CT_path, "CT", 250, 1200)
        self.nifti.importImage(SPECT_path, "SPECT", 50, 0.02)

if __name__=="__main__":
    # app = App()
    # app.mainloop()
    # tk = Tk()
    # tk.title("Image Slices")
    # tk.geometry("1920x1080")
    atlas.calibrate(join(ANNOTATIONS_FOLDER, "calibrate.json"), 27)
    for file in listdir(ANNOTATIONS_FOLDER):
        print(f"Processing {file}")
        try:
            atlas.addAnnotation(join(ANNOTATIONS_FOLDER, file))
        except:
            print(f"For {file}, error thrown")
    # atlas.centreAtlas()
    imgs = []

    figure = Figure(figsize = (15, 10), dpi=100)
    structure = "Stomach"
    organ = atlas.atlas.organs[structure]
    for level in set(organ.axes["z"]):
        indices = np.where(np.array(organ.axes["z"]).astype(int) == int(level))
        img = np.zeros((1600, 2560))
        points = np.array(tuple([x, y] for x, y, 
                       in zip(
                           np.array(organ.axes["x"])[indices], 
                           np.array(organ.axes["y"])[indices]))).astype(int)
        print(level)
        cv2.fillPoly(img, pts=[points], color=(1))
        plt.imshow(img)
        plt.show()


    # tk.mainloop()