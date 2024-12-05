#!/usr/bin/env python3
import cv2
import numpy as np
import argparse
import time
import io
parser = argparse.ArgumentParser()
parser.add_argument("--device", type=int, default=0, help="Video Device number e.g. 0, use v4l2-ctl --list-devices")
args = parser.parse_args()
	
if args.device:
	dev = args.device
else:
	dev = 0
	
#init video
cap = cv2.VideoCapture('/dev/video'+str(dev), cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

#256x192 General settings
width = 256 #Sensor width
height = 192 #sensor height
scale = 5 #scale multiplier
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

		#grab data from the center pixel...
		x_pixel = 128
		y_pixel = 96
		hi = thdata[96][128][0]
		lo = thdata[96][128][1]
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
		
		#show temp
		cv2.putText(heatmap,str(temp)+' C', (int(newWidth/2)+10, int(newHeight/2)-10),\
		cv2.FONT_HERSHEY_SIMPLEX, 0.45,(0, 255, 255), 1, cv2.LINE_AA)

		#display image
		cv2.imshow('Thermal',heatmap)
		keyPress = cv2.waitKey(1)
		if keyPress == ord('q'):
			break
			capture.release()
			cv2.destroyAllWindows()
		
