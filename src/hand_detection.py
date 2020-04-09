import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Se define el intervalo de color que se va a detectar
low_yellow = np.array([20, 100, 100], np.uint8)
high_yellow = np.array([30, 255, 255], np.uint8)

def get_hand_position(frame, draw=True):
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_HSV, low_yellow, high_yellow)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x,y,area = 0,0,0
    for c in contours:
      area = cv2.contourArea(c)
      if area > 3000:
        M = cv2.moments(c)
        if (M["m00"]==0): M["m00"]=1
        x = int(M["m10"]/M["m00"])
        y = int(M['m01']/M['m00'])
        if draw:
          cv2.circle(frame, (x,y), 7, (255,0,0), 1)
          font = cv2.FONT_HERSHEY_SIMPLEX
          cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
          cv2.putText(frame, '{}'.format(area),(x+10,y+20), font, 0.75,(0,255,0),1,cv2.LINE_AA)
          new_contour = cv2.convexHull(c)
          cv2.drawContours(frame, [new_contour], 0, (255,0,0), 3)
    
    cv2.imshow('frame', frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return   
    return x, y, area

def get_frame():
  ret, frame = cap.read()
  return cv2.flip(frame, 1)