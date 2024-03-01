# python -u trackandcount.py input.mp4 0 24000000000000 log.csv cue.mp4 heatmap.mp4

import numpy as np
import math
import cv2 as cv
import sys
import csv
import random

# heatmap
COEF_FADE_IN = 1.2
COEF_FADE_OUT = 0.4
# buat LOKA: any way to set these values more gracefully? like a slider?

threshold_value = 10 # good place to start
space= 4 # most probable uget2 uget2 size


framenum = 0
window_name = "uget2"
cv.namedWindow(window_name)

cap = cv.VideoCapture(sys.argv[1])
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
fps = cap.get(cv.CAP_PROP_FPS);
frame_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print("input video is: {}x{} @{} {}".format(width, height, fps, frame_length))

startframe = int(sys.argv[2])
cap.set(cv.CAP_PROP_POS_FRAMES, float(startframe))
framenum = startframe;
lastframe = int(sys.argv[3])

csvlog = open(sys.argv[4], 'w', newline='')
writer = csv.writer(csvlog)
# buat RINO: need to define the columns
header = ['framenum', 'count', 'motility']
writer.writerow(header);

vid_cue = cv.VideoWriter(sys.argv[5], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_heat = cv.VideoWriter(sys.argv[6], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))

heatmap = np.zeros([height, width], dtype=np.uint8)
mask = np.full([height, width], 255, dtype=np.uint8)
mask_col = np.full([height, width, 3], (255,255,255), dtype=np.uint8)

#------ setting the capilary mask
key=2;
color= (0,0,0)
mask_points=[]

def mouse_callback(event, x, y, flags, param):
    global mask_col, color
    if event == cv.EVENT_LBUTTONDOWN:
        mask_points.append((x, y))
        #print(f"Clicked at position: ({x}, {y})")
        cv.circle(mask_col, (x,y), 4, (0,200,0), -1)

    if len(mask_points) > 2:
        mask_contour= np.array(mask_points)
        cv.fillPoly(mask_col, pts=[mask_contour], color=(0,0,0))
        cv.fillPoly(mask, pts=[mask_contour], color=(0))

cv.setMouseCallback(window_name, mouse_callback)

ret, current_col = cap.read()
ref= cv.cvtColor(current_col, cv.COLOR_BGR2GRAY) 

# drawing the mask
while (key != ord('s')):
    # draw over mask_col with the dots
    cv.imshow(window_name, cv.bitwise_and(current_col, mask_col))
    key = cv.waitKey(1) & 0xff
    if key==27: # bail out
        quit()
    elif key==ord('c'): # clear masks
        mask_points=[]
        break
    elif key==ord('s'): # start analysis
        cv.destroyAllWindows()    
        break
        

# --- main routine
while (framenum < lastframe) and (framenum < frame_length - 1):
    ret, current_col = cap.read()
    current = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)
    cue = cv.bitwise_and(current, mask)

    # keep the ref (reference background) the brightest
    # also apply the mask for the capilary pipe
    for j in range(height):
        for i in range(width):
            if current.item(j,i) > ref.item(j,i):
                ref.itemset((j,i), current.item(j,i))
    ref = cv.bitwise_and(ref, mask)
    
    # uget2 detection: background substraction and thresholding
    cue = cv.absdiff(current, ref)
    #ret, cue_tri = cv.threshold(cue, 0, 250, cv.THRESH_TRIANGLE);
    ret, cue_raw= cv.threshold(cue,threshold_value,250,cv.THRESH_BINARY)
    cue_raw = cv.bitwise_and(cue_raw, mask)
    #cue_mean = cv.adaptiveThreshold(cue,250,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,2)
    #cue_gauss = cv.adaptiveThreshold(cue,250,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
    
    # uget2 counting with countours
    render = cv.cvtColor(cue_raw, cv.COLOR_GRAY2BGR)
    render = current_col
    contours, hierarchy = cv.findContours(cue_raw, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
	#contours, hierarchy = cv.findContours(cue, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    for c in contours:
        cv.fillPoly(render, pts=c, color=(0,255,0))
    cv.imshow("deteksi", render)
    print(f'{framenum}: {len(contours)} cells')
    
    framenum= framenum+1
    key = cv.waitKey(1) & 0xff
    if key==27:
        quit()
    if key==ord('s'):
        print("save {}".format(framenum))
        cv.imwrite("cue"+str(framenum)+".png", cue)
        cv.imwrite("det"+str(framenum)+".png", cue_raw)
        cv.imwrite("ref"+str(framenum)+".png", ref)
    if key==ord('a'):
        threshold_value = threshold_value -1
        print("threshold: "+str(threshold_value))
    if key==ord('d'):
        threshold_value = threshold_value +1
        print("threshold: "+str(threshold_value))

cv.imwrite('reffinal.png', ref)
cap.release
vid_cue.release
vid_heat.release
