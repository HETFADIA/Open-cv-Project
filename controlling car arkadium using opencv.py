#https://youtu.be/j48qQXzsrvQ
import cv2
import numpy as np
import math
import pyvjoy
import pyautogui
from keyboard import press_and_release,press
def nothing(x):
    pass
previouskey=None;
previousdist=0;previousslope=0;
cap = cv2.VideoCapture(0)
cap.set(3, 2400)
cap.set(4, 2400)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
l = np.array([0, 0, 157])
b = np.array([37, 170, 255])
positive = 0
negative = 0
while (True):
    ret, frame = cap.read()
    if (ret == True):

        im = frame
        frame = frame[223:620, 451:1038]
        im = cv2.rectangle(im, (1038, 620), (451, 223), (0, 255, 0), 2)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, l, b)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.dilate(mask, kernel, iterations=3)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        contours, hierarchies = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        try:
            for contour in contours:
                M = cv2.moments(contour)
                area = int(M["m00"])
                if (18000<area<=40000):

                    m1 = cv2.moments(contours[0])
                    m2 = cv2.moments(contours[1])
                    x1 = int(m1["m10"] / m1["m00"])
                    y1 = int(m1["m01"] / m1["m00"])
                    x2 = int(m2["m10"] / m2["m00"])
                    y2 = int(m2["m01"] / m2["m00"])
                    currentdist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

                    if currentdist>100:
                        if x2 != x1:
                            slope = math.tan(((y2 - y1) / (x2 - x1))) * 100
                            if (slope > 0):
                                positive += 1
                            else:
                                negative += 1

                        else:
                            slope = 0

                        if 0.02<abs(previousslope-slope)<20:
                            if slope >  15:

                                for i in range(int(slope/5)):
                                    print("Left")

                                    pyautogui.press("left")
                                previouskey="left"
                            elif slope<-15:
                                for i in range(int(abs(slope/5))):
                                    pyautogui.press("right")
                                    print("right")
                                previouskey="right"

                        else:
                            if previouskey != "" and previouskey!=None:
                                # print("previouskey", previouskey)
                                print(previouskey)
                                pyautogui.press(previouskey)
                        frame = cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                        cv2.drawContours(frame, contour, -1, (244, 255, 0), 3)
                        previousdist=currentdist
                        previousslope=slope;
                    else:
                        if previouskey != '' and previouskey!=None:
                            # print("previouskey", previouskey)
                            print(previouskey)
                            pyautogui.press(previouskey)
                elif (area>40000): #this means both hands are togther and so brake;
                    # print("brake")
                    # previouskey=""
                    continue;

        except:
            continue;
        out.write(res)
        cv2.imshow('Image', frame)
        cv2.imshow('Mask', mask)
        cv2.imshow('res', res)
        k = cv2.waitKey(1)
        if (k == 27):
            break
    else:
        break
print("postive", positive, "negative", negative)
out.release()
cap.release()
cv2.destroyAllWindows()
