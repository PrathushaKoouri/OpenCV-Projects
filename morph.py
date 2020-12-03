
#invisibility cloak using OpenCV python
import cv2
import time
import numpy as np
## Preparation for writing the ouput video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
##reading from the webcam
cap = cv2.VideoCapture(0)
## Allow the system to sleep for 3 seconds before the webcam starts
time.sleep(3)
count = 0
bg = 0
## Capture the background in range of 60
for i in range(60):
    ret, bg = cap.read()
bg = np.flip(bg, axis=1)
## Read every frame from the webcam, until the camera is open
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    frame = np.flip(frame, axis=1)
    ## Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ## Generate masks to detect red color
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(frame, frame, mask=mask2)
    res2 = cv2.bitwise_and(bg, bg, mask=mask1)
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
    out.write(finalOutput)
    cv2.imshow("magic", finalOutput)
    cv2.waitKey(1)
cap.release()
out.release()
cv2.destroyAllWindows()
