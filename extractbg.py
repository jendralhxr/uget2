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

# need interactive way to define the mask's countour
#contours = np.array([ [0,510], [0,790], [4096, 790], [4096, 510] ])
#cv.fillPoly(mask, pts =[contours], color=(0))

while (framenum<lastframe) and (framenum<frame_length-1):
    ret, current_col = cap.read()
    current_gray = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)
    if (framenum==startframe):
        bg_col= current_col;
        bg_gray= current_gray;
    
    framenum += 1
    #print(framenum)
    
    # need faster pixel access for this
    for j in range(height):
        for i in range(width):
            if (current_gray.item(j, i) > bg_gray.item(j, i)):
                bg_gray.itemset((j,i), current_gray.item(j,i));
                bg_col.itemset((j,i,0), current_col.item(j,i,0));
                bg_col.itemset((j,i,1), current_col.item(j,i,1));
                bg_col.itemset((j,i,2), current_col.item(j,i,2));
    
    # cv.imshow('background',bg_col)
    # cv.imshow('current',current_col)
    # k = cv.waitKey(1) & 0xFF
    # if k== 27: # esc
        # break
   
cv.imwrite(sys.argv[4], bg_col)
cap.release
