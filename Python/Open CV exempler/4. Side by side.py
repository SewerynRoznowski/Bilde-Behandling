# import moduler 
import cv2

# definer webcam objektet
cap = cv2.VideoCapture(0)

# Vis bilde i santid

while(True):
    # les inn bilde fra webcam
    ret, bilde = cap.read()

    # sjekk om bilde ble lest inn
    if not ret:
        print('Kunne ikke lese bilde fra webcam')
        break

    # Coverter til grayscale
    gray = cv2.cvtColor(bilde, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # sjekk om bilde og gray er like store
    print(bilde.shape)
    print(gray.shape)

    # slå sammen bildene
    concatenated = cv2.hconcat([bilde, gray])

    # vis bilde
    cv2.imshow('Bilde', concatenated)
    # vent på at bruker trykker en tast
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# lukk vinduer
cv2.destroyAllWindows()

# frigi webcam
cap.release()