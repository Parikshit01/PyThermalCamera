#!/usr/bin/env python3
import cv2
import numpy as np
import pyautogui
import time

# Initialize video
cam_left = 4
cap_left = cv2.VideoCapture('/dev/video' + str(cam_left), cv2.CAP_V4L)
cap_left.set(cv2.CAP_PROP_CONVERT_RGB, 0)
cv2.namedWindow('cam_left', cv2.WINDOW_GUI_NORMAL)

cam_right = 0
cap_right = cv2.VideoCapture('/dev/video' + str(cam_right), cv2.CAP_V4L)
cap_right.set(cv2.CAP_PROP_CONVERT_RGB, 0)
cv2.namedWindow('cam_right', cv2.WINDOW_GUI_NORMAL)

width = 256 #Sensor width
height = 192 #sensor height
scale = 4 #scale multiplier
newWidth = width*scale 
newHeight = height*scale
alpha = 1.0 

while cap_left.isOpened() & cap_right.isOpened():
    # Capture frame-by-frame
    ret1, frame_left = cap_left.read()
    imdata_left, thdata_left = np.array_split(frame_left, 2, axis=0)
    bgr_left = cv2.cvtColor(imdata_left, cv2.COLOR_YUV2BGR_YUYV)
    bgr_left = cv2.convertScaleAbs(bgr_left, alpha=alpha)
    bgr_left = cv2.resize(bgr_left, (newWidth, newHeight), interpolation=cv2.INTER_CUBIC)  # Scale up!
    heatmap_left = cv2.applyColorMap(bgr_left, cv2.COLORMAP_JET)
    height1_left, width1_left, _ = heatmap_left.shape
    cr_left = (width1_left / 2, height1_left / 2)
    M_left = cv2.getRotationMatrix2D(cr_left, 270, 1)
    rotated_heatmap_left = cv2.warpAffine(heatmap_left, M_left, (width1_left, height1_left))
    cv2.imshow('cam_left', rotated_heatmap_left)
    
    ret2, frame_right = cap_right.read()
    imdata_right, thdata_right = np.array_split(frame_right, 2, axis=0)
    bgr_right = cv2.cvtColor(imdata_right, cv2.COLOR_YUV2BGR_YUYV)
    bgr_right = cv2.convertScaleAbs(bgr_right, alpha=alpha)
    bgr_right = cv2.resize(bgr_right, (newWidth, newHeight), interpolation=cv2.INTER_CUBIC)  # Scale up!
    heatmap_right = cv2.applyColorMap(bgr_right, cv2.COLORMAP_JET)
    height1_right, width1_right, _ = heatmap_right.shape
    cr_right = (width1_right / 2, height1_right / 2)
    M_right = cv2.getRotationMatrix2D(cr_right, 270, 1)
    rotated_heatmap_right = cv2.warpAffine(heatmap_right, M_right, (width1_right, height1_right))
    cv2.imshow('cam_right', rotated_heatmap_right)

    stereo = cv.StereoBM.create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(rotated_heatmap_left,rotated_heatmap_right)
    cv2.imshow('disparity', disparity)

    
    keyPress = cv2.waitKey(1)
    
    if keyPress == ord('p'):
        cv2.imwrite("heatmap_left.png", rotated_heatmap_left)
        cv2.imwrite("heatmap_right.png", rotated_heatmap_right)		
    if keyPress == ord('q'):
        break

cap_left.release()
cap_right.release()
cv2.destroyAllWindows()


