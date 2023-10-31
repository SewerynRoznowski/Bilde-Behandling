import cv2
import numpy as np
import glob

############### Finne og kjenne igjen hjørnene på sjakkbrettet #####################

chessboardsize = (9,6)
frameSize = (640, 480)

## Kriterier ##

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30 , 0.001)

# Forberede objekt pointere, som (0,0,0), (1,0,0) osv...
objp = np.zeros((chessboardsize[0] * chessboardsize[1], 3), np.float32)