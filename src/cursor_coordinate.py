import pyautogui
from pynput import mouse

# Function to execute when the mouse moves
def on_move(x, y):
    print(f"Mouse moved to ({x}, {y})")

# Set up a listener for mouse events
with mouse.Listener(on_move=on_move) as listener:
    listener.join()

