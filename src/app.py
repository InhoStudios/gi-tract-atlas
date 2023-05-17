from annotationprocessor import AtlasProcessor

from os.path import join
from os import listdir

import tkinter as tk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

atlas = AtlasProcessor()
ANNOTATIONS_FOLDER = ".\\assets\\annotations"
IMAGES_FOLDER = ".\\assets\\images"

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.initWindow()
        self.initAtlas()
        self.initCanvas()

    def initWindow(self):
        self.title("Rat GIT Processor")
        self.geometry("1280x720")
        self.minsize(1280, 720)

    def initCanvas(self):
        self.fig = Figure(figsize = (10, 7), dpi=100)
        self.atlas.setAnnotationFig(self.fig)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=15, padx=25)
    
    def initAtlas(self):
        self.atlas = AtlasProcessor()
        self.calibrate()
        self.initAtlasChecks()
    
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

    def calibrate(self):
        calibration = self.atlas.calibrate(join(ANNOTATIONS_FOLDER, "calibrate.json"), 27)
        print(calibration)
        for file in listdir(ANNOTATIONS_FOLDER):
            print(f"Processing {file}")
            try:
                self.atlas.addAnnotation(join(ANNOTATIONS_FOLDER, file))
            except:
                print(f"For {file}, error thrown")


if __name__=="__main__":
    app = App()
    app.mainloop()