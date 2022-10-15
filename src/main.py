import cv2                    # 匯入 OpenCV 函式庫
img = cv2.imread('meme.jpg')  # 讀取圖片
x = 0
y = 0
w = 400
h = 400
resizeimg = cv2.resize(img, (400, 400))   # 產生 400x400 的圖

# crop_img = img[y:y+h, x:x+w]        # 取出陣列的範圍
# cv2.imwrite('output.jpg', crop_img) # 儲存圖片

cv2.imshow('Square_Size',resizeimg)        # 賦予開啟的視窗名稱，開啟圖片
output1 = cv2.blur(resizeimg, (5, 5))     # 指定區域單位為 (5, 5)
output1 = cv2.GaussianBlur(resizeimg, (5, 5),0)
output2 = cv2.blur(resizeimg, (25, 25))   # 指定區域單位為 (25, 25)

cv2.imshow('Normal blur', output1)
cv2.imshow('G blur', output2)
cv2.waitKey(0)                # 設定 0 表示不要主動關閉視窗