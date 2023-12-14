#!/usr/bin/python


import cv2 as cv
import numpy as np

draw = False

window_name= "uget2"
mask_col = np.full((512,512,3), 255, dtype=np.uint8)
cv.namedWindow(window_name)

color= (255, 255, 255)
color=128

def draw_circle(event, x, y, flags, param):
	global draw, mask_col, color
	if event == cv.EVENT_LBUTTONDOWN:
		draw = True
		cv.circle(mask_col, (x,y), 8, color, -1)
	elif event == cv.EVENT_MOUSEMOVE:
		if draw:
			cv.circle(mask_col, (x,y), 8, color, -1)
	elif (event==cv.EVENT_LBUTTONUP):
		draw = False

cv.setMouseCallback(window_name, draw_circle)

while(1):
	cv.imshow(window_name, mask_col)
	key = cv.waitKey(1) & 0xff
	if key==ord('q'):
		break
	elif key==ord('1'):
		color = (255,0,0)
		#color=0
		print(color)
	elif key==ord('2'):
		color = (0,255,0)
		#color=128
		print(color)
	elif key==ord('3'):
		color = (0,0,255)
		#color=200
		print(color)


cv.destroyAllWindows()
