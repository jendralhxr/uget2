import numpy
import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))

fgbg = cv2.createBackgroundSubtractorMOG2(200, 15, bool(0))

params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 15
detector = cv2.SimpleBlobDetector(params)

a = 1.2 # Contrast control (1.0-3.0)
b = 0 # Brightness control (0-100)
n=1
step = 0

frameb = []
aggre= 20;

while(1):
    ret, frame = cap.read()
    invr = cv2.bitwise_not(frame)
    adjusted = cv2.convertScaleAbs(invr, alpha=a, beta=b)
    framen = fgbg.apply(adjusted)
    
    # init the frames
    if n:
        for n in range(0, aggre):
            frameb.append(framen);
    
    # add the frames
    frame_sum= 0;
    frameb[0] = framen
    for n in range(0, aggre):
        frame_sum += frameb[n]
    
    # shift the frames
    for n in range(1, aggre):
        frameb[n] = frameb[n-1]
    
    # calculate blob position here
    #keypoints = detector.detect(sum) # iki nggarahi mati
    
    cv2.imshow('frame_sum from frames',frame_sum)
    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(16) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()