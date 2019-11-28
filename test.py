import cv2
import numpy as np

# カレンダー
img = cv2.imread("test3.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
img[20>img[:,:,0]]= 0
img[70<img[:,:,0]]= 0
cv2.imwrite("calendar_mod.png", img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("waowao.jpg" , gray)
contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_canny = cv2.Canny(gray, 30, 400)
cv2.imwrite('chirsuta.canny.jpg', img_canny)