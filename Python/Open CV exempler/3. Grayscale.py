# import moduler
import cv2

# definer webcam objektet
cap = cv2.VideoCapture(0)

# Vis bilde i santid
while(True):
    # les inn bilde fra webcam
    ret, bilde = cap.read()

    # Coverter til grayscale
    gray = cv2.cvtColor(bilde, cv2.COLOR_BGR2GRAY)

    # vis bilde
    cv2.imshow('Bilde', gray)
    # vent på at bruker trykker en tast
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# lukk vinduer

cv2.destroyAllWindows()

# frigi webcam
cap.release()