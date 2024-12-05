#!/usr/bin/env python3
import cv2
import numpy as np
import argparse
import time
import io
import pyautogui
dev = 0
#init video
cap = cv2.VideoCapture('/dev/video'+str(dev), cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

#256x192 General settings
width = 256 #Sensor width
height = 192 #sensor height
scale = 1 #scale multiplier
newWidth = width*scale 
newHeight = height*scale
alpha = 1.0 # Contrast control (1.0-3.0)
colormap = 0
font=cv2.FONT_HERSHEY_SIMPLEX
dispFullscreen = False
cv2.namedWindow('Thermal',cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow('Thermal', newWidth,newHeight)
rad = 0 #blur radius
threshold = 2
hud = True
recording = False
elapsed = "00:00:00"
snaptime = "None"

while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read()
	if ret == True:
		imdata,thdata = np.array_split(frame, 2)

		#grab data from the mouse position...
		mouse_x, mouse_y = pyautogui.position()
		hi = thdata[mouse_y][mouse_x][0]
		lo = thdata[mouse_y][mouse_x][1]
		#print(hi,lo)
		lo = lo*256
		rawtemp = hi+lo
		#print(rawtemp)
		temp = (rawtemp/64)-273.15
		temp = round(temp,2)
		# Convert the real image to RGB
		bgr = cv2.cvtColor(imdata,  cv2.COLOR_YUV2BGR_YUYV)
		#Contrast
		bgr = cv2.convertScaleAbs(bgr, alpha=alpha)#Contrast
		#bicubic interpolate, upscale and blur
		bgr = cv2.resize(bgr,(newWidth,newHeight),interpolation=cv2.INTER_CUBIC)#Scale up!
		if rad>0:
			bgr = cv2.blur(bgr,(rad,rad))

		heatmap = cv2.applyColorMap(bgr, cv2.COLORMAP_JET)
		
		# draw crosshairs
		cv2.line(heatmap,(mouse_x,mouse_y+20), (mouse_x,mouse_y-20),(255,255,255),2) #vline
		cv2.line(heatmap,(mouse_x+20,mouse_y), (mouse_x-20,mouse_y),(255,255,255),2) #hline
		cv2.line(heatmap,(mouse_x,mouse_y+20), (mouse_x,mouse_y-20),(0,0,0),1) #vline
		cv2.line(heatmap,(mouse_x+20,mouse_y), (mouse_x-20,mouse_y),(0,0,0),1) #hline
    				
		#show temp
		cv2.putText(heatmap,str(temp)+' C', (mouse_x+10, mouse_y-10),\
		cv2.FONT_HERSHEY_SIMPLEX, 0.45,(0, 255, 255), 1, cv2.LINE_AA)

		#display image
		cv2.imshow('Thermal',heatmap)
		keyPress = cv2.waitKey(1)
		if keyPress == ord('q'):
			break
			capture.release()
			cv2.destroyAllWindows()
		
