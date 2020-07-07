import numpy as np
import math
import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
 
fgbg = cv2.createBackgroundSubtractorMOG2(200, 15, bool(0))

a = 1.2 # Contrast control (1.0-3.0)
b = 0 # Brightness control (0-100)
frameb = []
aggre= 5;

framenum = 0
while(1):
    ret, frame = cap.read()
    invr = cv2.bitwise_not(frame)
    # init the frames
    adjusted = cv2.convertScaleAbs(invr, alpha=a, beta=b)
    framen = fgbg.apply(adjusted)
    
    if framenum<1:
        for i in range(0, aggre):
            frameb.append(framen);
    framenum += 1
            
    
    # shift the frames
    for i in range(0, aggre-1):
        frameb[i]= frameb[i+1];
    frameb[aggre-1] = framen
    
    frame_sum= 0;
    for i in range(0, aggre):
        frame_sum += frameb[i]
    
    # calculate blob position here
    contours, hierarchy = cv2.findContours(frame_sum, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    #print( len(contours)) # cacah uget2
    total_x= 0
    total_y= 0
    total_m= 0
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        m = w*h
        total_x += x*m
        total_y += y*m
        total_m += m
        #center = (x,y)
        #print (center)
    
    if framenum > aggre:
        #hitung kepadatan
        r= math.sqrt(total_m);
        center_x= total_x / total_m;
        center_y= total_y / total_m;
        density= 0;
        
        for i in range(int(center_x- (r/3)), int(center_x+(r/3)), 1):
            for j in range(int(center_y-(r/3)), int(center_y+(r/3)), 1):
                if frame_sum[i,j]:
                    density +=1
    
        print("cacah:{}\ttitik:({:0.2f},{:0.2f})\tradius={:0.2f}\tdensity={:0.2f}".format(len(contours), center_x, center_y, r,density/r))
        
    cv2.imshow('deteksi',frame_sum)
    
    k = cv2.waitKey(16) & 0xff
    if k == 27:
        break

for n in range(0, aggre):
    cv2.imwrite('{}.png'.format(str(n).zfill(5)), frameb[n])
            
cap.release()
cv2.destroyAllWindows()