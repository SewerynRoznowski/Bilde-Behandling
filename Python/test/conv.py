import cv2 

img = cv2.imread('Python/test/ImageR4.png')
img2 = cv2.imread('Python/test/ImageR5.png')

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

cv2.imwrite('Python/test/test1.png', img)
cv2.imwrite('Python/test/test2.png', img2)

