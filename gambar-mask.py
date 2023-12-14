#!/usr/bin/python


import cv2
import numpy as np

draw = False

window_name= "uget2"
img = np.zeros((512,512,1), np.uint8)
cv2.namedWindow(window_name)

#color= (255, 255, 255)
color=255

def draw_circle(event, x, y, flags, param):
	global draw, img

	if event == cv2.EVENT_LBUTTONDOWN:
		draw = True
		cv2.circle(img, (x,y), 10, color, -1)

	elif event == cv2.EVENT_MOUSEMOVE:
		if draw:
			cv2.circle(img, (x,y), 10, color, -1)

	elif event==cv2.EVENT_LBUTTONUP:
		draw = False
		#cv2.circle(img, (x,y), 10, (255, 255, 255), -1)

cv2.setMouseCallback(window_name, draw_circle)

while(1):
	cv2.imshow(window_name, img)
	key = cv2.waitKey(1) & 0xff
	if key==ord('q'):
		break
	elif key==ord('1'):
		#color = (255,0,0)
		color=0
		print(color)
	elif key==ord('2'):
		#color = (0,255,0)
		color=128
		print(color)
	elif key==ord('3'):
		#color = (0,0,255)
		color=200
		print(color)


cv2.destroyAllWindows()
