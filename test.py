import cv2
import numpy as np

# カレンダー
img = cv2.imread("test1.jpg")
b, g, r = cv2.split(img)
cv2.imwrite("b.jpg",b)
cv2.imwrite("g.jpg",g)
cv2.imwrite("r.jpg",r)

_, mask_b_img = cv2.threshold(b, 130, 255, cv2.THRESH_BINARY_INV)
_, mask_g_img = cv2.threshold(g, 130, 255, cv2.THRESH_BINARY)
except_b_img = cv2.bitwise_and(img, img, mask=mask_b_img)
except_g_img = cv2.bitwise_and(except_b_img, except_b_img, mask=mask_g_img)
cv2.imwrite("b except1.jpg",except_g_img)

gray = cv2.cvtColor(except_g_img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("calendar_mod.png", gray)
contours, hierarchy= cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
areas = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 10000:
        epsilon = 0.1*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        areas.append(approx)

cv2.drawContours(img,areas,-1,(0,255,0),3)
display_cv_image(img)