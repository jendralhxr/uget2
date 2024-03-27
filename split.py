# python -u extractbg.py input.mp4 0 8000 output.png

import numpy as np
import math
import cv2 as cv
import sys

framenum= 0

cap = cv.VideoCapture(sys.argv[1])
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
fps = cap.get(cv.CAP_PROP_FPS);
frame_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print("video is: {}x{} @{} {}".format(width, height, fps,  frame_length) )

startframe= int(sys.argv[2])
cap.set(cv.CAP_PROP_POS_FRAMES, float(startframe))
framenum= startframe;
lastframe= int(sys.argv[3])

vid_r = cv.VideoWriter(sys.argv[4], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_g = cv.VideoWriter(sys.argv[5], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_b = cv.VideoWriter(sys.argv[6], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_rx = cv.VideoWriter(sys.argv[7], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_gx = cv.VideoWriter(sys.argv[8], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_bx = cv.VideoWriter(sys.argv[9], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_gray = cv.VideoWriter(sys.argv[10], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))

while (framenum<lastframe) and (framenum<frame_length-1):
    ret, cue = cap.read()
    vid_gray.write(cv.cvtColor(cue, cv.COLOR_BGR2GRAY))
    framenum += 1
    print(framenum)
   
    r= cue.copy();
    r[:,:,0]= 0 
    r[:,:,1]= 0 
    vid_r.write(r)
    g= cue.copy();
    g[:,:,0]= 0 
    g[:,:,2]= 0 
    vid_g.write(g)
    b= cue.copy();
    b[:,:,2]= 0 
    b[:,:,1]= 0 
    vid_b.write(b)
    
    vid_bx.write(cv.cvtColor(cue[:,:,0], cv.COLOR_GRAY2BGR))
    vid_gx.write(cv.cvtColor(cue[:,:,1], cv.COLOR_GRAY2BGR))
    vid_rx.write(cv.cvtColor(cue[:,:,2], cv.COLOR_GRAY2BGR))
 
cap.release
