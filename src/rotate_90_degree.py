#!/usr/bin/env python3
import cv2
import numpy as np
import pyautogui

# Initialize video
dev = 0
cap = cv2.VideoCapture('/dev/video' + str(dev), cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
cv2.namedWindow('Thermal', cv2.WINDOW_GUI_NORMAL)
width = 256 #Sensor width
height = 192 #sensor height
scale = 3 #scale multiplier
newWidth = width*scale 
newHeight = height*scale
alpha = 1.0 

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from camera")
        break

    print("Frame shape:", frame.shape)
    imdata, thdata = np.array_split(frame, 2, axis=0)
    print("imdata shape:", imdata.shape)
    bgr = cv2.cvtColor(imdata, cv2.COLOR_YUV2BGR_YUYV)
    bgr = cv2.convertScaleAbs(bgr, alpha=alpha)
    bgr = cv2.resize(bgr, (newWidth, newHeight), interpolation=cv2.INTER_CUBIC)  # Scale up!
    heatmap = cv2.applyColorMap(bgr, cv2.COLORMAP_JET)
    
    # Rotate heatmap
    height1, width1, _ = heatmap.shape
    cr = (width1 / 2, height1 / 2)
    M = cv2.getRotationMatrix2D(cr, 90, 1)
    rotated_heatmap = cv2.warpAffine(heatmap, M, (width1, height1))
    
    # Display the rotated heatmap
    cv2.imshow('Thermal', rotated_heatmap)
    keyPress = cv2.waitKey(1)
    if keyPress == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


