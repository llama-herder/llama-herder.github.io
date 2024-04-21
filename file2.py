import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')

cap = cv2.VideoCapture(0)

while(1):

    _,frame=cap.read() # hold the frame, the underscore location can be used to store boolean to show true or false, use underscore when we don't care
    
    red=np.matrix(frame[:,:,2])
    green=np.matrix(frame[:,:,1])
    blue=np.matrix(frame[:,:,0])

    red_only=np.int16(red)-np.int16(green)-np.int16(blue)
    green_only=np.int16(green)-np.int16(red)
    blue_only=np.int16(blue)-np.int16(red)

    red_only[red_only<50]=0
    red_only[red_only>=50]=255 


    green_only[green_only<20]=0
    green_only[green_only>=20]=255
    

    blue_only[blue_only<50]=0
    blue_only[blue_only>=50]=255


    red_only=np.uint8(red_only)
    green_only=np.uint8(green_only)
    blue_only=np.uint8(blue_only)

    all_only=red_only+green_only+blue_only


    mask=np.ones((5,5),np.uint8)
    opening=cv2.morphologyEx(all_only,cv2.MORPH_OPEN,mask)
    cv2.imshow('Masked image',opening)



    _,labels=cv2.connectedComponents(opening,4) #
    b=np.matrix(labels)

    i=1
    while (i<np.amax(labels) and i<10):
        Obj=b==0 #background, Obj1 equals 1 only when b is 0, Obj1 equals 0 when b is not 0
        Obj=np.uint8(Obj) #Convert to data type of images
        Obj[Obj>0]=255
        cv2.imshow('Object'+str(i),Obj)
        i=i+1


    #Obj2=b==1
    #Obj2=np.uint8(Obj2)
    #Obj2[Obj2>0]=255
    #cv2.imshow('Second Object Object',Obj2)

    #Obj3=b==2
    #Obj3=np.uint8(Obj3)
    #Obj3[Obj3>0]=255
    #cv2.imshow('Third Object',Obj3)

    #Obj4=b==3
    #Obj4=np.uint8(Obj4)
    #Obj4[Obj4>0]=255
    #cv2.imshow('Fourth Object',Obj4)

    #red=frame[:,:,2]
    #green=frame[:,:,1]
    #blue=frame[:,:,0]

    cv2.imshow('rgb', frame) # show the frame
    cv2.imshow('All only', all_only)
    #cv2.imshow('Green only', green_only)
    #cv2.imshow('Blue only', blue_only)

    k=cv2.waitKey(5) # wait for 5 millisecond everytime we go through the loop to check see if we press a specific key
    if k==27: # 27 in the k=27 is the code for the escape key
        break # get out of the while loop

cv2.destroyAllWindows() # not indent, that means this should not be in the while loop

#Find the RGB values of each object as the first three features
AvgRed=[]
AvgBlue=[]
AvgGreen=[]

i=1
while(i<=np.amax(labels)):
    Obj=b==i
    RedValues=np.array(Obj)*np.array(red)
    BlueValues=np.array(Obj)*np.array(blue)
    GreenValues=np.array(Obj)*np.array(green)

    size=np.sum(Obj)
    AvgRed = np.append(AvgRed, np.sum(RedValues)/size)
    AvgBlue=np.append(AvgBlue,np.sum(BlueValues)/size)
    AvgGreen=np.append(AvgGreen,np.sum(GreenValues)/size)

    i=i+1

ax.scatter(AvgRed,AvgBlue,AvgGreen, c='b')

ax.set_xlabel('RedValue')
ax.set_ylabel('BlueValue')
ax.set_zlabel('GreenValue')

plt.show()

#print(frame)
#print(labels)