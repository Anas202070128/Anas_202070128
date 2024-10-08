import cv2
import mediapipe as mp
import numpy as np
import math

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]

while True:
   success, img = cap.read()
   img = cv2.flip(img, 1)
   imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   results = hands.process(imgRGB)
    
   lmList = []

   if results.multi_hand_landmarks:
      for handLms in results.multi_hand_landmarks:
         for id, lm in enumerate(handLms.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            print(h)
            print(w)
            print(lm.y)
            print(lm.x)
            print(cy)
            print(cx)

            if len(lmList)==21:
               x1,y1 = lmList[4][1], lmList[4][2]
               x2,y2 = lmList[8][1], lmList[8][2]
               cx,cy = (x1+x2) // 2,(y1+y2) // 2

               cv2.circle(img,(x1,y1),8,(200,200,150),cv2.FILLED)
               cv2.circle(img,(x2,y2),8,(200,200,150),cv2.FILLED)
               cv2.line(img,(x1,y1),(x2,y2),(0,0,0),3)
               cv2.circle(img,(cx,cy),8,(255,0,0),cv2.FILLED)

               length = math.hypot( x2 - x1 , y2 - y1 )
               if length > 0:
                cv2.circle(img,(cx,cy),8,(80,50,0),cv2.FILLED)

               if length > 150:
                cv2.circle(img,(cx,cy),8,(255,100,0),cv2.FILLED) 
                
               vol = np.interp(length,[0 , 200],[minVol , maxVol])
               volume.SetMasterVolumeLevel(vol , None)



   cv2.imshow('Hand Tracker', img)
   if cv2.waitKey(5) & 0xff == 27:
      break