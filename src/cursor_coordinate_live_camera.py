import cv2
import pyautogui

# Initialize the camera feed
camera = cv2.VideoCapture(0)

# Set camera resolution (optional)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Read frame from the camera
    ret, frame = camera.read()
    if not ret:
        break
    
    # Flip frame for a mirrored view (optional)
    frame = cv2.flip(frame, 1)
    
    # Get mouse position
    mouse_x, mouse_y = pyautogui.position()
    
    # Overlay the mouse position on the video feed
    cv2.circle(frame, (mouse_x, mouse_y), 2, (0, 0, 255), -1)
    
    		# draw crosshairs
    cv2.line(frame,(mouse_x,mouse_y+20), (mouse_x,mouse_y-20),(255,255,255),2) #vline
    cv2.line(frame,(mouse_x+20,mouse_y), (mouse_x-20,mouse_y),(255,255,255),2) #hline
    cv2.line(frame,(mouse_x,mouse_y+20), (mouse_x,mouse_y-20),(0,0,0),1) #vline
    cv2.line(frame,(mouse_x+20,mouse_y), (mouse_x-20,mouse_y),(0,0,0),1) #hline
		
    cv2.putText(frame, f"{mouse_x}, {mouse_y}", (mouse_x+10, mouse_y-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Display the video feed
    cv2.imshow("Live Camera Feed with Mouse Pointer", frame)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()

