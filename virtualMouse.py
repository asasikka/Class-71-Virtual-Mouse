import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import numpy as np
import math
import time

screenshotnum = 0

#Screen Width and Height
screenSize = pyautogui.size()
screenWidth=screenSize[0]
screenHeight=screenSize[1]
print(screenWidth, screenHeight)
captureVideo=cv2.VideoCapture(0)
# print(captureVideo.get(cv2.CAP_PROP_FRAME_WIDTH),captureVideo.get(cv2.CAP_PROP_FRAME_HEIGHT),captureVideo.get(cv2.CAP_PROP_FPS))
width=640
height=500
frameR=100

prevX=0
prevY=0

currX=0
currY=0

detector=HandDetector(detectionCon=0.8)
smoothingFactor=1

while True:
    try:
        check,image=captureVideo.read()
        # print(image)
        cameraFlipedImage=cv2.flip(image,1)
        handsDetector=detector.findHands(cameraFlipedImage,flipType=False)
        hands=handsDetector[0]
        # print(hands)
        
        if hands:
            hand1=hands[0]
            lmList1=hand1['lmList']
            handType1=hand1['type']

            fingers1=detector.fingersUp(hand1)

            if(len(lmList1)>0):
                indexFingerTipX=lmList1[8][0]
                indexFingerTipY=lmList1[8][1]

                if(fingers1[1] == 1 and fingers1[2] == 0):
                    x3=np.interp(indexFingerTipX, (frameR,width-frameR),(0,screenWidth))
                    y3=np.interp(indexFingerTipY, (frameR,height-frameR),(0,screenHeight))
                    # print(x3,y3)
                    currX=prevX+(x3-prevX)/smoothingFactor
                    currY=prevY+(y3-prevY)/smoothingFactor

                    prevX=currX
                    prevY=currY

                    pyautogui.moveTo(currX,currY)
                    
                    cv2.circle(cameraFlipedImage,(indexFingerTipX,indexFingerTipY),15,(0,255,0),cv2.FILLED)
                
                if(fingers1[1] == 1 and fingers1[2] == 1):
                    distance=math.dist(lmList1[8], lmList1[12])
                    indexFingerTipX=lmList1[8][0]
                    indexFingerTipY=lmList1[8][1]
                    middleFingerTipX=lmList1[12][0]
                    middleFingerTipY=lmList1[12][1]

                    cx=(indexFingerTipX+middleFingerTipX)//2
                    cy=(indexFingerTipY+middleFingerTipY)//2

                    cv2.line(cameraFlipedImage,(indexFingerTipX,indexFingerTipY),(middleFingerTipX,middleFingerTipY),(255,0,255),2)

                    if distance<20:
                        print("Distance: ", distance)
                        cv2.circle(cameraFlipedImage,(cx,cy),15,(255,0,0),cv2.FILLED)
                        pyautogui.click()

                if(fingers1[0] == 0 and fingers1[1] == 1 and fingers1[2] == 1 and fingers1[3] == 1 and fingers1[4] == 1):
                    time.sleep(0.1)
                    pyautogui.scroll(300)
                
                if(fingers1[1] == 1 and fingers1[1] == 0 and fingers1[2] == 0 and fingers1[3] == 0 and fingers1[4] == 0):
                    time.sleep(0.1)
                    pyautogui.scroll(-300)

                if(fingers1[1] == 0 and fingers1[1] == 0 and fingers1[2] == 0 and fingers1[3] == 0 and fingers1[4] == 0):
                    screenpath=f'screenshots/screenshot_{screenshotnum}.png'
                    pyautogui.screenshot(screenpath)
                    print(f'Screenshot Saved at {screenpath}')
                    screenshotnum+=1
                    time.sleep(1)
            # print(fingers1)

              

    except Exception as e:
        print(e)
    # cv2.imshow("mypic",image)
    cv2.imshow("mypicfliped",cameraFlipedImage)
    if cv2.waitKey(1) == 32:
       break
captureVideo.release()
