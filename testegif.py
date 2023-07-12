# Putting a gif image on a canvas with Tkinter
# tested with Python24 by  vegaseat  25jun2005
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
from time import *
from configparser import ConfigParser
from datetime import datetime
import requests
# create the canvas, size in pixels
canvas = Canvas(width = 300, height = 200, bg = 'yellow')
# pack the canvas into a frame/form
canvas.pack(expand = YES, fill = BOTH)
# load the .gif image file
# put in your own gif file here, may need to add full path
# like 'C:/WINDOWS/Help/Tours/WindowsMediaPlayer/Img/mplogo.gif'
gif1 = PhotoImage(file = 'Gifs/animated/final/broken_clouds.gif')
# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
canvas.create_image(50, 10, image = gif1, anchor = NW)
# run it ...
mainloop()