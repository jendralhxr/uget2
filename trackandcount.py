# python -u trackandcount.py input.mp4 0 24000000000000 cue.mp4 heatmap.mp4

import numpy as np
import cv2 as cv
import sys
import cmapy

# heatmap
COEF_FADE_IN  = 1.00
COEF_FADE_OUT = 0.75
HEATMAP_CEIL= COEF_FADE_IN * 60 # persistence presence is noted within 1 second
# buat LOKA: any way to set these values more gracefully? like a slider?

threshold_value = 13 # good place to start
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

vid_cue = cv.VideoWriter(sys.argv[4], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
vid_heat = cv.VideoWriter(sys.argv[5], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))

heatmap = np.zeros([height, width], dtype=np.single)
heatmap_cue = np.full([height, width], 255, dtype=np.uint8)

mask_col = np.full([height, width, 3], (255,255,255), dtype=np.uint8)
mask = np.full([height, width], 255, dtype=np.uint8)

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
    elif key==ord('s'): # start analysis
        cv.destroyAllWindows()    
        break

# --- main routine
while (framenum < lastframe) and (framenum < frame_length - 1):
    ret, current_col = cap.read()
    #vid_cue.write(current_col)
    
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
    contours, hierarchy = cv.findContours(cue_raw, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
	#contours, hierarchy = cv.findContours(cue, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    
    render = current_col
    # LOKA: atau pakai overlay yang lebih cantik
    for c in contours:
        cv.fillPoly(render, pts=c, color=(23,116,255)) # pumpkin orange
    
    
    #heatmap
    heatmap= heatmap + (COEF_FADE_IN * cue_raw/250)
    heatmap= heatmap - COEF_FADE_OUT
    heatmap= np.clip(heatmap, 0, None)
    heatmapf = np.clip(heatmap, 0, HEATMAP_CEIL) # saturated heatmap, only for display    
    heatmapf.itemset((0,0), HEATMAP_CEIL)
    cv.normalize(heatmapf, heatmap_cue, 0, 255, cv.NORM_MINMAX, cv.CV_8UC1)
    heatmap_render = cv.applyColorMap(heatmap_cue, cmapy.cmap('nipy_spectral'))
    
    # current presence
    cmoments= cv.moments(cue_raw, binaryImage=True) 
    cmx = int(cmoments["m10"] / cmoments["m00"])
    cmy = int(cmoments["m01"] / cmoments["m00"])
    cv.circle(heatmap_render, (cmx,cmy), 4, (0,200,0), -1)
    # cumulative heatmap
    hmoments= cv.moments(heatmap)
    hmx = int(hmoments["m10"] / hmoments["m00"])
    hmy = int(hmoments["m01"] / hmoments["m00"])
    cv.circle(heatmap_render, (hmx,hmy), 4, (0,0,200), -1)
    
    cv.imshow("treshold", cue_raw)
    cv.imshow("deteksi", render)
    cv.imshow("heatmap", heatmap_render)
    #vid_cue.write(render)
    
    print(f'{framenum},{len(contours)},{np.min(heatmap)},{np.max(heatmap)},{cmx},{cmy},{hmx},{hmy}')
    
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
    if key==ord('r'): # reset video from the beginning
        vid_cue.release()
        vid_heat.release()
        vid_cue = cv.VideoWriter(sys.argv[4], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
        vid_heat = cv.VideoWriter(sys.argv[5], cv.VideoWriter_fourcc(*'mp4v'), fps, (640, 480))
        framenum= 0
        cap.set(cv.CAP_PROP_POS_FRAMES, float(0.0))
        
cap.release
vid_cue.release
vid_heat.release
