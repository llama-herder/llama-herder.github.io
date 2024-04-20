import numpy as np
import cv2

cap=cv2.VideoCapture(0)
#uses first camera

while (1):
    _,frame=cap.read()

    #below is variables of each color, but not only that color
    red=np.matrix(frame[:,:,2]) #B G R
    green=np.matrix(frame[:,:,1])
    blue=np.matrix(frame[:,:,0])

    #separated red image layer
    red_only=np.int16(red)-np.int16(green)-np.int16(blue)
    
    #limits matrix to standard color range
    red_only[red_only<0]=0
    red_only[red_only>255]=255

    #sets matrix back to image quality
    red_only=np.uint8(red_only)

    #displays windows
    cv2.imshow('Frame', frame)
    cv2.imshow('Red Only', red_only)



    k=cv2.waitKey(5)
    #will wait until key press (5>?)
    if k==27:
        #breaks on ESC
        break

cv2.destroyAllWindows()