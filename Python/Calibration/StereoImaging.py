import cv2
import numpy as np

#cap1 is videocapture(0) and Left, cap2 is videocapture(2) and Right, this may differ from computer and port layout!
cap1 = cv2.VideoCapture(0)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap1.set(cv2.CAP_PROP_EXPOSURE, -1)

cap2 = cv2.VideoCapture(2)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap2.set(cv2.CAP_PROP_EXPOSURE, -1)

if not cap1.isOpened() or not cap2.isOpened():
    print("Error: Could not open camera.")

    exit()
while True:
# Caputre frame from camera 1 Left
    ret1, frame1 = cap1.read()
# Capture frame from camera 2 Right
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print('Error: Could  not read one or both frames.')
    #break
    height, width, _ = frame1.shape
    combined_frame = cv2.hconcat([frame1, frame2])

    cv2.namedWindow("Left, Combined Images, Right", cv2.WINDOW_NORMAL)

    cv2.imshow("Left, Combined Images, Right", combined_frame)
   # cv2.imshow("Live Image1", frame1)
   # cv2.imshow("Live Image2", frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cap2.release()

