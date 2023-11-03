import cv2
import numpy as np
import ttkbootstrap as tb

class StereoCameraCapture:
    bildenr = 0

    def capture_images(cls, frameL, frameR):
       
#       while True():
#           k = cv2.waitKey(5)

#            if k == 27: # Press 'ESC' for exit the program
#                return True
#           elif k == ord('s'):  # Wait for 's' key to save and exit.

        test = cv2.imwrite('Python/Calibration/images/LeftStereo/ImageL' + str(cls.bildenr) + '.png', frameL)
        test1 = cv2.imwrite('Python/Calibration/images/RightStereo/ImageR' + str(cls.bildenr) + '.png', frameR)
        if test == True and test1 == True:
            print('Images saved!')
        cls.bildenr += 1


        #if frameL is not None and frameR is not None:
        #   cv2.imshow('Left image', frameL)
        #  cv2.imshow('Right image', frameR)
        
        return False
    


