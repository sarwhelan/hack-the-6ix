import numpy as np
import cv2


#In the first part of the code we train the face cascade with the xml file.
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade= cv2.CascadeClassifier('haarcascade_eye.xml')

#Start capturing video
cap=cv2.VideoCapture(0)


leftWink=False
leftWinkCounter=0
rightWink=False
rightWinkCounter=0
blinkWink=False
blinkWinkCounter=0


while(True):

    #These return a true/false if the frame is read correctly
    ret,frame=cap.read()

    #Convert the frame to grayscale so we can analyze it using a Haar cascade
    grayFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Now, find faces in the image

    #Faces are returned as a list of rectangles: Rect(x,y,w,h)
    faces = face_cascade.detectMultiScale(grayFrame, 1.3, 5)

    #Loops for every rectangle
    for(x,y,w,h) in faces:

        #Draw a box around the face.
        cv2.rectangle(frame,(x,y),(x+w,y+h), (255,0,0),2)
        #Find eyes now cause they're always in the face
        #We input the grey region of interest (the rectange that the face we are looping for)


        #right eye first
        rightGrayROI= grayFrame[y:y+(h/2), x:x+(w/2)]
        rightColourROI=frame[y:y+(h/2),x:x+(w/2)]
        rightEye=eye_cascade.detectMultiScale(rightGrayROI)

        leftGrayROI= grayFrame[y:y+(h/2),(x+(w/2)):x+w]
        leftColourROI=frame[y:y+(h/2),(x+(w/2)):x+w]
        leftEye=eye_cascade.detectMultiScale(leftGrayROI)


        if  (not len(leftEye) and not len(rightEye)):
            blinkWink=True
            blinkWinkCounter+=1
            print "BLINK WINK COUNTER: " + str(blinkWinkCounter)
            if (blinkWinkCounter>10):
                print "blink"


        else:
            blinkWink=False
            blinkWinkCounter=0
            if not len(leftEye):
                leftWink=True
                leftWinkCounter+=1
                print leftWinkCounter
                if (leftWinkCounter>10):
                    print "left wink"

            else:
                leftWink=False
                leftWinkCounter=0

            if not len(rightEye):
                rightWink=True
                rightWinkCounter+=1
                print rightWinkCounter
                if (rightWinkCounter>10):
                    print "right wink"
            else:
                rightWink=False
                rightWinkCounter=0

        #Draw eye rectangles
        for (ex,ey,ew,eh) in rightEye:
            cv2.rectangle(rightColourROI,(ex,ey),(ex+ew,ey+eh),(0,120,120),2)

        for (ex,ey,ew,eh) in leftEye:
            cv2.rectangle(leftColourROI,(ex,ey),(ex+ew,ey+eh),(0,0,120),2)

    #Display face + rectangle
    cv2.imshow('frame',frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#Release the capture, destroy windows.
cap.release()
cv2.destroyAllWindows()
