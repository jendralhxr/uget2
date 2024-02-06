# python -u trackandcount.py input.mp4 bg.png 0 24000000000000 log.csv cue.mp4 output.mp4 heatmap.mp4

import numpy as np
import math
import cv2 as cv
import sys
import csv
import random

window_name = "uget2 mari berkipet"
cv.namedWindow(window_name)

# heatmap
COEF_FADE_IN = 1.2
COEF_FADE_OUT = 0.3

# buat LOKA: any way to set these values more gracefully?

framenum = 0

cap = cv.VideoCapture(sys.argv[1])
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
fps = cap.get(cv.CAP_PROP_FPS);
frame_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print("input video is: {}x{} @{} {}".format(width, height, fps, frame_length))

ref_col = cv.imread(sys.argv[2])
ref_gray = cv.cvtColor(ref_col, cv.COLOR_BGR2GRAY)

startframe = int(sys.argv[3])
cap.set(cv.CAP_PROP_POS_FRAMES, float(startframe))
framenum = startframe;
lastframe = int(sys.argv[4])

csvlog = open(sys.argv[5], 'w', newline='')
writer = csv.writer(csvlog)
# buat RINO: need to define the columns
header = ['framenum', 'count', 'motility']
writer.writerow(header);

vid_cue = cv.VideoWriter(sys.argv[6], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_overlay = cv.VideoWriter(sys.argv[7], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_heatmap = cv.VideoWriter(sys.argv[8], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))

def calculate_contour_distance(contour1, contour2):
    x1, y1, w1, h1 = cv.boundingRect(contour1)
    c_x1 = x1 + w1 / 2
    c_y1 = y1 + h1 / 2

    x2, y2, w2, h2 = cv.boundingRect(contour2)
    c_x2 = x2 + w2 / 2
    c_y2 = y2 + h2 / 2

    return max(abs(c_x1 - c_x2) - (w1 + w2) / 2, abs(c_y1 - c_y2) - (h1 + h2) / 2)

heatmap = np.zeros([height, width], dtype=np.uint8)
mask = np.full([height, width], 255, dtype=np.uint8)
mask_col = np.full([height, width, 3], (255,255,255), dtype=np.uint8)

key=2;
color= (0,0,0)
draw = False
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

cv.setMouseCallback(window_name, mouse_callback)

ret, current_col = cap.read()
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
        break
    #elif ( (key>=ord('0')) and (key<=ord('9')) ):
        
mask = cv.cvtColor(mask_col, cv.COLOR_BGR2GRAY)        
cue_prev = mask;
COLOR = ([255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255])


# --- main routine
while (framenum < lastframe) and (framenum < frame_length - 1):
    ret, current_col = cap.read()
    current_gray = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)

    # all uget2
    difference = cv.absdiff(current_gray, ref_gray)
    ret, thresh = cv.threshold(difference, 0, 255, cv.THRESH_TRIANGLE);
    #cv.imshow('heatmap',thresh)
    #DETEKSI DI SINI TERLALU RESTRIKTIF
    
    cue = cv.bitwise_and(thresh, mask)
    contours_cur, hierarchy = cv.findContours(cue, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if (framenum == startframe):
        contours_prev = contours_cur;
    for c in contours_cur:
        cv.fillPoly(cue, pts=c, color=(255))

    # for LOKA: is there any way to do such search faster?
    still_uget = 0;
    for i in range(len(contours_cur)):
        for j in range(len(contours_prev)):
            distance = calculate_contour_distance(contours_cur[i], contours_prev[j])
            if (distance < 1.0):
                cv.fillPoly(cue, pts=contours_cur[i], color=(0))
                still_uget += 1;
                break

    # heatmap
    ret, th1 = cv.threshold(cue, 10, 1, cv.THRESH_BINARY)
    heatmap = heatmap * (1-COEF_FADE_OUT)
    heatmap = np.add(heatmap.clip(None,250), th1*COEF_FADE_IN)
    #heatmap_col = cv.applyColorMap(heatmap, cv.COLORMAP_PARULA)

# ----------- results
# yang dibutuhkan macam benchmark: CACA
# - cacah yang tampak, yang motil, yang males 
# - kerapatan dalam tempat dan waktu (heatmap)
# - arah gerakan (puncak heatmap?)
# - kecepatan gerakan (?)
# - ukuran tiap uget2 (dalam histogram) 
 
    # cellcount from countour
    print("{} {} {}".format(framenum, len(contours_cur), still_uget));
    # buat RINO: do we need stuff like speed to express motility?
    # CSV
    numlist = [framenum, len(contours_cur), still_uget];
    
    # VIDEO 
    # cue
    render = cv.cvtColor(cue, cv.COLOR_GRAY2BGR)
    vid_cue.write(render);

    # imposed
    imposed = cv.bitwise_or(current_col, cue)
    vid_overlay.write(imposed);

    # heatmap
    cc = cv.cvtColor(current_gray, cv.COLOR_GRAY2BGR)
    heatmapoverlay = cv.addWeighted(heatmap_col, 0.6, cc, 0.4, 0)
    vid_heatmap.write(heatmapoverlay);

    contours_prev = contours_cur;
    framenum += 1

    #cv.imshow('cue',render)
    #cv.imshow('imposed',imposed)
    #cv.imshow('heatmap',heatmapoverlay)
    key = cv.waitKey(1) & 0xff
    if key==27:
        quit()

cap.release
vid_cue.release
vid_overlay.release
vid_heatmap.release
