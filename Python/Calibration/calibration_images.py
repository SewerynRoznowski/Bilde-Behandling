import cv2

#cap1 is videocapture(0), cap2 is videocapture(2), this may differ from computer and port layout!
capL = cv2.VideoCapture(0)
capL.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

capR = cv2.VideoCapture(2)
capR.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

num = 0

while capL.isOpened():

    succes1, imgL = capL.read() #img1 is Left camera
    succes2, imgR = capR.read() #img2 is Right camera

    k = cv2.waitKey(5)

    if k ==27:
        break
    elif k == ord('s'): # Wait for 's' key to save and exit.
        
        testL = cv2.imwrite('Python/Calibration/images/LeftStereo/ImageL' +str(num) + '.png', imgL)
        testR = cv2.imwrite('Python/Calibration/images/RightStereo/ImageR' +str(num) + '.png', imgR)
        if testL == True and testR == True:
            print('Images saved!')
        num += 1


    cv2.imshow('imageL', imgL)
    cv2.imshow('imageR', imgR)