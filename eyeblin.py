import cv2
import cvzone
import pyttsx3
engine = pyttsx3.init()
#from engine import Engine
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640,360,[0,40],invert = True)
idList = [22,23,24,26,110,157,158,159,160,161,130,243]
ratioList = []
blinkCounter = 0
color = (255, 0, 255)
engine = pyttsx3.init()
#name = "unknown"
while True:
    success,img = cap.read()
    img,faces = detector.findFaceMesh(img,draw = False)
    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img,face[id],5,(255,0,255))
            #cv2.circle(img,face[id],5,(255,0,255),cv2.FILLED)
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghthor,_ = detector.findDistance(leftLeft,leftRight)
        lenghtVer,_ = detector.findDistance(leftUp,leftDown)
        cv2.line(img,leftUp,leftDown,(0,200,0),3)
        cv2.line(img,leftLeft,leftRight,(0,200,0),3)
        ratio = int((lenghtVer/lenghthor)*100)
        ratioList.append(ratio)
        if len(ratioList)>3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList)/len(ratioList)
        if ratioAvg<37:
            blinkCounter +=1
            color = (0,200,0)
            if blinkCounter%5==0:
                engine.say("Urgent Help Needed")
                engine.runAndWait()
        cvzone.putTextRect(img,f'Blink Count:{blinkCounter}',(50,50),colorR=color)   
        color = (255, 0, 255)
        
        imgPlot = plotY.update(ratioAvg,color)
        #cv2.imshow('ImagePlot', imgPlot)
        imgStack = cvzone.stackImages([img,imgPlot],1,1)
    else:
        imgStack = cvzone.stackImages([img,img],1,1)
    cv2.imshow('Image' , imgStack)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
