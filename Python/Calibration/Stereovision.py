import numpy as np
import cv2

kalib_data = cv2.FileStorage('stereoMap.xml', cv2.FILE_STORAGE_READ)

stereoMapL_x = kalib_data.getNode('stereoMapL_x').mat()
stereoMapL_y = kalib_data.getNode('stereoMapL_y').mat()
stereoMapR_x = kalib_data.getNode('stereoMapR_x').mat()
stereoMapR_y = kalib_data.getNode('stereoMapR_y').mat()

kalib_data.release()

right_cam = cv2.VideoCapture(2)#, cv2.CAP_DSHOW) # Right camera
if not right_cam.isOpened():
    print("Error: Could not open right camera.")
    exit()

right_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
right_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

left_cam = cv2.VideoCapture(0)#, cv2.CAP_DSHOW) # Left camera
if not left_cam.isOpened():
    print("Error: Could not open left camera.")
    exit()

left_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
left_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    right_success, right_frame = right_cam.read()
    left_success, left_frame = left_cam.read()

    if not right_success or not left_success:
        print("Error: Failed to retrieve frames from cameras.")
        break

    right_frame = cv2.remap(right_frame, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    left_frame = cv2.remap(left_frame, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    cv2.imshow('Right camera', right_frame)
    cv2.imshow('Left camera', left_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

right_cam.release()
left_cam.release()
cv2.destroyAllWindows()
