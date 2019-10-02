# -*- coding: utf-8 -*-
#!/usr/bin/env python   #指定通过python解释代码(必须放在首行，不可少)

#https://www.jianshu.com/p/e98457cabf42
#https://blog.csdn.net/liu_jiangwen/article/details/85934447
#https://blog.csdn.net/qq_31063727/article/details/99980530

#from std_msgs.msg import Int32MultiArray    #导入python的标准字符处理库
import cv2 
import numpy as np
import imutils
import time 
import math

#打开摄像头
camera=cv2.VideoCapture(0)
#设定红色阈值，HSV空间             
boundaries = [ ( [0, 100, 100],    #lower color range
              [10, 255, 255] ) ]#upper color range 

while True:
    ret,frame = camera.read()   
    #判断是否成功打开摄像头
    if not ret:
        print("No Camera")
        break
    # resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=640)
    # 进行高斯模糊
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #转到HSV空间
    hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV) 
    cv2.imshow("hsv", hsv) 
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8") 
        upper = np.array(upper, dtype = "uint8") 
        
    # 对图片进行二值化处理
    mask = cv2.inRange(hsv, lower, upper)
    #腐蚀操作
    mask = cv2.erode(mask, None, iterations=2)
    #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)    
    #mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    #轮廓检测
    cnts= cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if imutils.is_cv2():
        cnts = cnts[0]
    else:
        cnts = cnts[1]
        center = None   #初始化轮廓质心
    
    #如果存在轮廓
    if len(cnts)>0:
        #找到面积最大的轮廓
        c=max(cnts,key = cv2.contourArea)

        # 外接矩形,始终水平
        cnt = c
        x, y, w, h = cv2.boundingRect(cnt)            # x,y=图像左上方坐标, w,h=宽和高
        origin_pic = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)   # 用绿色(0, 255, 0)来画出最小的矩形框架

        # 外接最小矩形
        rect = cv2.minAreaRect(c)                     #rect:元组，[0]是中心坐标，[1]长宽，[2]角度
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)   # 用红色表示有旋转角度的矩形框架
        theta = round(rect[2])
        cood_x = round(rect[0][0]) 
        cood_y = round(rect[0][1]) 
        print("角度:%d" % theta)

        print("目标像素坐标:%s,%s" %rect[0])
 
        cv2.imshow("frame", frame) 
        if cv2.waitKey(1) ==27 :
            camera.release() 
            cv2.destroyAllWindows() 
  
import cv2
import numpy as np #导入库
blue_lower = np.array([100,43,46])
blue_upper = np.array([124,255,255]) #设置颜色区间
cap = cv2.VideoCapture(0)  #打开摄像头
cap.set(3,640)
cap.set(4,480)  #设置窗口的大小
while 1: #进入无线循环
    ret,frame = cap.read() #将摄像头拍摄到的画面作为frame的值
    frame = cv2.GaussianBlur(frame,(5,5),0) #高斯滤波GaussianBlur() 让图片模糊
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #将图片的色域转换为HSV的样式 以便检测
    mask = cv2.inRange(hsv,blue_lower,blue_upper)  #设置阈值，去除背景 保留所设置的颜色

    mask = cv2.erode(mask,None,iterations=2) #显示腐蚀后的图像
    mask = cv2.GaussianBlur(mask,(3,3),0) #高斯模糊
    res = cv2.bitwise_and(frame,frame,mask=mask) #图像合并

    cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] #边缘检测

    if len(cnts) >0 : #通过边缘检测来确定所识别物体的位置信息得到相对坐标
        cnt = max(cnts,key=cv2.contourArea)
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),2) #画出一个圆
        print(int(x),int(y))
    else:
        pass
    cv2.imshow('frame',frame) #将具体的测试效果显示出来
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    if cv2.waitKey(5) & 0xFF == 27: #如果按了ESC就退出 当然也可以自己设置
        break

cap.release()
cv2.destroyAllWindows() #后面两句是常规操作,每次使用摄像头都需要这样设置一波

