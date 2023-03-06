# python -u trackandcount.py input.mp4 bg.png framenumber dist.csv [orifice_x orifice_y] overlay.png

import numpy as np
import math
import cv2 as cv
import sys
import csv

def calculate_distance(cx, cy, x, y): 
    return (math.sqrt( (cx-x)**2+(cy-y)**2 ))

framenum= int(sys.argv[3])
cap = cv.VideoCapture(sys.argv[1])
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
fps = cap.get(cv.CAP_PROP_FPS);
frame_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print("input video is: {}x{} @{} {}".format(width, height, fps,  frame_length) )    
# seek to frame
cap.set(cv.CAP_PROP_POS_FRAMES, float(framenum))

mask = np.zeros([height, width, 1], dtype=np.uint8)
mask= cv.bitwise_not(mask);
# buat LOKA: need some interactive way to define the mask's countour
contours = np.array([ [640,140], [315,220], [320, 300], [640, 230] ]) # 8879
cv.fillPoly(mask, pts =[contours], color=(0))
cue_prev= mask;

csvlog = open(sys.argv[4], 'a', newline='')
writer = csv.writer(csvlog)

ref_col= cv.imread(sys.argv[2])
ref_gray = cv.cvtColor(ref_col, cv.COLOR_BGR2GRAY)
ret, current_col = cap.read()
current_gray = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)
    
# all uget2
difference= cv.absdiff(current_gray, ref_gray)
ret,thresh = cv.threshold(difference,0,255,cv.THRESH_TRIANGLE);
cue = cv.bitwise_and(thresh, mask)
contours_cur,hierarchy = cv.findContours(cue, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

orifice_x= int(sys.argv[5])
orifice_y= int(sys.argv[6])

numlist= [framenum];
for i in range( len(contours_cur) ):
    #M= cv.moments(contours_cur[i])
    #if (M['m00']!=0):
    x1, y1, w1, h1 = cv.boundingRect(contours_cur[i])
    cx = x1 + w1/2
    cy = y1 + h1/2
    distance= calculate_distance(cx, cy, orifice_x, orifice_y)
    cv.fillPoly(current_col, pts=contours_cur[i], color=(0,255,0))
    numlist.append("{} {} {}".format(cx, cy, distance))
    
writer.writerow(numlist);
filename= str(framenum) + ".png"
print(filename)
cv.imwrite(filename, current_col);

cap.release
