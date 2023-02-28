# python -u trackandcount.py input.mp4 bg.png 0 24000000000000 log.csv uget.mp4 path.mp4 heatmap.mp4

import numpy as np
import math
import cv2 as cv
import sys
import csv

framenum= 0

cap = cv.VideoCapture(sys.argv[1])
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
fps = cap.get(cv.CAP_PROP_FPS);
frame_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print("video is: {}x{} @{} {}".format(width, height, fps,  frame_length) )    

ref_col= cv.imread(sys.argv[2])
ref_gray = cv.cvtColor(ref_col, cv.COLOR_BGR2GRAY)

startframe= int(sys.argv[3])
cap.set(cv.CAP_PROP_POS_FRAMES, float(startframe))
framenum= startframe;
lastframe= int(sys.argv[4])

csvlog = open(sys.argv[5], 'w', newline='')
writer = csv.writer(csvlog)
# buat RINO: need to define the columns
header= ['framenum','count','motility']
writer.writerow(header);

vid_uget = cv.VideoWriter(sys.argv[6],cv.VideoWriter_fourcc(*'mp4v'), fps, [height, width])
vid_path = cv.VideoWriter(sys.argv[6],cv.VideoWriter_fourcc(*'mp4v'), fps, [height, width])
vid_heatmap = cv.VideoWriter(sys.argv[7],cv.VideoWriter_fourcc(*'mp4v'), fps, [height, width])

#print(vidout.frameSize)


def calculate_contour_distance(contour1, contour2): 
    x1, y1, w1, h1 = cv.boundingRect(contour1)
    c_x1 = x1 + w1/2
    c_y1 = y1 + h1/2

    x2, y2, w2, h2 = cv.boundingRect(contour2)
    c_x2 = x2 + w2/2
    c_y2 = y2 + h2/2

    return max(abs(c_x1 - c_x2) - (w1 + w2)/2, abs(c_y1 - c_y2) - (h1 + h2)/2)

path = np.zeros([height, width, 3], dtype=np.uint8)
pheromone = np.zeros([height, width, 1], dtype=np.double)

mask = np.zeros([height, width, 1], dtype=np.uint8)
mask= cv.bitwise_not(mask);
# buat LOKA: need some interactive way to define the mask's countour
#contours = np.array([ [300,200], [300,240], [640, 240], [640, 200] ])
#cv.fillPoly(mask, pts =[contours], color=(0))


#--- main routine
while (framenum<lastframe) and (framenum<frame_length-1):
    ret, current_col = cap.read()
    current_gray = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)
    
    framenum += 1
    #print(ref.shape)
    
    difference= cv.absdiff(current_gray, ref_gray)
    ret,thresh = cv.threshold(difference,0,255,cv.THRESH_TRIANGLE);
    cue = cv.bitwise_and(thresh, mask)
    contours,hierarchy = cv.findContours(cue, cv.RETR_LIST, cv.CHAIN_APPROX_TC89_L1)
    
    total_x= 0
    total_y= 0
    total_m= 0
    
    for c in contours:
        cv.fillPoly(cue, pts=c, color=(255))
    
    # cellcount from countour
    print(len(contours))
    
    # motility from correlation
    
    
    # selective tracking
    
        
    # heatmap
    
    
    
    
    # ----------- results
    # CSV
    # numlist= [framenum, count, motility];
    # writer.writerow(numlist);
    
    # VIDEO
    # render= cv.cvtColor(cue,cv.COLOR_GRAY2RGB)
    # render= = cv.bitwise_and(render, path) 
    # vid_uget.write(render)
    
    # overlay= = cv.bitwise_and(current_col, path) 
    # vid_path.write(overlay)
    
    
    
    cv.imshow('display',cue)
    k = cv.waitKey(1) & 0xFF
    if k== 27: # esc
       break

    # GRAPHS

cap.release
vid_path.release 
vid_heatmap.release
