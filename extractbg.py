# python -u extractbg.py input.mp4 0 8000 output.png

import numpy as np
import math
import cv2 as cv
import sys

framenum= 0
THRESH_VAL= 40
STEP= 3

cap = cv.VideoCapture(sys.argv[1])
height = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
width = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
fps = cap.get(cv2.CAP_PROP_FPS;
vsize = (int(height/4), int(width/4))        

ref_col= cv.imread(sys.argv[2])
ref = cv.cvtColor(ref_col, cv.COLOR_BGR2GRAY)

lastframe= int(sys.argv[3])
csvlog = open(sys.argv[4], 'w', newline='')
writer = csv.writer(csvlog)
#----- need to define the columns
header= ['framenum','count','motility']
writer.writerow(header);

vidout = cv.VideoWriter(sys.argv[5],cv.VideoWriter_fourcc(*'mp4v'), fps, [height, width])
#print(vidout.frameSize)

# region of interest
mask = np.zeros((width,height,1),np.uint8)
# need interactive way to define the mask's countour
contours = np.array([ [0,510], [0,790], [4096, 790], [4096, 510] ])
cv.fillPoly(mask, pts =[contours], color=(0))

while (framenum<lastframe):
    ret, frame_col = cap.read()
    frame = cv.cvtColor(frame_col, cv.COLOR_BGR2GRAY)
    
    framenum += 1
    #print(ref.shape)
    
    difference= cv.absdiff(ref, frame)
    ret,thresh = cv.threshold(difference,THRESH_VAL,255,cv.THRESH_BINARY | cv.THRESH_OTSU);
    cue = cv.bitwise_and(thresh, mask)
    #dist = cv.distanceTransform(cue, cv.DIST_L2, 3)

    # le fancy shaker filter
    affineMat1 = np.float32([[1, 0, STEP], [0, 1, 0]])
    shake1 = cv.warpAffine(cue, affineMat1, (height, width))
    affineMat2 = np.float32([[1, 0, -STEP], [0, 1, 0]])
    shake2 = cv.warpAffine(cue, affineMat2, (height, width))
    affineMat3 = np.float32([[1, 0, 0], [0, 1, STEP]])
    shake3 = cv.warpAffine(cue, affineMat3, (height, width))
    affineMat4 = np.float32([[1, 0, 0], [0, 1, -STEP]])
    shake4 = cv.warpAffine(cue, affineMat4, (height, width))
    #print("cue-{} 1-{} 2-{} 3-{} 4-{}".format(cue.shape, shake1.shape, shake2.shape, shake3.shape, shake4.shape))   
    cue = cv.bitwise_and(cue, shake1)
    cue = cv.bitwise_and(cue, shake2)
    cue = cv.bitwise_and(cue, shake3)
    cue = cv.bitwise_and(cue, shake4)
    
    M = cv.moments(cue)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    #print("{} {} {}: {} {} {}".format(framenum, cX, cY, M["m10"], M["m01"], M["m00"]))
    if (framenum%100 == 0):
        print("{} {} {}".format(framenum, cX, cY))
    
    
    numlist= [framenum, cX, cY];
    writer.writerow(numlist);
    
    # video output sometimes doesnt work on me
    render = cv.cvtColor(cue,cv.COLOR_GRAY2RGB)
    render = cv.circle(render, (cX, cY), 20, (255, 0, 0), 3)
    #display=cv.resize(render, vsize, interpolation= cv.INTER_AREA)
    vidout.write(render)
    
    #cv.imshow('display',display)
    #k = cv.waitKey(1) & 0xFF
    #if k== 27: # esc
    #    break

cap.release
vidout.release 
