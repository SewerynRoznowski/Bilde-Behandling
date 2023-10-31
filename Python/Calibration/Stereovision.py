import numpy as np
import cv2

kalib_data = cv2.FileStorage()
kalib_data.open('stereoMap.xml', cv2.FILE_STORAGE_READ)

stereoMapL_x = kalib_data.getNode('stereoMapL_x').map()
stereoMapL_y = kalib_data.getNode('stereoMapL_y').map()
stereoMapR_x = kalib_data.getNode('stereoMapR_x').map()
stereoMapR_y = kalib_data.getNode('stereoMapR_y').map()

# Åpne begge kameraene

rigth_cam = cv2.VideoCapture(2, cv2.CAP_DSHOW) # Høyre kamera
left_cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Venstre kamera

while(rigth_cam.isOpened() and left_cam.isOpened()):

    right_succes, right_frame = rigth_cam.read()
    left_succes, left_frame = left_cam.read()

    #Uforvrengt og gjennopprettet bilde

    right_frame =cv2.remap(right_frame, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    left_frame =cv2.remap(left_frame, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    # Åpner begge kameraene
    cv2.imshow('Høyre kamera', right_frame)
    cv2.imshow('Venstre kamera', left_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

rigth_cam.release()
left_cam.release()

cv2.destroyAllWindows()