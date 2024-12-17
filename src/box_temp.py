import cv2
import numpy as np
import pyautogui

# Global variables
drawing = False
ix, iy = -1, -1
rectangle = None

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rectangle

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            rectangle = (ix, iy, x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rectangle = (ix, iy, x, y)

dev = 0
cap = cv2.VideoCapture('/dev/video' + str(dev), cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
width = 256 #Sensor width
height = 192 #sensor height
scale = 5 #scale multiplier
newWidth = width*scale 
newHeight = height*scale
alpha = 1.0 

if not cap.isOpened():
    print("Error: Unable to open video capture.")
    exit()

cv2.namedWindow("Live Feed")
cv2.setMouseCallback("Live Feed", draw_rectangle)


while cap.isOpened():
    ret, frame = cap.read()
    imdata, thdata = np.array_split(frame, 2, axis=0)
    bgr = cv2.cvtColor(imdata, cv2.COLOR_YUV2BGR_YUYV)
    bgr = cv2.convertScaleAbs(bgr, alpha=alpha)
    bgr = cv2.resize(bgr, (newWidth, newHeight), interpolation=cv2.INTER_CUBIC)  # Scale up!
    heatmap = cv2.applyColorMap(bgr, cv2.COLORMAP_JET)
    if not ret:
        print("Failed to capture frame.")
        break

    if rectangle:
        x1, y1, x2, y2 = rectangle
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        cv2.rectangle(heatmap, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # Crop and process
        cropped_image = thdata[y1:y2, x1:x2]
        lomax = cropped_image[...,1].max()
        posmax = cropped_image[...,1].argmax()
        #since argmax returns a linear index, convert back to row and col
        mcol,mrow = divmod(posmax,width)
        himax = thdata[mcol][mrow][0]
        lomax=lomax*256
        maxtemp = himax+lomax
        maxtemp = (maxtemp/64)-273.15
        maxtemp = round(maxtemp,2)
        cv2.putText(heatmap,'Max Temp:' +str(maxtemp)+'C', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.imshow("Live Feed", heatmap)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
