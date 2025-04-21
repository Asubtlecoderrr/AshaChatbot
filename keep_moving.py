import pyautogui
import time

print("Mouse mover started. Press Ctrl+C to stop.")

try:
    while True:
        pyautogui.moveRel(10, 0, duration=0.1)  # Move right by 1 pixel
        pyautogui.moveRel(-10, 0, duration=0.1) # Move back to original position
        time.sleep(10)  # Wait 10 seconds before next move (adjust as needed)
except KeyboardInterrupt:
    print("Mouse mover stopped.")
