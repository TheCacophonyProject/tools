#!/usr/bin/python

"""
Tool to combine two videos at a different frame rate.
Frame rate can be read from video file but also might need to be hard coded.
Only support 480, 640 video at the moment.
Can delay when ir or cptv video starts.
"""

# TODO Add support for different height videos

import numpy as np
import cv2

## ======= SETTINGS =========
ir_offset = 0  # Delay for starting IR video in seconds
cptv_offset = 0  # Delay for starting cptv video in seconds
ir_file = "ir.mp4"
cptv_file = "cptv.mp4"

## ==========================

ir = cv2.VideoCapture(ir_file) 
ir_fps = ir.get(cv2.CAP_PROP_FPS)
ir_fps = 10 # Hard coded because it's not what it thinks it is..
print(F"ir fps: {ir_fps}")

cptv = cv2.VideoCapture(cptv_file)
cptv_fps = cptv.get(cv2.CAP_PROP_FPS)
print(F"cptv fps: {cptv_fps}")

ir_frames = []
cptv_frames = []
cptv_count = 0

s = (480, 640, 3)
cptv_frame = np.zeros(s, np.uint8)
ir_frame = np.zeros(s, np.uint8)
ir_rec = False
cptv_rec = False
frame_count = 0
while(True):
    if not frame_count/ir_fps <= ir_offset:
        ir_rec = True
        ret, ir_frame = ir.read()
        if not ret:
            break
    
    if frame_count/ir_fps >= cptv_count/cptv_fps+cptv_offset:
        cptv_rec = True
        cptv_count+=1
        ret, cptv_frame = cptv.read()
        if not ret:
            break
    frame_count+=1
    if cptv_rec and ir_rec:
        ir_frames.append(ir_frame)
        cptv_frames.append(cptv_frame)


height, width, channels = np.concatenate((ir_frames[0], cptv_frames[0]), axis=1).shape
size = (width, height)
print(size)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter("out.mp4", fourcc, ir_fps, size)

for i in range(len(cptv_frames)):
    both = np.concatenate((ir_frames[i], cptv_frames[i]), axis=1)
    a = writer.write(both)
writer.release()

# TODO Have time offset for videos