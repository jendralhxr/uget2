import numpy as np
import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))

fgbg = cv2.createBackgroundSubtractorMOG2(200, 15, bool(0))

params = cv2.SimpleBlobDetector_Params()
detector = cv2.SimpleBlobDetector()

a = 1.2 # Contrast control (1.0-3.0)
b = 0 # Brightness control (0-100)
n=1
step = 0

frameb = []
aggre= 5;

while(1):
    ret, frame = cap.read()
    invr = cv2.bitwise_not(frame)
    # init the frames
    adjusted = cv2.convertScaleAbs(invr, alpha=a, beta=b)
    framen = fgbg.apply(adjusted)
    
    if n>0:
        for i in range(0, aggre):
            frameb.append(framen);
        n=0
        
    # shift the frames
    for i in range(0, aggre-1):
        frameb[i]= frameb[i+1];
    frameb[aggre-1] = framen
    
    frame_sum= 0;
    for i in range(0, aggre):
        frame_sum += frameb[i]
    
    # calculate blob position here
    contours, hierarchy = cv2.findContours(frame_sum, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    print( len(contours))
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        center = (x,y)
        #print (center)
    
    cv2.imshow('frame_sum from frames',frame_sum)
    cv2.imshow('frame',frame_sum)
    
    k = cv2.waitKey(16) & 0xff
    if k == 27:
        break

#for n in range(0, aggre):
#    cv2.imwrite('{}.png'.format(str(n).zfill(5)), frameb[n])
            
cap.release()
cv2.destroyAllWindows()