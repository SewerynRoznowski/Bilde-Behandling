import cv2 

# definer webcam objektet (Har du flere webcams kan du velge hvilket du vil bruke)
# 0 er som regel er det den som er innebygd i pcen
# Det er bare å endre på tallet til du finner en som funker
cap = cv2.VideoCapture(0)

# Hvis du får en svart bilde, prøv å vent litt
# Det skjer noen ganger at det tar litt tid før webcam starter
# cv2.waitKey(1000)

# les inn bilde fra webcam
ret, bilde = cap.read()

# vis bilde
cv2.imshow('Bilde', bilde)

# vent på at bruker trykker en tast
cv2.waitKey(0)

# lukk vinduer
cv2.destroyAllWindows()

# frigi webcam (Den er viktig å kjøre denne når du er ferdig med å bruke webcam)
cap.release()