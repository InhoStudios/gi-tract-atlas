from os.path import join
from os import listdir

import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
import json
import cv2

ANNOTATIONS_FOLDER = ".\\assets\\annotations"

body = {}

def loadImages():
    for file in listdir(ANNOTATIONS_FOLDER):
        try:
            loadImage(join(ANNOTATIONS_FOLDER, file))
        except:
            print(f"Skipping {file}")

def loadImage(path):
    f = open(path)
    annotation = json.load(f)[0]
    for entity in annotation["annotation"]["annotationGroups"][0]["annotationEntities"]:
        eName = entity["name"]
        try:
            body[eName]
        except:
            body[eName] = []
        points = []
        for point in entity["annotationBlocks"][0]["annotations"][0]["segments"][0]:
            points.append(point)
        img = np.zeros((2560, 2560))
        points = np.array(points).astype(int)
        cv2.fillPoly(img, pts=[points], color=(255, 255, 255))
        body[eName].append(img)

if __name__=="__main__":
    loadImages()
    organ = body["Jejunum"]
    precision = 1000

    window = Tk()
    window.title("Image Slices")
    window.geometry("1920x1080")

    slice = tk.IntVar()
    interpolate = Scale(window, variable=slice, from_=0, to=precision, length=800)

    fig = Figure(figsize=(16, 10), dpi=100)
    ax = fig.add_subplot()
    canvas = FigureCanvasTkAgg(fig, master=window)

    def update(evt):
        input = slice.get()

        numImg = len(organ) - 1
        imgDepth = float(precision)/numImg
        index = input / imgDepth
        
        ind0 = int(np.floor(index))
        ind1 = int(np.ceil(index))
        img0 = organ[ind0]
        img1 = organ[ind1]

        alpha = (input % int(imgDepth)) / imgDepth

        additiveImage = np.add(img0 * alpha, img1 * (1.0 - alpha)) / 2
        binaryImg = np.zeros(additiveImage.shape)
        binaryImg[np.where(additiveImage > 0.5)] = 1

        fig.clf()
        ax = fig.add_subplot()
        ax.imshow(binaryImg)
        canvas.draw()

        

    ax.imshow(organ[0])
    canvas.draw()
    
    canvas.get_tk_widget().grid(row=0, column=0, padx=25)
    interpolate.bind("<ButtonRelease-1>", update)
    interpolate.grid(row=0, column=1)

    window.mainloop()

