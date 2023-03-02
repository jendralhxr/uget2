# python -u trackandcount.py input.mp4 bg.png 0 24000000000000 log.csv path.mp4 heatmap.mp4 startx starty

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

vid_uget = cv.VideoWriter(sys.argv[6],cv.VideoWriter_fourcc(*'mp4v'), 30.0, (640, 480))
#vid_heatmap = cv.VideoWriter(sys.argv[7],0, 60.0, (480, 640))

# buat LOKA: needs to define the starting point more aesthetically
TRACK_X= int(sys.argv[7]);
TRACK_Y= int(sys.argv[8]);
TRACK_HOP= 16;

# buat LOKA: pheromone trail and evaporation coefficients
COEF_EVAPORATE= 0.1
COEF_TRAIL= 0.02
COEF_SCALE= 1
COEF_PATH_FADE= 1

def calculate_contour_distance(contour1, contour2): 
    x1, y1, w1, h1 = cv.boundingRect(contour1)
    c_x1 = x1 + w1/2
    c_y1 = y1 + h1/2

    x2, y2, w2, h2 = cv.boundingRect(contour2)
    c_x2 = x2 + w2/2
    c_y2 = y2 + h2/2

    return max(abs(c_x1 - c_x2) - (w1 + w2)/2, abs(c_y1 - c_y2) - (h1 + h2)/2)

path = np.zeros([height, width, 3], dtype=np.uint8)
path1 = np.ones([height, width, 3], dtype=np.uint8)
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
    
    # all uget2
    difference= cv.absdiff(current_gray, ref_gray)
    ret,thresh = cv.threshold(difference,0,255,cv.THRESH_TRIANGLE);
    cue = cv.bitwise_and(thresh, mask)
    contours_cur,hierarchy = cv.findContours(cue, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if (framenum==startframe):
        contours_prev= contours_cur;
    
    for c in contours_cur:
        cv.fillPoly(cue, pts=c, color=(255))
    
    # tracking
    for i in range( len(contours_cur) ):
        cnt= contours_cur[i]
        M= cv.moments(cnt)
        if (M['m00']!=0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if (abs(cx-TRACK_X)<TRACK_HOP) and (abs(cy-TRACK_Y)<TRACK_HOP):
                cv.line(path, (TRACK_X,TRACK_Y), (cx, cy), (0,255,0), 1)
                cv.rectangle(path, (cx,cy), (cx+1, cy+1), (0,255,0), 2)
                TRACK_X= cx;
                TRACK_Y= cy;
                break;
    path= path - (COEF_PATH_FADE*path1).clip(None, path)
    
    
    # cellcount from countour
    print("{} {} {} {} {}".format(framenum, len(contours_cur), len(contours_prev), TRACK_X, TRACK_Y));
    # buat RINO: do we need stuff like speed to express motility?
    
    
    
    # heatmap
    #pheromone = np.add(pheromone, np.transpose(cue.astype(np.double)/255 * COEF_TRAIL))
    #pheromone = pheromone * (1-COEF_EVAPORATE)
    #heatmap= pheromone.astype(int)
    #heatmap = cv.applyColorMap(heatmap, cv.COLORMAP_JET)
    #heatmap = heatmap/255
        
    
    # ----------- results
    # CSV
    # numlist= [framenum, count, motility];
    # writer.writerow(numlist);
    
    # VIDEO 
    #render= cv.cvtColor(cue,cv.COLOR_GRAY2BGR)
    #render= cv.bitwise_or(render, path) 
    render= cv.bitwise_or(current_col, path)
    cv.rectangle(render, (TRACK_X,TRACK_Y), (TRACK_X+1, TRACK_Y+1), (0,0,255), 2)
    vid_uget.write(render)
    #render= cv.bitwise_or(render, pheromone_show)
    
    
    contours_prev= contours_cur;
    framenum += 1
    
    cv.imshow('all',render)
    k = cv.waitKey(1) & 0xFF
    if k== 27: # esc
       break

    # GRAPHS

cap.release
vid_uget.release
#vid_heatmap.release
