from niftiprocessor import NIFTIManager
import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
import json
import cv2


nifti = NIFTIManager()

if __name__ == "__main__":
    CT_path = ".\\assets\\images\\sample\\CT_TS_HEUHR_In111_free_M1039_0h_220721-selfcal.nii"
    SPECT_path = ".\\assets\\images\\sample\\SPECT_REG_TS_HEUHR_In111_free_M1039_0h_220721_171kev_04vox_16ss_6it_dc-ac.nii"
    nifti.importImage(CT_path, "CT", 250, 1200)
    nifti.importImage(SPECT_path, "SPECT", 50, 0.02)
    
    
    window = Tk()