# PAINT APPLICATION WITH ADJUSTABLE COLOR AND BRUSH SIZE

import cv2
import numpy as np

draw = False
window_name = "Paint Brush Application"
color_win_position = [(400, 30), (490,90)]

img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow(window_name)

def draw_circle(event, x, y, flags, param):
    global draw, img

    if event == cv2.EVENT_LBUTTONDOWN:
        draw = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if draw:
            cv2.circle(img, (x,y), 10, (255, 255, 255), -1)

    elif event==cv2.EVENT_LBUTTONUP:
        draw = False
        cv2.circle(img, (x,y), 10, (255, 255, 255), -1)

cv2.setMouseCallback(window_name, draw_circle)

while(1):
    cv2.imshow(window_name, img)
    key = cv2.waitKey(1) & 0xff
    if key==ord('q'):
        break

    #cv2.rectangle(img, color_win_position[0], color_win_position[1], (b,g,r), -1)

cv2.destroyAllWindows()
