import cv2 

cap = cv2.VideoCapture(0)

# wait for 1 second

cv2.waitKey(1000)

ret , bilde = cap.read()

gray = cv2.cvtColor(bilde, cv2.COLOR_BGR2GRAY)

_ ,tresh  = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

cv2.imshow('Bilde', tresh)

ret , corners = cv2.findChessboardCorners(gray, (8,5), None)

print(ret)

cv2.imshow('Bilde', tresh)

cv2.waitKey(0)

cv2.destroyAllWindows()