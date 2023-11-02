import cv2

class StereoCameraCapture:
    def __init__(self):
        # Initialize the left and right camera capture objects
        self.cap1 = cv2.VideoCapture(0)
        self.cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.cap2 = cv2.VideoCapture(2)
        self.cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.num = 0

    def capture_images(self):
        while self.cap1.isOpened():
            success1, img1 = self.cap1.read()  # img1 is the left camera
            success2, img2 = self.cap2.read()  # img2 is the right camera

            k = cv2.waitKey(5)

            if k == 27:
                break
            elif k == ord('s'):  # Wait for 's' key to save and exit.

                test = cv2.imwrite('Python/Calibration/images/LeftStereo/ImageL' + str(self.num) + '.png', img1)
                test1 = cv2.imwrite('Python/Calibration/images/RightStereo/ImageR' + str(self.num) + '.png', img2)
                if test == True and test1 == True:
                    print('Images saved!')
                self.num += 1

            cv2.imshow('Left image', img1)
            cv2.imshow('Right image', img2)

    def release_cameras(self):
        # Release camera objects when done
        self.cap1.release()
        self.cap2.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    stereo_capture = StereoCameraCapture()
    stereo_capture.capture_images()
    stereo_capture.release_cameras()
