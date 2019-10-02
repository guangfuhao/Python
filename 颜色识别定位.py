#注：定位中解释下，因为我打开摄像头的时候，窗口默认大小是640*480的，
#你输出圆心坐标后，若想知道实际的距离，可以根据你的图像像素的大小，然后在乘上坐标的值，就可以知道实际的距离。

from collections import  deque
import numpy as np
import time
import cv2

mybuffer = 16
pts = deque(maxlen=mybuffer)
flag = 0
camera = cv2.VideoCapture(0)
time.sleep(3)
while flag <= 5:
    print("000")   
    flag += 1
    if flag ==1:
        print("111")
        blueLower = np.array([100, 43, 46])
        blueUpper = np.array([124, 255, 255])
        (ret, frame) = camera.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, blueLower, blueUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key = cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            if radius > 150:#这里150可以变，改成你想要的大小
                print"蓝色"
                print(int(x), int(y))#输出圆心坐标若不要这些坐标可以删除
                if int(x) < 300:
                    print"right"
                if int(x) > 340:
                    print"left"
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)
        else:
            pts.clear()
        cv2.imshow('Frame', frame)
  
    if flag ==2:
        print("222")
        greenLower = np.array([35, 43, 46])
        greenUpper = np.array([77, 255, 255])
        (ret, frame) = camera.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key = cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            if radius > 150:
                print"绿色"
                print(int(x), int(y))
            if int(x) < 300:
               print"right"
            if int(x) > 340:
               print"left"
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)
        else:
            pts.clear()
        cv2.imshow('Frame', frame)
    
    if flag ==3:
        redLower = np.array([156, 43, 46])
        redUpper = np.array([180, 255, 255])
        print("333")
        (ret, frame) = camera.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, redLower, redUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key = cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            if radius > 150:
                print"红色"
                print(int(x), int(y))
            if int(x) < 300:
               print"right"
            if int(x) > 340:
               print"left"
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)
        else:
            pts.clear()
        cv2.imshow('Frame', frame)
    
    if flag ==4:
        whileLower = np.array([0, 0, 180])
        whileUpper = np.array([180, 60, 255])
        print("444")
        (ret, frame) = camera.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, whileLower, whileUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key = cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            if radius > 150:
                print"白色"
                print(int(x), int(y))
            if int(x) < 300:
               print"right"
            if int(x) > 340:
               print"left"
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)
        else:
            pts.clear()
        cv2.imshow('Frame', frame)
   
    if flag ==5:
        greenLower = np.array([0, 0, 0])
        greenUpper = np.array([180, 255, 46])
        print("555")
        (ret, frame) = camera.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key = cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            if radius > 150:
                print"黑色"
                print(int(x), int(y))
            if int(x) < 300:
               print"right"
            if int(x) > 340:
               print"left"
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)
        else:
            pts.clear()
        cv2.imshow('Frame', frame)

#摄像头释放
camera.release()
#销毁所有窗口
cv2.destroyAllWindows()
