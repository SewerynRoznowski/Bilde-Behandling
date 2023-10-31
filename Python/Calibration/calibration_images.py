import cv2

#cap1 is videocapture(0), cap2 is videocapture(2), this may differ from computer and port layout!
cap1 = cv2.VideoCapture(0)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cap2 = cv2.VideoCapture(2)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

num = 0

while cap1.isOpened():

    succes1, img1 = cap1.read() #img1 is Left camera
    succes2, img2 = cap2.read() #img2 is Right camera

    k = cv2.waitKey(5)

    if k ==27:
        break
    elif k == ord('s'): # Wait for 's' key to save and exit.
        
        test = cv2.imwrite('Python/Calibration/images/LeftStereo/ImageL' +str(num) + '.png', img1)
        test1 = cv2.imwrite('Python/Calibration/images/RightStereo/ImageR' +str(num) + '.png', img2)
        if test == True and test1 == True:
            print('Images saved!')
        num += 1


    cv2.imshow('Left image', img1)
    cv2.imshow('Right image', img2)