import cv2
import numpy as np

# カレンダー
original_img = cv2.imread("test3.jpg")
size = original_img.shape[0] * original_img.shape[1]
img = cv2.cvtColor(original_img, cv2.COLOR_BGR2HLS)
img[10>img[:,:,0]]= 0
img[90<img[:,:,0]]= 0
cv2.imwrite("calendar_mod.png", img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("waowao.jpg" , gray)
contours, hierarchy = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
max_area = 10000000
approxs = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    print(area)
    epsilon = 0.1 * cv2.arcLength(cnt, True)
    tmp = cv2.approxPolyDP(cnt, epsilon, True)
    if 4 == len(tmp):
        approxs.append(tmp)
        if size * 0.01 <= area\
            and area <= size * 0.99\
            and max_area > area:
            print("waawawaaaa--")
            print(size * 0.01)
            best_approx = tmp
            max_area = area
r_btm = best_approx[0][0]
r_top = best_approx[1][0]
l_top = best_approx[2][0]
l_btm = best_approx[3][0]
top_line   = (abs(r_top[0] - l_top[0]) ^ 2) + (abs(r_top[1] - l_top[1]) ^ 2)
btm_line   = (abs(r_btm[0] - l_btm[0]) ^ 2) + (abs(r_btm[1] - l_btm[1]) ^ 2)
left_line  = (abs(l_top[0] - l_btm[0]) ^ 2) + (abs(l_top[1] - l_btm[1]) ^ 2)
right_line = (abs(r_top[0] - r_btm[0]) ^ 2) + (abs(r_top[1] - r_btm[1]) ^ 2)
max_x = top_line  if top_line  > btm_line   else btm_line
max_y = left_line if left_line > right_line else right_line
# 画像の座標上から4角を切り出す
pts1 = np.float32(best_approx)
pts2 = np.float32([[max_x, max_y], [max_x, 0], [0, 0], [0, max_y]])

# 透視変換の行列を求める
M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(original_img, M, (max_x, max_y))
cv2.imwrite("unchi.jpg" , dst)