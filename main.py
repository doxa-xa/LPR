import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

# the following code reads an image of car with a licenceplate focuses on it and translates it to string
# it prints the string to console 

img = cv2.imread('./static/image1.jpg')
gray = cv2.cvtColor(img, COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

# applying filters for noise reduction & edges capture
bfilter = cv2.bileteralFilter(gray, 11, 17, 17)
edged = cv2.Canny(bfilter, 30, 200)
plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

# detecting contour
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.coutourArea, reverse=True)[:10]

# apply mask to the desired contour
location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break
print(location)

mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0, 255, -1)
new_image = cv2.bitwise_and(img,img,mask=mask)
plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

# cropping the licence plate
(x, y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2+1, y1:y2+1]
plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

# reading the licence plate from an image
reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)
print(result)