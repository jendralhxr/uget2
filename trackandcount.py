# python -u trackandcount.py input.mp4 bg.png 0 24000000000000 log.csv cue.mp4 output.mp4 heatmap.mp4 arrow.png [startx starty]...

import numpy as np
import math
import cv2 as cv
import sys
import csv
import random

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

# buat LOKA: needs to define the starting point more aesthetically

trackers_count = int((len(sys.argv) - 10) / 2)
trackx = np.zeros(trackers_count, dtype=np.uint16)
tracky = np.zeros(trackers_count, dtype=np.uint16)
trackx_init = np.zeros(trackers_count, dtype=np.uint16)
tracky_init = np.zeros(trackers_count, dtype=np.uint16)
for i in range(trackers_count):
    trackx[i] = int(sys.argv[2 * i + 10])
    tracky[i] = int(sys.argv[2 * i + 11])
    trackx_init[i] = trackx[i]
    tracky_init[i] = tracky[i]
    print("tracker{}: {} {}".format(i, trackx[i], tracky[i]))

TRACK_HOP = 12;

# buat LOKA: pheromone trail and evaporation coefficients
# tracking trail
COEF_PATH_FADE = 1
# heatmap
COEF_EVAPORATE = 1
COEF_TRAIL = 8
COEF_SMEAR = 6
DIST_SMEAR = 1

COLOR = ([255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255])


def calculate_contour_distance(contour1, contour2):
    x1, y1, w1, h1 = cv.boundingRect(contour1)
    c_x1 = x1 + w1 / 2
    c_y1 = y1 + h1 / 2

    x2, y2, w2, h2 = cv.boundingRect(contour2)
    c_x2 = x2 + w2 / 2
    c_y2 = y2 + h2 / 2

    return max(abs(c_x1 - c_x2) - (w1 + w2) / 2, abs(c_y1 - c_y2) - (h1 + h2) / 2)


path = np.zeros([height, width, 3], dtype=np.uint8)
path1 = np.ones([height, width, 3], dtype=np.uint8)

pheromone = np.zeros([height, width], dtype=np.uint8)
ph1 = np.ones([height, width], dtype=np.uint8)

mask = np.zeros([height, width, 1], dtype=np.uint8)

mask = cv.bitwise_not(mask);
# buat LOKA: need some interactive way to define the mask's countour
contours = np.array([[640, 110], [390, 130], [320, 260], [345, 324], [640, 300]])  # 8879
cv.fillPoly(mask, pts=[contours], color=(0))
cue_prev = mask;

