import cv2
import sys
import time
import face_detection as fd


def get_image():
    camera_id=1
    delay=1
    window_name='frame'

    cap=cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        sys.exit()

    while True:
        ret,frame=cap.read()
        #frame=fd.face_detection(frame)
        cv2.imshow(window_name,frame)
        if cv2.waitKey(delay)&0xFF==ord('q'):
            break

    cv2.destroyWindow(window_name)

#とりあえず実行
get_image()
