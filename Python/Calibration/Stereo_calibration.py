import cv2
import numpy as np
import glob
############### Finne og kjenne igjen hjørnene på sjakkbrettet #####################

chessboardSize = (9,6)
frameSize = (640, 480)

## Kriterier ##

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30 , 0.001)

# Forberede objekt pointere, som (0,0,0), (1,0,0) osv...
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0 : chessboardSize[0], 0:[chessboardSize[1]]].T.reshape[-1,2]

objp = objp * 20
print(objp)

#Array for å lagre objekt punkter og bilde punkter fra alle bildene.
objpoints = []
imgpointsL = []
imgpointsR = []

imagesLeft = glob.glob('images/LeftStereo/*.png')
imagesRight = glob.glob('images/RightStereo/*.png')

for imgLeft, imgRight, in zip(imagesLeft, imagesRight):
    imgL = cv2.imread(imgLeft)
    imgR = cv2.imread(imgRight)

    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    # Nå skal koden finne hjørnene i sjakkmønsteret
    retL = cornersL = cv2.findChessboardCorners(grayL, chessboardSize, None)
    retR = cornersR = cv2.findChessboardCorners(grayR, chessboardSize, None)

    if retL and retR == True:

        objpoints.append(objp)

        cornersL = cv2.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
        imgpointsL.append(cornersL)

        cornersR = cv2.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)
        imgpointsR.append(cornersR)

        # Tegn og vis alle hjørner

        cv2.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
        cv2.imshow('Venstre', imgL)
        cv2.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
        cv2.imshow('Høyre', imgR)
        cv2.waitKey(1000)

cv2.destroyAllWindows

#!# Kalibrering kameraer#!#

retL, cameraMatrixL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, frameSize, None, None,)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, frameSize, None, None,)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv2.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

#!# Stereoskopi Kalibrering #!#

flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
# Setter opp kamera matrise så bare Rot, Trns, Emat og Fmat er kalkulert.

criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2. TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Dette steget blir gjennomført for å transformere mellom kameraene og kalkulere Essenstiell og Fundamentale

retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(objpoints, imgpointsL, 
            imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1],
            criteria=criteria_stereo, flags=flags)


#!# Stereo Gjennoppretting #!#

rectifyScale = 1
rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv2.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, 
            grayL.shape[::-1], rot, trans, rectifyScale, (0,0))

stereoMapL = cv2.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv2.CV_16SC2)
stereoMapR = cv2.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv2.CV_16SC2)

print("Lagrer Data!")

kalib_data = cv2.FileStorage('stereoMap.xml', cv2.FILE_STORAGE_WRITE)

kalib_data.write('stereoMapL_x', stereoMapL[0])
kalib_data.write('stereoMapL_y', stereoMapL[1])
kalib_data.write('stereoMapR_x', stereoMapL[0])
kalib_data.write('stereoMapR_y', stereoMapL[1])

kalib_data.release()

