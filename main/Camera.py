import cv2
import sys
import time
import face_detection as fd
def get_image():
    camera_id=0
    delay=1
    window_name='frame'
    cap=cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        sys.exit()

    while True:
        ret,frame=cap.read()
        #frame=fd.face_detection(frame)
        #frame=cap.read()
       #frame=cv2.resize(frame,(200,100))
        print(frame)
       # cv2.imshow(window_name,frame)
        if cv2.waitKey(delay)&0xFF==ord('q') :
            break
    cap.release()
    cv2.destroyWindow(window_name)
get_image()
