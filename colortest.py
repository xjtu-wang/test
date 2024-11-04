import cv2
import numpy as np

# 定义全局变量用于存储当前RGB值
current_rgb = (0, 0, 0)
lower_purple = np.array([0,0, 0])
upper_purple = np.array([150, 255, 255])
blob_threshold_black_low = (0, 0, 0)
blob_threshold_black_high = (180, 255, 30)

blob_threshold_blue_low = (100, 150, 50)
blob_threshold_blue_high = (144, 255, 255)

blob_threshold_red_low = (120, 50, 50)
blob_threshold_red_high = (180, 255, 255)

blob_threshold_purple_low = (130, 50, 50)
blob_threshold_purple_high = (180, 255, 255)

blob_threshold_yellow_low = (10, 90, 50)
blob_threshold_yellow_high = (80, 255, 255)

blob_threshold_brown_low = (150, 50, 50)
blob_threshold_brown_high = (180, 255, 255)
# 打开摄像头
cap = cv2.VideoCapture(0)


while True:
    # 读取一帧图像
    ret, frame = cap.read()
    if not ret:
        break
    # 将图像转换为HSV颜色空间
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img_gaus = cv2.GaussianBlur(img_hsv, (7, 7), 1.5)
    mask = cv2.inRange(img_gaus, blob_threshold_purple_low, blob_threshold_purple_high)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    threshold_area = 800
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > threshold_area:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            print("see color")
    cv2.imshow("frame", frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    dst = cv2.dilate(dst, None, iterations=2)
    cv2.imshow("third", dst)

    color = dst[200]
    color2 = dst[230]

    white_count = np.sum(color == 255)
    white_count2 = np.sum(color2 == 255)

    white_index = np.where(color == 255)
    white_index2 = np.where(color2 == 255)

    if white_count == 0 and white_count2 == 0:
        center = 320
        center2 = 320

    elif white_count2 == 0 and white_count != 0:
        center2 = 640
        center = (white_index[0][white_count - 1] + white_index[0][0]) / 2

    elif white_count2 != 0 and white_count == 0:
        center = 640
        center2 = (white_index2[0][white_count2 - 1] + white_index2[0][0]) / 2

    else:
        center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
        center2 = (white_index2[0][white_count2 - 1] + white_index2[0][0]) / 2

    cv2.rectangle(frame, (0, 195), (640, 205), (255, 0, 0), thickness=2)
    cv2.rectangle(frame, (0, 215), (640, 225), (255, 0, 0), thickness=2)

    cv2.imshow("frame", frame)

    direction = 0
    if abs(center - 320) > abs(center2 - 320):
        direction = center2 - 320
    else:
        direction = center - 320

        print("direction = ", direction)

        if direction >= 40:
            if direction > 40:
                direction = 40
                print("right1")
                stop = 0
                go_straight = 0
                turn_right = 1
                turn_left = 0
                upstairs = 0
                

        elif direction < -40:
            if direction < -40:
                direction = -40
                print("left1")
                stop = 0
                go_straight = 0
                turn_right = 0
                turn_left = 1
                upstairs = 0
                

        else:
            print("straight1")
            stop = 0
            go_straight = 1
            turn_right = 0
            turn_left = 0
            upstairs = 0
            

        # time.sleep(0.6)
    # 按下ESC键退出循环
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
