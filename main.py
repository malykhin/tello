import time
import cv2

from tello import Tello

drone = Tello()

while True:
    if drone.is_new_frame_ready():
        frame = drone.get_last_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 30, 150)
        cv2.imshow('image', edged)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

cv2.destroyAllWindows()
