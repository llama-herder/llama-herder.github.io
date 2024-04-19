import numpy as np
import cv2

cap=cv2.VideoCapture(0)
#uses first camera

while (1):
    _,frame=cap.read()

    cv2.imshow('Frame', frame)

    k=cv2.waitKey(5)
    #will wait until key press (5>?)
    if k==27:
        #breaks on ESC
        break

cv2.destroyAllWindows()