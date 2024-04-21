import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')

cap=cv2.VideoCapture(0)
#uses first camera

j=1
while(j<=2):    #number of classes

    while (1):
        _,frame=cap.read()

        #below is variables of each color, but not only that color
        red=np.matrix(frame[:,:,2]) #B G R
        green=np.matrix(frame[:,:,1])
        blue=np.matrix(frame[:,:,0])

        #separated red image layer
        red_only=np.int16(red)-np.int16(green)-np.int16(blue)
        #separated green image layer
        green_only=np.int16(green)-np.int16(red)
        #separated blue image layer
        blue_only=np.int16(blue)-np.int16(red)
        
        #limits matrix to standard color range
        red_only[red_only<40]=0
        red_only[red_only>=40]=255
        #alter value in brackets to adjust noise in image

        #sets matrix back to image quality
        red_only=np.uint8(red_only)
        
        #limits matrix to standard color range
        green_only[green_only<20]=0
        green_only[green_only>=20]=255
        #alter value in brackets to adjust noise in image

        #sets matrix back to image quality
        green_only=np.uint8(green_only)

        #limits matrix to standard color range
        blue_only[blue_only<50]=0
        blue_only[blue_only>=60]=255
        #alter value in brackets to adjust noise in image

        #sets matrix back to image quality
        blue_only=np.uint8(blue_only)

        #refined image?
        all_only=red_only+green_only+blue_only

        #mask
        mask=np.ones((5,5),np.uint8)
        opening=cv2.morphologyEx(all_only, cv2.MORPH_OPEN,mask)
        cv2.imshow('Masked Image',opening)

        #begin adding mask
        _,labels=cv2.connectedComponents(opening,4)
        #cuts the mask into number of visible objects
        b=np.matrix(labels)

        i=1
        while(i<np.amax(labels) and i<10):
            #inverts any 0 into a 1 from b
            Obj=b==i
            #converts variable into image quality
            Obj=np.uint8(Obj)
            #increases brightness of image
            Obj[Obj>0]=255
            cv2.imshow('Object '+str(i),Obj)
            i=i+1

        
        #displays windows
        cv2.imshow('Frame', frame)
        cv2.imshow('All Only', all_only)



        k=cv2.waitKey(5)
        #will wait until key press (5>?)
        if k==27:
            #breaks on ESC
            break

    cv2.destroyAllWindows()

    #Find the RGB values of each object as the first three features
    AvgRed=[]
    AvgGreen=[]
    AvgBlue=[]

    i=1
    while(i<=np.amax(labels)):
        Obj=b==i
        RedValues=np.array(Obj)*np.array(red)
        GreenValues=np.array(Obj)*np.array(green)
        BlueValues=np.array(Obj)*np.array(blue)

        size=np.sum(Obj)
        #angle=np.angle(Obj) # should allow for a way to differentiate shapes? throws a fit when running
        AvgSize=size/255.0
        #AvgAngle=angle/255.0
        AvgRed=np.append(AvgRed,np.sum(RedValues)/size)
        AvgGreen=np.append(AvgGreen,np.sum(GreenValues)/size)
        AvgBlue=np.append(AvgBlue,np.sum(BlueValues)/size)

        i=i+1

    if(j==1): #plots in blue
        ax.scatter(AvgRed,AvgBlue,AvgSize, c='b')
        #plt.hold(True)
    if(j==2): #plots in red
        ax.scatter(AvgRed,AvgBlue,AvgSize, c='r')

    j=j+1



ax.set_xlabel('RedValue')
ax.set_ylabel('BlueValue')
ax.set_zlabel('SizeValue')

plt.show()