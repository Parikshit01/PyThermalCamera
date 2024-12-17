import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

# Global variables
drawing = False
ix, iy = -1, -1
rectangle = None

# Lists to store time, max temp, and min temp values for plotting
time_values = []
maxtemp_values = []
mintemp_values = []

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

# Sensor properties
width = 256  # Sensor width
height = 192  # Sensor height
scale = 5  # Scale multiplier
newWidth = width * scale
newHeight = height * scale
alpha = 1.0

if not cap.isOpened():
    print("Error: Unable to open video capture.")
    exit()

cv2.namedWindow("Live Feed")
cv2.setMouseCallback("Live Feed", draw_rectangle)

# Start time to record the time elapsed
start_time = time.time()

# Set up the plot
plt.ion()  # Turn on interactive mode for real-time plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Max and Min Temperatures Over Time")
line_max, = ax.plot([], [], label="Max Temperature (°C)", color='b')
line_min, = ax.plot([], [], label="Min Temperature (°C)", color='r')
ax.grid(True)
ax.legend()

# Function to update the plot
def update_plot():
    line_max.set_data(time_values, maxtemp_values)
    line_min.set_data(time_values, mintemp_values)
    ax.relim()  # Recalculate limits
    ax.autoscale_view()  # Automatically scale view
    plt.draw()
    plt.pause(0.1)  # Pause to allow the plot to update

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # Split the frame into imdata and thdata
    imdata, thdata = np.array_split(frame, 2, axis=0)

    # Convert and process imdata
    bgr = cv2.cvtColor(imdata, cv2.COLOR_YUV2BGR_YUYV)
    bgr = cv2.convertScaleAbs(bgr, alpha=alpha)
    bgr = cv2.resize(bgr, (newWidth, newHeight), interpolation=cv2.INTER_CUBIC)
    heatmap = cv2.applyColorMap(bgr, cv2.COLORMAP_JET)

    # If rectangle is drawn, calculate temperatures
    if rectangle:
        x1, y1, x2, y2 = rectangle
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        # Ensure rectangle coordinates are valid within scaled frame dimensions
        x1 = max(0, min(x1, newWidth - 1))
        x2 = max(0, min(x2, newWidth - 1))
        y1 = max(0, min(y1, newHeight - 1))
        y2 = max(0, min(y2, newHeight - 1))

        if x2 > x1 and y2 > y1:
            cv2.rectangle(heatmap, (x1, y1), (x2, y2), (0, 0, 0), 2)

            # Scale back coordinates for cropping the original image (before resizing)
            orig_x1 = int(x1 / scale)
            orig_y1 = int(y1 / scale)
            orig_x2 = int(x2 / scale)
            orig_y2 = int(y2 / scale)

            # Crop the region from thdata (original resolution)
            cropped_image = thdata[orig_y1:orig_y2, orig_x1:orig_x2]

            if cropped_image.size > 0 and cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
                # Max temperature calculation
                lomax = cropped_image[..., 1].max()
                posmax = cropped_image[..., 1].argmax()
                maxcol, maxrow = divmod(posmax, cropped_image.shape[1])
                himax = cropped_image[maxcol, maxrow][0]
                lomax = lomax * 256
                maxtemp = himax + lomax
                maxtemp = (maxtemp / 64) - 273.15
                maxtemp = round(maxtemp, 2)

                # Min temperature calculation
                lomin = cropped_image[..., 1].min()
                posmin = cropped_image[..., 1].argmin()
                mincol, minrow = divmod(posmin, cropped_image.shape[1])
                himin = cropped_image[mincol, minrow][0]
                lomin = lomin * 256
                mintemp = himin + lomin
                mintemp = (mintemp / 64) - 273.15
                mintemp = round(mintemp, 2)

                # Print debugging info
                print(f"Max Temp: {maxtemp}C, Min Temp: {mintemp}C")
                
                # Store time, max temp, and min temp
                elapsed_time = time.time() - start_time
                time_values.append(elapsed_time)
                maxtemp_values.append(maxtemp)
                mintemp_values.append(mintemp)
                
                # Display temperatures
                cv2.putText(heatmap, f"Max: {maxtemp}C, Min: {mintemp}C",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                # Update the plot
                update_plot()

    # Show the live feed with heatmap and temp info
    cv2.imshow("Live Feed", heatmap)

    # Press 'q' to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# After exiting the loop, keep the plot displayed
plt.ioff()  # Turn off interactive mode
plt.show()

cap.release()
cv2.destroyAllWindows()

