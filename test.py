import json
from flask import Flask
from flask_cors import CORS
from flask import request

from PIL import Image
import numpy as np
import cv2

import multiprocessing
import pickle
from time import time
import os
import potrace

def get_contours(filename = None, image = None, nudge = .33):
    if type(image) == type(None):
        image = cv2.imread(filename)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    median = max(10, min(245, np.median(gray)))
    lower = int(max(0, (1 - nudge) * median))
    upper = int(min(255, (1 + nudge) * median))
    filtered = cv2.bilateralFilter(gray, 5, 50, 50)
    edged = cv2.Canny(filtered, lower, upper, L2gradient = True)

    return edged

def get_trace(data):
    for i in range(len(data)):
        data[i][data[i] > 1] = 1
    bmp = potrace.Bitmap(data)
    path = bmp.trace(2, potrace.TURNPOLICY_MINORITY, 1.0, 1, .5)
    return path

import cv2
video = cv2.VideoCapture("data/walking.mp4")
ret, test_frame = video.read()

with open("demo.txt", "w") as fh: # Clear previous file
    pass
frame = 0 
frames2skip = 10 

with open("demofile3.txt", "w") as fh:
    while ret:
        path = get_trace(get_contours(image = test_frame))

        for curve in path.curves:
            segments = curve.segments
            start = curve.start_point
            fh.write(f"{start}\n")
            for segment in segments:
                if not segment.is_corner:
                    fh.write(f"{segment.c1} {segment.c2} {segment.end_point}\n")
        
            fh.write(f"#\n")
        [video.read() for _ in range(frames2skip)]
        ret, test_frame = video.read()

#print(get_latex("../Images/box.jpg"))

## Get a list of points distributed along the curve.
#points_on_curve = geometry.interpolate_bezier(
#    bez_points[0].co,
#    bez_points[0].handle_right,
#    bez_points[1].handle_left,
#    bez_points[1].co,
#    16)

def test():
    controls = [[(0,0),(2.5,7.5),(5,5),(1,1)]]
    pass
test()

## Create cubes.
#cube_rad = 0.5 / count
#for point in points_on_curve:
#    ops.mesh.primitive_cube_add(size=cube_rad, location=point)
#    cube = context.active_object
#    cube.parent = group