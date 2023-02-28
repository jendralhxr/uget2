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

# buat LOKA: needs to define the starting point more aesthetically
TRACK_X= 100;
TRACK_Y= 300;

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
contours = np.array([ [640,150], [400,200], [380, 290], [640, 235] ]) # 8879
cv.fillPoly(mask, pts =[contours], color=(0))
cue_prev= mask;

#--- main routine
while (framenum<lastframe) and (framenum<frame_length-1):
    ret, current_col = cap.read()
    current_gray = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)
    
    #print(ref.shape)
    
    # all uget2
    difference= cv.absdiff(current_gray, ref_gray)
    ret,thresh = cv.threshold(difference,0,255,cv.THRESH_TRIANGLE);
    cue = cv.bitwise_and(thresh, mask)
    contours_cur,hierarchy = cv.findContours(cue, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    for c in contours_cur:
        cv.fillPoly(cue, pts=c, color=(255))
    
    # mask out still uget2
    # for LOKA: is there any way to do such search faster?
    # tee= cue.copy();
    # if (framenum== startframe):
        # contours_prev= contours_cur;
    # still_uget=0;
    # for i in range( len(contours_cur) ):
        # for j in range (len(contours_prev) ):
            # distance= calculate_contour_distance(contours_cur[i], contours_prev[j])
            # if (distance<1.0):
                # cv.fillPoly(tee, pts=contours_cur[i], color=(0))
                # still_uget += 1;
    
    # motile uget2, selective tracking
    #contours_motile,hierarchy = cv.findContours(tee, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    
    contours_motile= contours_cur
    min_distance= 40;
    #min_idx= 0;
    for i in range( len(contours_motile) ):
        x,y,w,h = cv.boundingRect(contours_motile[i])
        distance= math.sqrt( pow((x-TRACK_X),2) + pow((y-TRACK_Y),2) );
        if (distance<min_distance):
            min_distance= distance;
            min_idx= i;
            xmin= x;
            ymin= y;
    if (min_idx!=0):
        cv.rectangle(path, (xmin,ymin), (xmin+1, ymin+1), (0,255,0), 1)
        TRACK_X= x;
        TRACK_Y= y;
        
    # cellcount from countour
    print("{} {} {} {}".format(framenum, len(contours_cur), len(contours_motile), min_distance));
    # buat RINO: do we need stuff like speed to express motility?
    
    
        
    # heatmap
    
    
    
    
    # ----------- results
    # CSV
    # numlist= [framenum, count, motility];
    # writer.writerow(numlist);
    
    # VIDEO 
    #render= cv.cvtColor(cue,cv.COLOR_GRAY2RGB)
    #render= = cv.bitwise_and(render, path) 
    #vid_uget.write(render)
    
    #overlay= = cv.bitwise_and(current_col, path) 
    #overlay= cv.cvtColor(tee,cv.COLOR_GRAY2RGB)
    #vid_path.write(overlay)
    
    contours_prev= contours_cur;
    framenum += 1
    
    cv.imshow('all',cue)
    cv.imshow('motile',path)
    
    k = cv.waitKey(1) & 0xFF
    if k== 27: # esc
       break

    # GRAPHS

cap.release
vid_uget.release
vid_path.release 
vid_heatmap.release