# --- main routine
while (framenum < lastframe) and (framenum < frame_length - 1):
    ret, current_col = cap.read()
    current_gray = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)

    # all uget2
    difference = cv.absdiff(current_gray, ref_gray)
    ret, thresh = cv.threshold(difference, 0, 255, cv.THRESH_TRIANGLE);
    cue = cv.bitwise_and(thresh, mask)
    contours_cur, hierarchy = cv.findContours(cue, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if (framenum == startframe):
        contours_prev = contours_cur;
    for c in contours_cur:
        cv.fillPoly(cue, pts=c, color=(255))

    # for LOKA: is there any way to do such search faster?
    still_uget = 0;
    for i in range(len(contours_cur)):
        for j in range(i+1, len(contours_prev)):
            distance = calculate_contour_distance(contours_cur[i], contours_prev[j])
            if (distance < 1.0):
                cv.fillPoly(cue, pts=contours_cur[i], color=(0))
                still_uget += 1;
                break

    # tracking
    for t in range(trackers_count):
        for i in range(len(contours_cur)):
            cnt = contours_cur[i]
            M = cv.moments(cnt)
            if (M['m00'] != 0):
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                if (abs(cx - trackx[t]) < TRACK_HOP) and (abs(cy - tracky[t]) < TRACK_HOP):
                    cv.line(path, (trackx[t], tracky[t]), (cx, cy), COLOR[t % 6], 2)
                    cv.circle(path, (cx, cy), 1, COLOR[t % 6], 2)
                    trackx[t] = cx + random.randint(-2, 2)
                    tracky[t] = cy + random.randint(-2, 2)
                    break;
        # print("tracker{}: {} {}".format(t, trackx[t], tracky[t]))

    path = path - (COEF_PATH_FADE * path1).clip(None, path)

    # heatmap
    ret, th1 = cv.threshold(cue, 10, 1, cv.THRESH_BINARY)

    smear = np.zeros([height, width], dtype=np.uint8)
    affineMat1 = np.float32([[1, 0, DIST_SMEAR], [0, 1, 0]])
    affineMat2 = np.float32([[1, 0, -DIST_SMEAR], [0, 1, 0]])
    affineMat3 = np.float32([[1, 0, 0], [0, 1, DIST_SMEAR]])
    affineMat4 = np.float32([[1, 0, 0], [0, 1, -DIST_SMEAR]])
    affineMat5 = np.float32([[1, 0, DIST_SMEAR], [0, 1, DIST_SMEAR]])
    affineMat6 = np.float32([[1, 0, -DIST_SMEAR], [0, 1, -DIST_SMEAR]])
    affineMat7 = np.float32([[1, 0, -DIST_SMEAR], [0, 1, DIST_SMEAR]])
    affineMat8 = np.float32([[1, 0, DIST_SMEAR], [0, 1, -DIST_SMEAR]])
    shake1 = cv.warpAffine(th1, affineMat1, (width, height))
    shake2 = cv.warpAffine(th1, affineMat2, (width, height))
    shake3 = cv.warpAffine(th1, affineMat3, (width, height))
    shake4 = cv.warpAffine(th1, affineMat4, (width, height))
    shake5 = cv.warpAffine(th1, affineMat5, (width, height))
    shake6 = cv.warpAffine(th1, affineMat6, (width, height))
    shake7 = cv.warpAffine(th1, affineMat7, (width, height))
    shake8 = cv.warpAffine(th1, affineMat8, (width, height))
    smear = cv.bitwise_or(smear, shake1)
    smear = cv.bitwise_or(smear, shake2)
    smear = cv.bitwise_or(smear, shake3)
    smear = cv.bitwise_or(smear, shake4)
    smear = cv.bitwise_or(smear, shake5)
    smear = cv.bitwise_or(smear, shake6)
    smear = cv.bitwise_or(smear, shake7)
    smear = cv.bitwise_or(smear, shake8)
    pheromone = np.add(pheromone.clip(None, 255 - COEF_SMEAR), smear * COEF_SMEAR)
    pheromone = np.add(pheromone.clip(None, 255 - COEF_TRAIL), th1 * COEF_TRAIL)
    pheromone = pheromone - (COEF_EVAPORATE * ph1).clip(None, pheromone)

    heatmap = cv.applyColorMap(pheromone, cv.COLORMAP_PARULA)

    # ----------- results

    # cellcount from countour
    print("{} {} {}".format(framenum, len(contours_cur), still_uget));
    # buat RINO: do we need stuff like speed to express motility?
    # CSV
    numlist = [framenum, len(contours_cur), still_uget];
    for i in range(trackers_count):
        numlist.append("{} {}".format(trackx[i], tracky[i]))
    writer.writerow(numlist);

    # VIDEO 
    # cue
    render = cv.cvtColor(cue, cv.COLOR_GRAY2BGR)
    render = cv.bitwise_or(render, path)
    for i in range(trackers_count):
        cv.circle(render, (trackx[i], tracky[i]), 1, (0, 0, 255), 2)
    vid_cue.write(render);

    # imposed on input
    impose = cv.bitwise_or(current_col, path)
    for i in range(trackers_count):
        cv.circle(impose, (trackx[i], tracky[i]), 1, (0, 0, 255), 2)
    vid_overlay.write(impose);

    # heatmap
    cc = cv.cvtColor(current_gray, cv.COLOR_GRAY2BGR)
    heatmapoverlay = cv.addWeighted(heatmap, 0.6, cc, 0.4, 0)
    vid_heatmap.write(heatmapoverlay);

    contours_prev = contours_cur;
    framenum += 1

    # cv.imshow('cue',render)
    # cv.imshow('imposed',impose)
    # cv.imshow('heatmap',heatmapoverlay)
    # k = cv.waitKey(1) & 0xFF
    # if k== 27: # esc
    # break

    # GRAPHS

for t in range(trackers_count):
    cv.arrowedLine(impose, (trackx_init[t], tracky_init[t]), (trackx[t], tracky[t]), COLOR[t % 6], 1, tipLength=0.04)

cv.imwrite(sys.argv[9], impose)

cap.release
vid_cue.release
vid_overlay.release
vid_heatmap.release
