import numpy as np
import math
import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
 
fgbg = cv2.createBackgroundSubtractorMOG2(50, 10, bool(0))

a = 1.2 # Contrast control (1.0-3.0) bukan control tanpa r
b = 0 # Brightness control (0-100)
frameb = []
aggre= 5;

video_width  = int(cap.get(3))  # float
video_height = int(cap.get(4)) # float

density_minimum= 10000000
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
            
    #nulis ngawur
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
        
        x_start= int(center_x - r/2)
        if x_start<0:
            x_start= 0
        x_stop = int(center_x + r/2)
        if x_stop>video_width:
            x_stop= video_width
        y_start= int(center_y - r/2)
        if y_start<0:
            y_start= 0
        y_stop = int(center_y + r/2)
        if y_stop>video_height:
            y_stop= video_height
        #print("{:0.2f} {:0.0f} {:0.0f} {:0.0f} {:0.0f}".format(r,x_start,x_stop,y_start,y_stop))
        
        for i in range(x_start, x_stop-1, 1):
            for j in range(y_start, y_stop-1, 1):
                if frame_sum[j,i]:
                    density +=1
    
        if density_minimum>total_m:
            density_minimum= total_m;
            
        print("time:{:0.2f}\tcount:{}\tpoint:({:0.2f},{:0.2f})\tdensity={:0.0f}\tratio={:0.3f}".format(framenum/60,len(contours), center_x, center_y, total_m, total_m/density_minimum))
        
    cv2.imshow('frame',frame)
    cv2.imshow('deteksi',frame_sum)
    
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

#for n in range(0, aggre):
#    cv2.imwrite('{}.png'.format(str(n).zfill(5)), frameb[n])
            
cap.release()
cv2.destroyAllWindows()