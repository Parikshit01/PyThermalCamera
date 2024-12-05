import cv2

# Initialize global variables
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial position
rectangle = None  # To store the rectangle coordinates

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rectangle

    # Mouse press event
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # Mouse movement event
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            rectangle = (ix, iy, x, y)

    # Mouse release event
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rectangle = (ix, iy, x, y)

# Start capturing video
cap = cv2.VideoCapture(0)

# Set mouse callback for drawing
cv2.namedWindow("Live Feed")
cv2.setMouseCallback("Live Feed", draw_rectangle)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # If a rectangle is being drawn or exists
    if rectangle:
        x1, y1, x2, y2 = rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Calculate and display the centroid
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv2.putText(frame, f"Centroid: ({cx}, {cy})", (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Display the live feed
    cv2.imshow("Live Feed", frame)

    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()

